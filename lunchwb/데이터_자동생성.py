import random
import cx_Oracle

def insert_users(email, password, name, birth_year, sex):
    conn = cx_Oracle.connect("lunchwb", "lunchwb", "localhost:1521/xe")
    cs = conn.cursor()

    sql = "INSERT INTO users VALUES(seq_user_no.nextval, :email, :password, :name, :birth_year, :sex, sysdate, 1, 'none', '')"

    cs.execute(sql, email=email, password=password, name=name, birth_year=birth_year, sex=sex)
    conn.commit()

    cs.close()
    conn.close()


def insert_groups(group_leader, group_name):
    conn = cx_Oracle.connect("lunchwb", "lunchwb", "localhost:1521/xe")
    cs = conn.cursor()

    sql = "INSERT INTO groups VALUES(seq_group_no.nextval, :group_leader, :group_name)"

    cs.execute(sql, group_name=group_name, group_leader=group_leader)
    conn.commit()

    cs.close()
    conn.close()


def insert_member(user_no, group_no, leader, boss):
    conn = cx_Oracle.connect("lunchwb", "lunchwb", "localhost:1521/xe")
    cs = conn.cursor()

    sql = "INSERT INTO group_member VALUES(seq_group_member_no.nextval, :user_no, :group_no, :leader, :boss, '')"

    cs.execute(sql, user_no=user_no, group_no=group_no, leader=leader, boss=boss)
    conn.commit()

    cs.close()
    conn.close()


def insert_visited(user_no, group_no, store_no):
    conn = cx_Oracle.connect("lunchwb", "lunchwb", "localhost:1521/xe")
    cs = conn.cursor()

    sql = "INSERT INTO visited VALUES(seq_visited_no.nextval, :user_no, :group_no, :store_no, '', sysdate)"

    cs.execute(sql, user_no=user_no, group_no=group_no, store_no=store_no)
    conn.commit()

    cs.close()
    conn.close()


def insert_review(user_no, visited_no, review_content, user_score):
    conn = cx_Oracle.connect("lunchwb", "lunchwb", "localhost:1521/xe")
    cs = conn.cursor()

    sql = "INSERT INTO review VALUES(seq_review_no.nextval, :user_no, :visited_no, :review_content, :user_score, '', 0)"

    cs.execute(sql, user_no=user_no, visited_no=visited_no, review_content=review_content, user_score=user_score)
    conn.commit()

    cs.close()
    conn.close()



gender = ["male", "female"]

## 회원 삽입
for i in range(1, 101):
    email = "test" + str(i) + "@naver.com"
    password = "1234"
    name = "test" + str(i)
    birth_year = random.randrange(1950, 2003)
    sex = gender[random.randrange(0, 2)]

    insert_users(email, password, name, birth_year, sex)
    print("users", email)


## 그룹 삽입
for i in range(1, 21):
    group_name = "group" + str(i)

    insert_groups(i, group_name)
    print("groups", group_name)
    insert_member(i, i, 1, 0)
    print("group_member", i)


## 1~20번 유저 그룹원 삽입
for i in range(1, 21):
    group1 = (i+5)%21
    group2 = (i+10)%21

    if group1 == 0:
        group1 += 1
    if group2 == 0:
        group2 += 1

    insert_member(i, group1, 0, 0)
    print("group_member", i, group1)
    insert_member(i, group2, 0, 0)
    print("group_member", i, group2)


## 그룹원 삽입
for i in range(22, 101):
    group_no = random.randrange(1, 21)
    insert_member(i, group_no, 0, 0)
    print("group_member", i, group_no)

## 방문 기록 + 리뷰 삽입
n = 0
for i in range(14, 21):
    group1 = (i + 5) % 21
    group2 = (i + 10) % 21

    if group1 == 0:
        group1 += 1
    if group2 == 0:
        group2 += 1

    groups = [i, group1, group2]

    for _ in range(50):
        n += 1
        store_no = 552
        while store_no == 552:
            store_no = random.randrange(1, 4023)

        insert_visited(i, i, store_no)
        print("visited", i, store_no)
        insert_review(i, n, "리뷰" + str(n), random.randrange(1, 6))
        print("review", i)
