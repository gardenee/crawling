from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import cx_Oracle
from selenium.webdriver.common.keys import Keys
import bs4


## rating_others 테이블에 데이터 추가
def update(store_no, rating_naver):
    conn = cx_Oracle.connect("lunchwb", "lunchwb", "localhost:1521/xe")
    cs = conn.cursor()

    sql = "UPDATE rating_others SET rating_naver=:rating_naver WHERE store_no=:store_no"

    cs.execute(sql, rating_naver=rating_naver, store_no=store_no)
    conn.commit()

    cs.close()
    conn.close()


## store 정보 찾아오기
def select():
    conn = cx_Oracle.connect("lunchwb", "lunchwb", "localhost:1521/xe")
    cs = conn.cursor()

    sql = "SELECT store_no, store_name, store_road_address FROM store ORDER BY store_no ASC"

    rs = cs.execute(sql)

    result = list()
    for r in rs:
        result.append(list(r))

    cs.close()
    conn.close()

    return result


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


## 크롤링하기
store_lst = select()
for store in store_lst[8:]:
    store_no = store[0]
    store_name = store[1]
    store_address = store[2]
    rating = 0

    print(store_no, store_name, store_address, end=" ")

    driver.get(url="https://map.naver.com/v5/")
    driver.implicitly_wait(5)

    try: ## 검색해서 바로 가게가 나오는 경우
        search_bar = driver.find_element(By.CSS_SELECTOR, ".input_search")
        search_bar.click()
        search_bar.send_keys(store_name)
        search_bar.send_keys(Keys.ENTER)
        driver.implicitly_wait(10)

        frame = driver.find_element(By.CSS_SELECTOR, "#entryIframe")
        driver.switch_to.frame(frame)
        driver.implicitly_wait(5)

        soup = bs4.BeautifulSoup(driver.page_source, "html.parser")

        try:
            rating = float(soup.select_one("._20Ivz > span > em").text)
        except:
            print("별점미공개", end=" ")

    except NoSuchElementException: ## 가게 목록에서 찾아야 하는 경우
        try:
            search_bar = driver.find_element(By.CSS_SELECTOR, ".input_search")
            search_bar.click()
            search_bar.send_keys(store_name)
            search_bar.send_keys(Keys.ENTER)
            driver.implicitly_wait(10)

            driver.switch_to.default_content()
            frame = driver.find_element(By.CSS_SELECTOR, "#searchIframe")
            driver.switch_to.frame(frame)
            driver.implicitly_wait(5)
            body = driver.find_element(By.CSS_SELECTOR, "body")
            body.click()

            # 스크롤 내리기
            try:
                for i in range(5):
                    body.send_keys(Keys.PAGE_DOWN)
            except:
                print("스크롤끝", end=" ")

            driver.implicitly_wait(10)

            results = driver.find_elements(By.CSS_SELECTOR, "li ._3ZU00 ._2w9xx ._2s4DU .place_bluelink")

            i = 0
            for result in results:
                i += 1
                if i > 15:
                    break

                result.click()
                driver.switch_to.default_content()
                driver.implicitly_wait(5)

                entry_frame = driver.find_element(By.CSS_SELECTOR, "#entryIframe")
                driver.switch_to.frame(entry_frame)
                driver.implicitly_wait(5)

                address = driver.find_element(By.CSS_SELECTOR, "._6aUG7 ._1h3B_ ._2yqUQ").text
                if address == store_address:
                    try:
                        rating = float(driver.find_element(By.CSS_SELECTOR, "._20Ivz > span > em").text)
                    except:
                        print("별점미공개", end=" ")
                    break

                driver.switch_to.default_content()
                driver.switch_to.frame(frame)
                driver.implicitly_wait(10)
        except:
            rating = -1
            with open("별점이슈.txt", "a") as file:
                file.write(str(store_no) + " " + store_name)

    print(rating)
    if rating > 0:
        update(store_no, rating)
