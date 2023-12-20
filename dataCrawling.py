from selenium.webdriver.common.by import By
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re
from selenium.webdriver.common.keys import Keys
import time
import requests
from openpyxl import Workbook

# 네이버 블로그 개수 기준 1000개 이상인 가게들 중 최근 블로그 리뷰에 대가성 표기가 3개 이상 되어있는 가게들만 선정하였습니다.

# 식당 리뷰 개별 url 접속
"""
urls = ['https://m.place.naver.com/restaurant/1324132180/review/visitor', 'https://m.place.naver.com/restaurant/83612604/review/visitor', 'https://m.place.naver.com/restaurant/1323525758/review/visitor', 'https://m.place.naver.com/restaurant/329955337/review/visitor',
        'https://m.place.naver.com/restaurant/1171532481/review/visitor', 'https://m.place.naver.com/restaurant/1266673496/review/visitor', 'https://m.place.naver.com/restaurant/1404784472/review/visitor', 'https://m.place.naver.com/restaurant/1835052467/review/visitor',
        'https://m.place.naver.com/restaurant/1426989264/review/visitor', 'https://m.place.naver.com/restaurant/13114967/review/visitor'
        ]
resNames = ['더스테이크쥬벤쿠바', '어썸로즈', '진작', '고가빈커리하우스', 'H라운지', '살롱순라', '오마', '남산도담', '을지다락 여의도', '진대감 마포점']
"""

urls = ['https://m.place.naver.com/restaurant/1171532481/review/visitor', 'https://m.place.naver.com/restaurant/1266673496/review/visitor', 'https://m.place.naver.com/restaurant/1404784472/review/visitor', 'https://m.place.naver.com/restaurant/1835052467/review/visitor',
        'https://m.place.naver.com/restaurant/1426989264/review/visitor', 'https://m.place.naver.com/restaurant/13114967/review/visitor'
        ]
resNames = ['H라운지', '살롱순라', '오마', '남산도담', '을지다락 여의도', '진대감 마포점']


# Webdriver headless mode setting
options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

# BS4 setting for secondary access
session = requests.Session()
headers = {
    #사용자의 user-agent값
    "User-Agent": "$User value"}

retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[500, 502, 503, 504])

session.mount('http://', HTTPAdapter(max_retries=retries))
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

for i in range(len(urls)):
    xlsx = Workbook()
    list_sheet = xlsx.create_sheet('output')
    list_sheet.append(['restaurant name','content', 'tag'])

#url = 'https://m.place.naver.com/restaurant/1562525784/review/visitor'
#    url = 'https://m.place.naver.com/restaurant/1036217683/review/visitor'
    url = urls[i]

    resName = resNames[i]



    # Start crawling/scraping!
    res = driver.get(url)
    driver.implicitly_wait(30)

    # Pagedown
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

    try:
        while True:
            driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[7]/div[2]/div[3]/div[2]').click()
            time.sleep(0.4)
    except Exception as e:
        print('finish')


    time.sleep(10)
    blindContect = driver.find_elements(By.CLASS_NAME, "xHaT3")
    time.sleep(0.4)

    for element in blindContect:
        driver.execute_script("arguments[0].click();", element)
        time.sleep(0.4)
    print("open content")

    time.sleep(10)
    html = driver.page_source
    bs = BeautifulSoup(html, 'lxml')
    reviews = bs.select('li.YeINN')

    for r in reviews:
        content = r.select_one('span.zPfVt')

        # exception handling
        content = content.text if content else ''

 	# append sheet
        list_sheet.append([resName, content, 0])
        time.sleep(0.5)
    file_name = 'naver_review_' + resName + '.xlsx'
    xlsx.save(file_name)

driver.close()
