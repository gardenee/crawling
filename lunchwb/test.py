import collections
import requests
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By

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

## db 연결
conn = cx_Oracle.connect("lunchwb", "lunchwb", "localhost:1521/xe")

##카카오 API
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
num_x = 11
num_y = 7

overlapped_result = overlapped_data(keyword, start_x, start_y, next_x, next_y, num_x, num_y)

# 최종 데이터가 담긴 리스트 중복값 제거
results = list(map(dict, collections.OrderedDict.fromkeys(tuple(sorted(d.items())) for d in overlapped_result)))
cnt = 0

for place in results:
    if "관악구" in place['road_address_name']:
        cnt += 1

        X = float(place['x'])
        Y = float(place['y'])
        store_name = place['place_name']
        road_address = place['road_address_name']
        place_url = place['place_url']
        ID = place['id']
        full_category = place['category_name'].replace('>', '').split()
        opening_hour = [정보없음] * 8
        break_time = [정보없음] * 7

        if len(full_category) >= 2 and full_category[1] != "간식" and full_category[1] != "술집":
            category_1st = full_category[1]

            if len(full_category) <= 2:
                category_2nd = full_category[1]
            else:
                category_2nd = full_category[2]

            driver.get(place_url)
            driver.implicitly_wait(5)

            try:
                rating = driver.find_element(By.CSS_SELECTOR, ".link_evaluation>span").text
            except:
                rating = 0
            #opening_hour = driver.find_element(By.CSS_SELECTOR, ".list_operation").text

            if float(rating) > 0:
                print("가게명", place['place_name'], "주소", place['road_address_name'], "카테고리", category, "별점", rating)


print('total_result_number = ', cnt)

driver.quit()
