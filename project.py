import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString


def create_soup(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

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
        print(f"{index+1}. {title}")
        print(f" ( 링크 : {link}")
    print()


if __name__ == "__main__":
    #scrape_weather() # 오늘의 날씨 정보 가져오기
    scrape_headline_news()
