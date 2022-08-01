from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By


chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
ID = 10957180

menu_category = []
rating = []
opening_hours = []

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

driver.get(url="http://place.map.kakao.com/" + str(ID))
driver.implicitly_wait(5)


try:
    opening = driver.find_element(By.CSS_SELECTOR, ".list_operation").text
except:
    opening = ""

if "더보기" in opening:
    try:
        more_btn = driver.find_element(By.CSS_SELECTOR, ".btn_more").click()
        driver.implicitly_wait(3)
    except:
        print("클릭 오류")

    try:
        opening = driver.find_element(By.CSS_SELECTOR, ".fold_floor").text
    except:
        print("오류다다")


opening_hour = ['정보없음'] * 8
break_time = ['정보없음'] * 7

lst = opening.split("\n")
lst.remove("영업시간")
print(lst)
driver.quit()
