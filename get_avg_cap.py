from selenium.webdriver import Chrome
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

def get_avg_cap():
    page_no = 1
    url = f"https://auto.danawa.com/leaserent/?Work=leaserentSearch&Tab=list&Brand=&Classify=&Fuel=20&Price=&Period=36&PriceType=2&Order=popular&Punit=30&SearchWord=&MinPrice=0&MaxPrice=&Page={page_no}"

    driver = Chrome()
    driver.get(url)

    total_battery = 0
    total_cnt = 0

    # 최대 2페이지까지 존재
    for i in range(1, 2 + 1):
        bs = BeautifulSoup(driver.page_source, "lxml")

        # 배터리 정보 가져오기
        battery_li = bs.select("div.mid_con > div.car_info > ul > li:nth-child(5)")

        for j in range(len(battery_li)):
            battery = battery_li[j].text.replace("배터리 용량 ", "")
            total_battery += sum(map(float, battery[:-3].split("~")))
            total_cnt += 1

        # 마지막 페이지가 아닌 경우만 페이지 넘기기
        if i != 2:
            clickable = driver.find_element(By.ID, f"leaserent_page{i+1}")
            clickable.click()
            time.sleep(1.5)
    driver.quit()

    avg_battery = round(total_battery / total_cnt, 1)
    
    return avg_battery
