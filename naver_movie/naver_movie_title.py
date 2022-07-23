import requests
from bs4 import BeautifulSoup

response = requests.get("https://movie.naver.com/movie/sdb/rank/rmovie.naver")

stat_code = response.status_code #상태코드
html = response.text #html

soup = BeautifulSoup(html, "html.parser")

tags = soup.select(".tit3>a")
#하나만 추출하기: tag = soup.select_one(".tit3>a").text

for index, tag in enumerate(tags):
    print(str(index+1) + "위 " + tag.text)
