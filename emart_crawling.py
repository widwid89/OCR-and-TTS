from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time
import urllib.request
import os
import schedule
import time
from datetime import datetime


def marketcurly_crawling(category):
    if category == '우유':
        num = '6000213534'
        page_num = 1
    elif category == '밀키트':
        num = '6000213247'
        page_num = 2
    elif category == '김치':
        num = '6000213299'
        page_num = 3
    elif category == '생수':
        num = '6000213424'
        page_num = 4
    elif category == '커피':
        num = '6000215245'
        page_num = 5
    elif category == '면류':
        num = '6000213319'
        page_num = 6
    elif category == '양념':
        num = '6000215286'
        page_num = 7
    elif category == '과자':
        num = '6000213362'
        page_num = 8
    elif category == '베이커리':
        num = '6000213412'
        page_num = 9
    elif category == '건강식품':
        num = '6000213046'
        page_num = 10
        
    item_list = [] #상품명, 이미지 리스트 저장
    detail_list = []
    count = 2
        
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    options.binary_location = '/usr/bin/google-chrome' # 여기에 실제 Chrome 실행 파일 경로를 넣어주세요
    options.add_argument('--headless') 
    s = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=s, options=options)
    
    url = 'https://emart.ssg.com/disp/category.ssg?dispCtgId='+num
    driver.get(url)
    driver.implicitly_wait(time_to_wait=5)
    elements = driver.find_elements(By.CLASS_NAME, 'mnemitem_tit') #상품명에 접근

    # 상품 8개만큼 반복
    for i in range(32,40):
        elements = driver.find_elements(By.CLASS_NAME, 'mnemitem_tit')
        element = elements[i]
    
        #상품명
        item_name = element.text
        
        #상품 클릭
        element.click()
        time.sleep(count)
        
        #상품 가격
        item_price = driver.find_element(By.CLASS_NAME, 'cdtl_new_price').text
        
        #상세정보페이지는 iframe으로 되어있어서 아래와 같은 접근이 필요함
        iframe = driver.find_element(By.CSS_SELECTOR, '#_ifr_html')
        driver.switch_to.frame(iframe)
        
        try:
            item_img = driver.find_element(By.CSS_SELECTOR, '#wrap_ifr > div > div.cdtl_tmpl_guide > div > div > div:nth-child(1) > img').get_attribute('src')
            detail_img = driver.find_element(By.CSS_SELECTOR, '#wrap_ifr > div > div.cdtl_tmpl_guide > div > div > div:nth-child(2) > img').get_attribute('src')
        except:
            try:
                detail_img = driver.find_element(By.CSS_SELECTOR, '#wrap_ifr > div > div.cdtl_tmpl_guide > div > div > div > img').get_attribute('src')
                driver.switch_to.default_content()
                item_img = driver.find_element(By.XPATH, '//*[@id="mainImg"]').get_attribute('src')
            except:
                driver.switch_to.default_content()
                item_img = driver.find_element(By.XPATH, '//*[@id="mainImg"]').get_attribute('src')
                detail_img = driver.find_element(By.XPATH,'//*[@id="item_detail"]/div[1]/div[2]/div[2]/img').get_attribute('src')
        
        item_list.append([item_name, item_price, item_img])
        detail_list.append([item_name, detail_img])
        
        # 브라우져 뒤로가기
        driver.execute_script("window.history.go(-1)")
        time.sleep(count)

    # 작업 완료 후 드라이버 종료
    driver.quit()
    print('A')
    #df 저장
    item_df = pd.DataFrame(data=item_list,columns=['item_name', 'item_price', 'item_img'])
    detail_df = pd.DataFrame(data=detail_list,columns=['item_name', 'detail_img'])
    print('B')
    #데이터프레임 csv 저장하기
    item_df.to_csv(f"/home/kchh1015/proj2/Dataset/{category}/{page_num}"+"item"+".csv", sep= ',', encoding='utf-8', index=False)
    detail_df.to_csv(f"/home/kchh1015/proj2/Dataset/{category}/{page_num}"+"detail"+".csv", sep= ',', encoding='utf-8', index=False)
    print('C')
    ### img_url -> jpg로 저장하기
    #저장할 위치
    save_at = f"/home/kchh1015/proj2/Dataset/{category}/"
    save_at1 = f'/home/kchh1015/proj2/Dataset/{category}이미지/'
    print('D')
    #for문 돌려서 df url -> jpg로 모두 저장
    for i in range(len(item_list)):
        url1 = item_df['item_img'][i]
        url2 = detail_df['detail_img'][i]
        urllib.request.urlretrieve(url1, save_at1+"item"+str(i)+".jpg")
        urllib.request.urlretrieve(url2, save_at+"detail"+str(i)+".jpg")

# marketcurly_crawling('우유') 
# marketcurly_crawling('김치') 
# marketcurly_crawling('생수')
# marketcurly_crawling('커피') 
# marketcurly_crawling('면류') 
# marketcurly_crawling('양념') 
# marketcurly_crawling('과자') 
# marketcurly_crawling('베이커리') 
# marketcurly_crawling('건강식품')
marketcurly_crawling('밀키트')

#############sheduling#################

def job():
    # Specify the base output directory
    base_output_dir = "/home/kchh1015/proj2/Dataset"

    # Get the current date for creating a unique output directory
    current_date = datetime.now().strftime("%Y%m%d")
    output_dir = os.path.join(base_output_dir, current_date)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Run the crawler for each category
    categories = ['우유', '밀키트', '김치', '생수', '커피', '면류', '양념', '과자', '베이커리', '건강식품']
    for category in categories:
        marketcurly_crawling(category, output_dir)

# Schedule the job to run once a month
schedule.every().month.at('00:00').do(job)

while True:
    schedule.run_pending()
    time.sleep(1)