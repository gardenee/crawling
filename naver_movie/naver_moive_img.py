import requests
from bs4 import BeautifulSoup

html = requests.get("https://movie.naver.com/movie/sdb/rank/rmovie.naver").text
soup = BeautifulSoup(html, "html.parser")
tags = soup.select(".tit3>a")

for index, tag in enumerate(tags):
    rank = index+1
    title = tag.text
    print(rank, title)

    sub_page_url = "http://movie.naver.com" + tag["href"]
    html = requests.get(sub_page_url).text
    soup = BeautifulSoup(html, "html.parser")
    img_tag = soup.select_one(".poster>a>img")

    poster_url = img_tag["src"]

    filePath = "C:\\javaStudy\\upload\\movie\\" + str(rank) + title + ".jpg"

    file = open(filePath, "wb")
    file.write(requests.get(poster_url).content)
    file.close()
