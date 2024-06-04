import pymysql


def insert_fq(input_fq):

    conn = pymysql.connect(
        host="127.0.0.1", user="root", password="1234", charset="utf8"
    )
    conn.select_db("carDB")
    cur = conn.cursor()

    # 데이터프레임의 각 행을 반복하며 SQL INSERT 문 실행
    for row in input_fq.itertuples():
        sql = "INSERT INTO faq (type, question,answer) VALUES (%s, %s, %s)"
        cur.execute(sql, (row[1], row[2],row[3]))

    # 변경사항 저장
    conn.commit()

    # 연결 종료
    cur.close()
    conn.close()

    print("F&Q DB에 insert성공")
