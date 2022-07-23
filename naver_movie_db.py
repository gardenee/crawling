import cx_Oracle
import requests
from bs4 import BeautifulSoup


def insert(movie):
    conn = cx_Oracle.connect("webdb", "webdb", "localhost:1521/xe")
    cs = conn.cursor()

    rank = movie[0]
    title = movie[1]
    filepath = movie[2]

    sql = "insert into movie values (seq_movie_no.nextval, :rank, :title, :filepath)"

    cs.execute(sql, rank=rank, title=title, filepath=filepath)
    conn.commit()

    cs.close()
    conn.close()

    return cs.rowcount


html = requests.get("https://movie.naver.com/movie/sdb/rank/rmovie.naver").text
soup = BeautifulSoup(html, "html.parser")
tags = soup.select(".tit3>a")

for index, tag in enumerate(tags):
    rank = index+1
    title = tag.text
    title = title.replace(":", "")

    sub_page_url = "http://movie.naver.com" + tag["href"]
    html = requests.get(sub_page_url).text
    soup = BeautifulSoup(html, "html.parser")
    img_tag = soup.select_one(".poster>a>img")

    poster_url = img_tag["src"]

    filePath = "C:\\javaStudy\\upload\\movie\\" + str(rank) + title + ".jpg"

    file = open(filePath, "wb")
    file.write(requests.get(poster_url).content)
    file.close()

    movie = [rank, title, filePath]
    n = insert(movie)
    print("\"" + str(rank) + "." + title + "\" 저장되었습니다.")
