from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36")

browser = webdriver.Chrome(options=options)
browser.maximize_window()

url = "https://www.daum.net"
browser.get(url)

keyword = "송파 아이파크"
inputKeyword = browser.find_element(By.ID, "q")
inputKeyword.send_keys(keyword)
inputKeyword.send_keys(Keys.ENTER)

soup = BeautifulSoup(browser.page_source, "lxml")
trades= soup.find("div", attrs={"class":["wrap_tbl", "tbl_trade"]}).find("tbody").find_all("tr")

print("trades", trades)
