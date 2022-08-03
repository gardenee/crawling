import cx_Oracle

def select_2nd(cate_name):
    conn = cx_Oracle.connect("lunchwb", "lunchwb", "localhost:1521/xe")
    cs = conn.cursor()

    sql = "SELECT menu_2nd_cate_no FROM food_2nd_category WHERE menu_2nd_cate_name=:cate_name"

    rs = cs.execute(sql, cate_name=cate_name)

    for r in rs:
        result = r[0]

    cs.close()
    conn.close()

    return result

print(select_2nd("분식"))
