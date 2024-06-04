import pandas as pd

# 서울시 시소유 전기차충전소 충전량
rechargers_csv_path = "./csvs/서울특별시_소유 전기차충전소의 충전량_20240229.csv"
car_regist_csv_path = "./csvs/서울시 자치구별 전기차 용도별 등록현황(2017~2022년).csv"


def get_rechargers():
    df = pd.read_csv(rechargers_csv_path, encoding="cp949")

    # 23년도만 보기
    df = df[(df["충전날짜"] >= "2023-01-01") & (df["충전날짜"] <= "2023-12-31")]
    # 주소, 충전량만 보기
    df = df[["주소", "충전량(kWh)"]]

    # 구단위로 주소 자르기
    df["주소"] = df["주소"].str.split("구").str[0] + "구"

    # 구로구 주소 정상화
    df["주소"] = df["주소"].replace("서울 구", "서울 구로구")

    # 아웃라이어 주소들 병합
    df["주소"] = df["주소"].replace("서울시 성동구", "서울 성동구")
    df["주소"] = df["주소"].replace(" 서울 송파구", "서울 송파구")
    df["주소"] = df["주소"].str.split("울").str[1]
    # 구별 충전량의 합 계산
    df_grouped = df.groupby("주소")["충전량(kWh)"].sum().reset_index()
    print("충전소 csv 데이터 읽어오기 성공")

    return df_grouped


def get_car_regist():
    # csv read
    df = pd.read_csv(car_regist_csv_path, encoding="cp949")
    # 21년도만 보기
    df = df[(df["연월별"] == "2021-12-31")]
    # 시군구별, 계 col 만 보기
    df = df[["시군구별", "계"]]
    # 시군구별 합 구하기
    df_grouped = df.groupby("시군구별")["계"].sum().reset_index()
    print("자동차 csv 데이터 등록현황 읽어오기 성공 ")
    return df_grouped
