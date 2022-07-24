from selenium import webdriver
from selenium.webdriver.common.by import By

wd = webdriver.Chrome("C:\\javaStudy\\프로그램\\chromedriver.exe")

url = "https://movie.daum.net/moviedb/grade?movieId=139606"
wd.get(url)
wd.implicitly_wait(10)

while True:
    try:
        wd.find_element(By.CSS_SELECTOR, ".alex_more").click()
        wd.implicitly_wait(2)
    except:
        print("마지막")
        break

cmt_tags = wd.find_elements(By.CSS_SELECTOR, ".cmt_info")

for i, cmt_tag in enumerate(cmt_tags):
    point = cmt_tag.find_element(By.CSS_SELECTOR, ".ratings").text

    try:
        cmt = cmt_tag.find_element(By.CSS_SELECTOR, "li p").text
    except:
        cmt = "************************************************"

    date = cmt_tag.find_element(By.CSS_SELECTOR, ".txt_date").text

    print(i+1, point, cmt, date, end="\n")
