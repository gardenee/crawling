import cx_Oracle

def insert(menu_2nd_cate_no, menu_name):
    conn = cx_Oracle.connect("lunchwb", "lunchwb", "localhost:1521/xe")
    cs = conn.cursor()

    sql = "INSERT INTO menu VALUES(seq_menu_no.nextval, :menu_2nd_cate_no, :menu_name, '')"

    cs.execute(sql, menu_2nd_cate_no=menu_2nd_cate_no, menu_name=menu_name)
    conn.commit()

    cs.close()
    conn.close()


with open("메뉴분류.tsv", "r", encoding="utf-8") as file:
    while True:
        line = file.readline()
        print(line)
        if not line:
            break
        ipt = line.split("\t", maxsplit=2)
        cate_2nd = int(ipt[1])
        menu = ipt[2].rstrip()

        insert(cate_2nd, menu)
