import pymysql


def insert_rechargers(input_rechargers):
    rechargers = input_rechargers

    conn = pymysql.connect(
        host="127.0.0.1", user="root", password="1234", charset="utf8"
    )
    conn.select_db("carDB")
    cur = conn.cursor()

    # 데이터프레임의 각 행을 반복하며 SQL INSERT 문 실행
    for row in rechargers.itertuples():
        sql = "INSERT INTO chargingamount (addr, charging_amount) VALUES (%s, %s)"
        cur.execute(sql, (row[1], row[2]))

    # 변경사항 저장
    conn.commit()

    # 연결 종료
    cur.close()
    conn.close()
