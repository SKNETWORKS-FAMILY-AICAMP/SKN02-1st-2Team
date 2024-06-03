import csvRead
import model.db_model
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import get_avg_cap
from insert_recharging import insert_rechargers
from insert_car_regist import insert_car_regist
from read_car_regist import read_car_regist
from read_rechargers import read_rechargers

# DB 및 테이블 생성
model.db_model.create_table()

# DataFrame 가져오기
rechargers = csvRead.get_rechargers()
car_regist = csvRead.get_car_regist()
avg_cap = get_avg_cap.get_avg_cap()
print(f"평균 배터리 용량 = {avg_cap}")

# DB에 rechargers, car_regist 저장
insert_rechargers(rechargers)
insert_car_regist(car_regist)

# DB에서 rechargers, car_regist 불러오기
df1 = pd.DataFrame(read_rechargers())
df2 = pd.DataFrame(read_car_regist())

# 페이지 선택
page = st.sidebar.selectbox("Choose a page", ["Homepage", "Page 1"])

# 페이지에 따른 내용 표시
if page == "Homepage":
    st.header("서울시 구역별 전기자동차 충전량")

    # 플롯할 데이터
    labels1 = df1[0]
    sizes1 = df1[1]

    labels2 = df2[0]
    sizes2 = df2[1]

    df = df1.sort_values(by=1, ascending=False)
    df = df2.sort_values(by=1, ascending=False)

    # figure와 axes 객체 생성
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()

    # 한글 폰트 설정
    matplotlib.rcParams["font.family"] = "Malgun Gothic"

    # 글꼴 크기 설정
    matplotlib.rcParams["font.size"] = 5

    # 파이 차트 생성
    ax1.pie(sizes1, labels=labels1, autopct="%1.1f%%")
    ax2.pie(sizes2, labels=labels2, autopct="%1.1f%%")

    # Streamlit에서 플롯 표시
    st.pyplot(fig1)
    st.pyplot(fig2)
    
elif page == "Page 1":
    st.header("기업 F&Q")
    # 여기에 페이지 1의 내용을 추가합니다.
