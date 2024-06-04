from selenium.webdriver import Chrome
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import pandas as pd

def get_page(driver,category, rest_time=0.1):
    bs = BeautifulSoup(driver.page_source, 'lxml')
    qa_dict = {'category':[], 'q':[], 'a':[]}
    
    total_cnt = len(bs.select('div.customer-toggle-btn > div'))
    current_cnt = 0
    
    # list 태그 정보를 담는 인덱스 정보가 불규칙하므로 Brute-Force 방식을 사용
    idx = 0
    
    while True:
        try:
            driver.find_element(By.CSS_SELECTOR, f'#faq-short-{idx} > div.customer-toggle-btn > div').click()
            time.sleep(rest_time)
        except:
            idx += 1
            continue
               
        bs = BeautifulSoup(driver.page_source, 'lxml')
        
        answer = ''
        for data in bs.select(f'#faq-short-{idx} > div.customer-toggle-cont.customer-cont-{idx}.active'):
            answer += data.text
            
        qa_dict['q'].append(bs.select_one(f'#faq-short-{idx} > div.customer-toggle-btn > div').text)
        qa_dict['a'].append(answer)
        qa_dict['category'].append(category)
        
        idx += 1; current_cnt += 1;
        time.sleep(rest_time)
    
        # 현재 카운트 개수와 전체 개수가 같을 경우를 기준으로 다음 행동을 분기
        if current_cnt == total_cnt:
            current_page = int(bs.select_one('#currentPage').text)
            total_page = int(bs.select_one('#totalPage').text)
    
            # 현재 페이지 수와 토탈 페이지 수가 같을 경우, 반복문을 탈출        
            if current_page == total_page:
                break
                
            else:
                driver.find_element(By.CSS_SELECTOR, '#wrap > div.customer-container > div > div.tab-cont.tab-normal > div > div.pagination-wrap > button.btn.btn-paging-next').click()
                time.sleep(rest_time)
                
                bs = BeautifulSoup(driver.page_source, 'lxml')
                
                total_cnt = len(bs.select('div.customer-toggle-btn > div'))
                current_cnt = 0

    return qa_dict    
    
def get_total_page(driver):
    category_li = ['short', 'long', 'common']
    total_qa_dict = {'category':[], 'q':[], 'a':[]}
    
    for i in range(len(category_li)):
        result = get_page(driver,category_li[i])
        
        total_qa_dict['category'] += result['category']
        total_qa_dict['q'] += result['q']
        total_qa_dict['a'] += result['a']
        
        if i == 0:
            driver.find_element(By.CSS_SELECTOR, '#long > button').click()
        elif i == 1:
            driver.find_element(By.CSS_SELECTOR, '#common > button').click()
            
    return total_qa_dict

def crawling_fq():
    url = 'https://www.lotterentacar.net/hp/kor/cs/faq/list.do'

    driver = Chrome()
    driver.get(url)

    result = get_total_page(driver)
    result_df = pd.DataFrame(result)
    print("F&Q 크롤링 성공")
    return result_df