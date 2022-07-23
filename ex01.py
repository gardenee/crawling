import requests
from bs4 import BeautifulSoup

response = requests.get("https://movie.naver.com/movie/sdb/rank/rmovie.naver")

stat_code = response.status_code #상태코드
html = response.text #html

soup = BeautifulSoup(html, "html.parser")

tags = soup.select(".tit3>a")

title = list()
for tag in tags:
    title.append(tag.text)

print(title)
