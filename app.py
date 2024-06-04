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
from crawling_fq import crawling_fq
from insert_fq import insert_fq
from read_fq import read_fq

@st.cache_data
def get_data():
    # DB 및 테이블 생성
    model.db_model.create_table()

    # DataFrame 가져오기
    rechargers = csvRead.get_rechargers()
    car_regist = csvRead.get_car_regist()
    avg_cap = get_avg_cap.get_avg_cap()
    fq = crawling_fq()

    # DB에 rechargers, car_regist, f&q 저장
    insert_rechargers(rechargers)
    insert_car_regist(car_regist)
    insert_fq(fq)

    # DB에서 rechargers, car_regist 불러오기
    df1 = pd.DataFrame(read_rechargers())
    df2 = pd.DataFrame(read_car_regist())
    df3 = pd.DataFrame(read_fq())

    return df1, df2, df3, fq, avg_cap

# get_data 함수 호출
df1, df2, df3, fq, avg_cap = get_data()

# 페이지 선택
page = st.sidebar.selectbox("Choose a page", ["Homepage", "단기 질문","장기 질문","공통 질문"])

# 페이지에 따른 내용 표시
if page == "Homepage":
    st.header("서울시 구역별 전기자동차 충전량")
    # 한글 폰트 설정
    matplotlib.rcParams["font.family"] = "Malgun Gothic"

    # 글꼴 크기 설정
    matplotlib.rcParams["font.size"] = 3
    # 플롯할 데이터
    labels1 = df1[0]
    values1 = df1[1]

    labels2 = df2[0]
    values2 = df2[1]

    df = df1.sort_values(by=1, ascending=False)
    df = df2.sort_values(by=1, ascending=False)

    # figure와 axes 객체 생성
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()

    

    # 막대 그래프 생성
    ax1.bar(labels1, values1)
    ax2.bar(labels2, values2)

    # 그래프 제목 및 y축 레이블 설정
    ax1.set_title('서울시 각 구별 충전량')
    ax1.set_ylabel('충전량 (kWh)')

    ax2.set_title('서울시 가 구별 전기자동차 등록 수')
    ax2.set_ylabel('단위 (대)')
    # Streamlit에서 플롯 표시
    st.pyplot(fig1)
    st.pyplot(fig2)


elif page == "단기 질문":
    st.header("단기 렌트 질문")
    st.dataframe(df3[(df3[0]=="short")][[1,2]])

elif page == "장기 질문":
    st.header("장기 렌트 질문")
    st.dataframe(df3[(df3[0]=="long")][[1,2]])

elif page == "공통 질문":
    st.header("공통 질문")
    st.dataframe(df3[(df3[0]=="common")][[1,2]])
