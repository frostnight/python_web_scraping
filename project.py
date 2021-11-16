import re

import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString


def create_soup(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def print_news(index, title, link):
    print(f"{index+1}. {title}")
    print(f" ( 링크 : {link} )")

def scrape_weather():
    print("[오늘의 날씨]")
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8"
    soup = create_soup(url)
    # 흐림, 어제보다 00º 높아요
    cast = soup.find("p", attrs={"class":"summary"}).get_text()
    # 현재 00ºC (최저 00º / 최고 00º)
    #cur_temps = soup.find("div", attrs={"class":"temperature_text"}).find_all()
    cur_temp_tag = soup.select_one(".temperature_text > strong")
    cur_temp = None
    for tag in cur_temp_tag:
        if isinstance(tag, NavigableString):
            cur_temp = tag
            break

    min_temp = soup.find("li", attrs={"class":"week_item today"}).find("span", attrs={"class":"lowest"}).get_text()
    min_temp = min_temp.replace("기온", " ")
    max_temp = soup.find("li", attrs={"class":"week_item today"}).find("span", attrs={"class":"highest"}).get_text()
    max_temp = max_temp.replace("기온", " ")
    # 오전 강수확률 00% / 오후 강수확률 00%
    rain_rate = soup.find_all("span", attrs={"class":"weather_left"})
    morning_rain_rate = rain_rate[0].find("span", attrs={"class":"rainfall"}).get_text().strip()
    afternoon_rain_rate = rain_rate[1].find("span", attrs={"class":"rainfall"}).get_text().strip()
    # 미세먼지, 초미세먼지, 자외선
    add_weather = soup.find("ul", attrs={"class":"today_chart_list"}).find_all("li", attrs={"class":"item_today level2"})
    dust = add_weather[0].find("span",attrs={"class":"txt"}).get_text()
    hyper_dust = add_weather[1].find("span",attrs={"class":"txt"}).get_text()
    ultraviolet = add_weather[2].find("span",attrs={"class":"txt"}).get_text()

    print(cast)
    print("현재 {}° ({} / {})".format(cur_temp, min_temp, max_temp))
    print("오전 강수확률 {} / 오후 강수확률{}".format(morning_rain_rate, afternoon_rain_rate))
    print("미세먼지 {} / 초미세먼지 {} / 자외선 {}".format(dust, hyper_dust, ultraviolet))

def scrape_headline_news():
    print("[헤드라인 뉴스]")
    url = "https://news.naver.com"
    soup = create_soup(url)
    news_list = soup.find("ul", attrs={"class":"hdline_article_list"}).find_all("li", limit=3)
    for index, news in enumerate(news_list):
        title = news.find("a").get_text().strip()
        link = url+news.find("a")["href"]
        print_news(index, title, link)
    print()

def scrape_it_news():
    print("[IT 뉴스]")
    url = "https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=105&sid2=230"
    soup = create_soup(url)
    news_list = soup.find("ul", attrs={"class":"type06_headline"}).find_all("li", limit=3) # 개까지
    for index, news in enumerate(news_list):
        img = news.find("a").img
        if img:
            title = img["alt"]
        else:
            title = news.find("a").get_text().strip()
        link = news.find("a")["href"]
        print_news(index, title, link)
    print()

def scrape_english():
    print("[오늘의 영어 회화]")
    url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english&keywd=haceng_submain_lnb_eng_I_others_english&logger_kw=haceng_submain_lnb_eng_I_others_english#;"
    soup = create_soup(url)
    sentences = soup.find_all("div", attrs={"id":re.compile("^conv_kor_t")})
    print("(영어 지문)")
    for sentence in sentences[len(sentences)//2:]: # 8문장이 있다고 가정할 때, index 기준 4~7까지 잘라서 가져옴
        print(sentence.span.b.get_text().strip())

    print("(한글 지문)")
    for sentence in sentences[0:len(sentences)//2]: # 8문장이 있다고 가정할 때, index 기준 0~3까지 잘라서 가져옴
        print(sentence.span.b.get_text().strip())

    print()

if __name__ == "__main__":
    #scrape_weather() # 오늘의 날씨 정보 가져오기
    #scrape_headline_news() # 헤드라인 뉴스 정보 가져오기
    #scrape_it_news() # IT 뉴스 정보 가져오기
    scrape_english() # 오늘의 영어 회화 가져오기
