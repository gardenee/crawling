import collections
import requests
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
import cx_Oracle


## 셀레니움 크롬 연결
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('lang=ko_KR')

try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=options)
    print("이미 드라이버가 설치되어있습니다.")
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=options)
    print("설치 완료")


## store_no 찾아오기
def select_store_no(store_name, store_road_address):
    conn = cx_Oracle.connect("lunchwb", "lunchwb", "localhost:1521/xe")
    cs = conn.cursor()

    sql = "SELECT store_no FROM store WHERE store_name = :store_name AND store_road_address = :store_road_address"
    rs = cs.execute(sql, store_name=store_name, store_road_address=store_road_address)

    result = 0
    for r in rs:
        result = r[0]

    cs.close()
    conn.close()

    return int(result)


## store 테이블 추가 함수
def insert_store(cate_2nd, store_name, store_x, store_y, store_road, store_old, store_opening, break_time):
    conn = cx_Oracle.connect("lunchwb", "lunchwb", "localhost:1521/xe")
    cs = conn.cursor()

    sql = "INSERT INTO store VALUES(seq_store_no.nextval, :cate_2nd, :store_name, :store_x, :store_y, :store_road, :store_old, :store_opening, :break_time, :visit)"

    cs.execute(sql, cate_2nd=cate_2nd, store_name=store_name, store_x=store_x, store_y=store_y, store_road=store_road, store_old=store_old, store_opening=store_opening, break_time=break_time, visit=0)
    conn.commit()

    cs.close()
    conn.close()


## store 영업시간 다시 추가
def update_store(store_no, store_opening_hours, store_breaktime):
    conn = cx_Oracle.connect("lunchwb", "lunchwb", "localhost:1521/xe")
    cs = conn.cursor()

    sql = "UPDATE store SET store_opening_hours = :store_opening_hours, store_breaktime = :store_breaktime WHERE store_no = :store_no"

    cs.execute(sql, store_opening_hours=store_opening_hours, store_breaktime=store_breaktime, store_no=store_no)
    conn.commit()

    cs.close()
    conn.close()


## rating_bujang 테이블에 추가
def insert_bujang(store_no):
    conn = cx_Oracle.connect("lunchwb", "lunchwb", "localhost:1521/xe")
    cs = conn.cursor()

    sql = "INSERT INTO rating_bujang VALUES(:store_no, 0, 0, 0)"

    cs.execute(sql, store_no=store_no)
    conn.commit()

    cs.close()
    conn.close()


## rating_others 테이블에 추가
def insert_others(store_no, rating_kakao):
    conn = cx_Oracle.connect("lunchwb", "lunchwb", "localhost:1521/xe")
    cs = conn.cursor()

    sql = "INSERT INTO rating_others VALUES(:store_no, 0, :rating_kakao, 0)"

    cs.execute(sql, store_no=store_no, rating_kakao=rating_kakao)
    conn.commit()

    cs.close()
    conn.close()


## rating_others 별점 다시 추가
def update_others(store_no, rating_kakao):
    conn = cx_Oracle.connect("lunchwb", "lunchwb", "localhost:1521/xe")
    cs = conn.cursor()

    sql = "UPDATE rating_others SET rating_kakao = :rating_kakao WHERE store_no = :store_no"

    cs.execute(sql, rating_kakao=rating_kakao, store_no=store_no)
    conn.commit()

    cs.close()
    conn.close()


## menu_2nd_cate 찾아오기
def select_2nd(cate_name):
    conn = cx_Oracle.connect("lunchwb", "lunchwb", "localhost:1521/xe")
    cs = conn.cursor()

    sql = "SELECT menu_2nd_cate_no FROM food_2nd_category WHERE menu_2nd_cate_name=:cate_name"

    rs = cs.execute(sql, cate_name=cate_name)

    for r in rs:
        result = r[0]

    cs.close()
    conn.close()

    return result


## menu_1st_cate 찾아오기
def select_1st(cate_name):
    conn = cx_Oracle.connect("lunchwb", "lunchwb", "localhost:1521/xe")
    cs = conn.cursor()

    sql = "SELECT menu_1st_cate_no FROM food_1st_category WHERE menu_1st_cate_name=:cate_name"

    rs = cs.execute(sql, cate_name=cate_name)

    for r in rs:
        result = r[0]

    cs.close()
    conn.close()

    return result


## 배열 문자열로 저장
def arr_change(lst):
    rtn = ""

    for l in lst:
        rtn += str(l) + " "

    return rtn[:-1]


## 카테고리 정보 저장할 사전
category_keys = ['뷔페', '아시아음식', '양식', '일식', '한식', '패스트푸드', '패밀리레스토랑', '치킨', '분식', '중식']

category_dict = dict()
category_dict['뷔페'] = ['해산물뷔페', '한식뷔페', '고기뷔페', '뷔페']
category_dict['아시아음식'] = ['터키음식', '동남아음식', '인도음식', '아시아음식']
category_dict['양식'] = ['스테이크,립', '햄버거', '피자', '해산물', '이탈리안', '멕시칸,브라질', '양식']
category_dict['일식'] = ['일본식라면', '일식집', '돈까스,우동', '참치회', '초밥,롤', '일식']
category_dict['한식'] = ['냉면', '국밥', '순대', '수제비', '죽', '설렁탕', '감자탕', '사철탕,영양탕', '곰탕', '두부전문점', '해물,생선', '해장국', '찌개,전골', '주먹밥', '육류,고기', '국수', '한정식', '쌈밥', '한식']
category_dict['패스트푸드'] = ['패스트푸드']
category_dict['패밀리레스토랑'] = ['패밀리레스토랑']
category_dict['치킨'] = ['치킨']
category_dict['분식'] = ['분식']
category_dict['중식'] = ['중식']


## 요일 참조용 리스트
ref_day = ['월', '화', '수', '목', '금', '토', '일']


## 영업시간 + 브레이크타임 찾기 함수
def opening_search(driver):
    opening_hour = ['정보없음'] * 7
    break_time = ['정보없음'] * 7

    try:
        opening = driver.find_element(By.CSS_SELECTOR, ".list_operation").text.split()
    except:
        print(store_name, "영업시간 정보가 없음")
        opening = []

    if "더보기" in opening:
        try:
            more_btn = driver.find_element(By.CSS_SELECTOR, ".btn_more").click()
            driver.implicitly_wait(3)
        except:
            print("클릭 오류")

        try:
            opening = driver.find_element(By.CSS_SELECTOR, ".fold_floor").text.split()
        except:
            print("세부 시간 불러오기 오류")
            opening = []

    if opening:
        if '영업시간' in opening:
            opening.remove('영업시간')
        if '닫기' in opening:
            opening.remove('닫기')

        temp = [False] * 7
        time = ""

        n = 0
        for m in opening:
            if n == 0:
                if m == '매일':
                    temp = [True] * 7

                elif '~' in m and m[0] in ref_day:
                    start = ref_day.index(m[0])
                    end = ref_day.index(m[2])
                    for i in range(start, end + 1):
                        temp[i] = True

                elif ',' in m and (not '공휴일' in m) and (not '브레이크' in m) and m[0] in ref_day:
                    curr = m.split(",")
                    for c in curr:
                        idx = ref_day.index(c[0])
                        temp[idx] = True

                elif m[0] in ref_day:
                    idx = ref_day.index(m[0])
                    temp[idx] = True

                else:
                    temp = [False] * 7
                    continue

                n += 1

            elif n == 1:
                if ":" in m:
                    time += m
                    n += 1

                elif m == "브레이크타임":
                    n = 4

                else:
                    n = 0

            elif n == 2:
                if m == "~":
                    time += m
                    n += 1

                else:
                    n = 0

            elif n == 3:
                if ":" in m:
                    if int(time[:2]) > int(m[:2]):
                        m = str(int(m[:2]) + 24) + m[2:]
                    time += m

                    for i in range(7):
                        if temp[i]:
                            opening_hour[i] = time

                    temp = [False] * 7
                    time = ""
                    n = 0

            elif n == 4:
                time += m
                n += 1

            elif n == 5:
                time += m
                n += 1

            elif n == 6:
                time += m

                for i in range(7):
                    if temp[i]:
                        break_time[i] = time

                temp = [False] * 7
                time = ""
                n = 0

        if '정보없음' in opening_hour and opening_hour.count('정보없음') != 7:
            for i in range(7):
                if opening_hour[i] == '정보없음':
                    opening_hour[i] = '휴무일'
                    break_time[i] = '휴무일'

    return opening_hour, break_time


## 카카오 API
def whole_region(keyword, start_x, start_y, end_x, end_y):
    page_num = 1

    all_data_list = []

    while (True):
        url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
        params = {'query': keyword, 'page': page_num, 'rect': f'{start_x},{start_y},{end_x},{end_y}'}
        headers = {"Authorization": "KakaoAK bde0ccb3c7c732a5380910cd2be9a535"}

        resp = requests.get(url, params=params, headers=headers)
        search_count = resp.json()['meta']['total_count']

        if search_count > 45:
            print('좌표 4등분')
            dividing_x = (start_x + end_x) / 2
            dividing_y = (start_y + end_y) / 2

            all_data_list.extend(whole_region(keyword, start_x, start_y, dividing_x, dividing_y))
            all_data_list.extend(whole_region(keyword, dividing_x, start_y, end_x, dividing_y))
            all_data_list.extend(whole_region(keyword, start_x, dividing_y, dividing_x, end_y))
            all_data_list.extend(whole_region(keyword, dividing_x, dividing_y, end_x, end_y))

            return all_data_list

        else:
            if resp.json()['meta']['is_end']:
                print('데이터추가')
                all_data_list.extend(resp.json()['documents'])

                return all_data_list

            else:
                print('다음페이지')
                page_num += 1
                all_data_list.extend(resp.json()['documents'])


def overlapped_data(keyword, start_x, start_y, next_x, next_y, num_x, num_y):
    overlapped_result = []

    for i in range(1, num_x + 1):  ## 1,10
        end_x = start_x + next_x
        initial_start_y = start_y
        for j in range(1, num_y + 1):  ## 1,6
            end_y = initial_start_y + next_y
            each_result = whole_region(keyword, start_x, initial_start_y, end_x, end_y)
            overlapped_result.extend(each_result)
            initial_start_y = end_y
        start_x = end_x

    return overlapped_result


# 시작 좌표 및 증가값
keyword = '음식점'
start_x = 126.8991376
start_y = 37.4393374
next_x = 0.01
next_y = 0.01
num_x = 10
num_y = 6


overlapped_result = overlapped_data(keyword, start_x, start_y, next_x, next_y, num_x, num_y)

# 최종 데이터가 담긴 리스트 중복값 제거
results = list(map(dict, collections.OrderedDict.fromkeys(tuple(sorted(d.items())) for d in overlapped_result)))
print("==========데이터 일단 가져옴==========================================================")
print("추리기 전 데이터 수:", len(results))

"""
# txt 저장할 내용들 

with open("메뉴.txt", "w") as file:
    file.write("\n")

with open("별점.txt", "w") as file:
    file.write("저장 안된 별점 목록\n")

with open("크롤링데이터.txt", "w") as file:
    file.write("\n")
"""

cnt = 0


for place in results:
    if "관악구" in place['road_address_name']:
        X = float(place['x'])
        Y = float(place['y'])
        store_name = place['place_name']
        address_name = place['address_name']
        road_address = place['road_address_name']
        place_url = place['place_url']
        ID = place['id']
        full_category = place['category_name'].replace('>', '').split()
        rating = ""

        ## 카테고리 정리하기
        if len(full_category) >= 2 and full_category[1] in list(category_keys):
            """
            # 혹시 모르니 데이터 세이브
            with open("크롤링데이터.txt", "a") as file:
                file.write(str(cnt + 1) + " {")
                for key in place.keys():
                    file.write(str(key) + ": " + str(place[key]) + "  ")
                file.write("}\n")
            """

            if len(full_category) == 2:
                category_2nd = select_2nd(full_category[1])
            else:
                if full_category[2] in category_dict[full_category[1]]:
                    category_2nd = select_2nd(full_category[2])
                else:
                    category_2nd = select_2nd(full_category[1])

            print(store_name, cnt+1)

            """
            ## breakpoint
            if cnt < 3300: 
                cnt += 1
                continue
            """

            driver.get(place_url)
            driver.implicitly_wait(5)

            opening_hour, break_time = opening_search(driver)

            ## db에 추가
            cnt += 1

            insert_store(category_2nd, store_name, X, Y, road_address, address_name, arr_change(opening_hour), arr_change(break_time))
            insert_bujang(cnt)

            store_no = select_store_no(store_name, road_address)
            if store_no == 0:
                continue

            """
            # 영업시간 못가져온 경우 추가
            if opening_hour != ['정보없음'] * 7:
                update_store(store_no, arr_change(opening_hour), arr_change(break_time))
            """

            ## 별점 가져오기 + db에 추가
            try:
                rating = float(driver.find_element(By.CSS_SELECTOR, ".link_evaluation>span").text)
            except:
                print(store_name, "별점 못가져온듯")
                with open("별점.txt", "a") as file:
                    file.write(str(cnt) + " " + store_name + " " + str(ID) + "\n")

            insert_others(store_no, rating)

            """
            # 별점 못가져온 경우 추가
            if rating != 0:
                update_others(store_no, rating)
            """

            """
            ## 메뉴 목록 긁어오기
            try:
                lst = driver.find_elements(By.CSS_SELECTOR, ".loss_word")
                with open("메뉴.txt", "a") as file:
                    for l in lst:
                        file.write(str(select_1st(full_category[1])) + " " + str(category_2nd) + l.text + "\n")
            except:
                print("메뉴 못불러옴")
            """

print('total_result_number = ', cnt)

driver.quit()
