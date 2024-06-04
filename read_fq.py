import pymysql


def read_fq():
    conn = pymysql.connect(
        host="127.0.0.1", user="root", password="1234", charset="utf8"
    )
    conn.select_db("carDB")
    cur = conn.cursor()

    cur.execute("SELECT * FROM faq")

    # 결과를 가져와 변수에 저장
    rows = cur.fetchall()

    # 연결 종료
    cur.close()
    conn.close()
    print("DB에서 F&Q  불러오기 성공")
    return rows
