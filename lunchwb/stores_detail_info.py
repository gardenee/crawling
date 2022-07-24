from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By


chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
ID = 15538644

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

menu_cate = driver.find_element(By.CSS_SELECTOR, ".txt_location").text
rating = driver.find_element(By.CSS_SELECTOR, ".link_evaluation>span").text
opening_hour = driver.find_element(By.CSS_SELECTOR, ".list_operation").text.split()
if not opening_hour:
    opening_hours.append('정보없음')

print(menu_cate)
print(rating)
print(opening_hour)

driver.quit()
