import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
browser.maximize_window() # 창 최대화

url = "https://flight.naver.com/"
browser.get(url) # url로 이동

# 가는 날 선택 클릭
browser.find_element(By.CLASS_NAME, "select_Date__1aF7Y").click()
calElem = browser.find_element(By.CLASS_NAME, "calendar_content__1Xc5a")

# 이번달 27일, 28일 선택
#calElem.find_elements(By.XPATH, '//button[normalize-space()="27"]')[0].click()
#calElem.find_elements(By.XPATH, '//button[normalize-space()="28"]')[0].click()

# 다음달 27일, 28일 선택
#calElem.find_elements(By.XPATH, '//button[normalize-space()="27"]')[1].click()
#calElem.find_elements(By.XPATH, '//button[normalize-space()="28"]')[1].click()

# 이번달 27일, 다음달 28일 선택
calElem.find_elements(By.XPATH, '//button[normalize-space()="27"]')[0].click()
calElem.find_elements(By.XPATH, '//button[normalize-space()="28"]')[1].click()

# 도착 선택
browser.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[1]/button[2]').click()
browser.find_element(By.CLASS_NAME, "autocomplete_input__1vVkF").send_keys("제주도")
time.sleep(1)
browser.find_elements(By.CLASS_NAME, "autocomplete_search_item__2WRSw")[0].click()

# 항공권 검색 클릭
browser.find_element(By.XPATH, '//button[normalize-space()="항공권 검색"]').click()

try:
    elem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'result')))
    # 성공했을 때 동작 수행
    print("text", elem.text) # 첫 번째 결과 출력

except TimeoutError:
    print("ERR")

finally:
    pass
    #browser.quit()
