from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import cx_Oracle
from selenium.webdriver.common.keys import Keys
import bs4


## 셀레니움 크롬 연결
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('lang=ko_KR')

try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=options)
    print("이미 드라이버가 설치되어있습니다.")
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=options)
    print("설치 완료")

store_name = '믹스앤테이블'
store_address = '서울 관악구 시흥대로160길 12'
rating = 0

driver.get(url="https://map.naver.com/v5/")
driver.implicitly_wait(5)

try:
    search_bar = driver.find_element(By.CSS_SELECTOR, ".input_search")
    search_bar.click()
    search_bar.send_keys(store_name)
    search_bar.send_keys(Keys.ENTER)
    driver.implicitly_wait(5)

    frame = driver.find_element(By.CSS_SELECTOR, "#entryIframe")
    driver.switch_to.frame(frame)
    driver.implicitly_wait(5)

    soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
    rating = float(soup.select_one("._20Ivz > span > em").text)

except NoSuchElementException:
    try:
        search_bar = driver.find_element(By.CSS_SELECTOR, ".input_search")
        search_bar.click()
        search_bar.send_keys(store_name)
        search_bar.send_keys(Keys.ENTER)
        driver.implicitly_wait(5)

        driver.switch_to.default_content()
        frame = driver.find_element(By.CSS_SELECTOR, "#searchIframe")
        driver.switch_to.frame(frame)
        driver.implicitly_wait(5)
        body = driver.find_element(By.CSS_SELECTOR, "body")
        body.click()
        try:
            for i in range(5):
                body.send_keys(Keys.PAGE_DOWN)
        except:
            print("스크롤 안됨")
        print(3)
        driver.implicitly_wait(5)
        print(4)
        results = driver.find_elements(By.CSS_SELECTOR, "li ._3ZU00 ._2w9xx ._2s4DU .place_bluelink")
        print(5)
        i = 0
        for result in results:
            print(6+i)
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
                rating = float(driver.find_element(By.CSS_SELECTOR, "._20Ivz > span > em").text)
                break

            driver.switch_to.default_content()
            driver.switch_to.frame(frame)
            driver.implicitly_wait(10)
    except:
        print("검색해도 안나오는 가게")
except:
    print("오류발생")

print(rating)
