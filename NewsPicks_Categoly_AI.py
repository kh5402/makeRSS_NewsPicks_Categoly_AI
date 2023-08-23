import os
import requests
from bs4 import BeautifulSoup
from feedgenerator import Rss201rev2Feed
from dateutil.parser import parse
from xml.dom.minidom import parseString

# ファイル名
exportfile = "feed.xml"

def create_rss_feed():
    url = "https://newspicks.com/theme-news/9980/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url)
    content = response.text

    # HTMLの解析
    soup = BeautifulSoup(content, 'html.parser')

    # RSSフィードの生成
    feed = Rss201rev2Feed(
        title="NewsPicks Categoly：AI",
        link=url,
        description="最新のAI関連のニュースをお届けします",
    )

    # 最初の記事の情報を取得
    first_article_div = soup.find('div', class_="css-7q0s18")
    a_tag = first_article_div.find('a', href=True)
    title_tag = first_article_div.find(class_="typography css-19plv60")
    subtitle_tag = first_article_div.find(class_="typography css-rvnxno")
    time_tag = first_article_div.find('time', datetime=True)

    title = title_tag.text
    subtitle = subtitle_tag.text
    href = a_tag['href']
    date = parse(time_tag['datetime'])

    feed.add_item(
        title=title + " - " + subtitle,
        link=href,
        pubdate=date,
        description="",
    )

    # 各記事の情報を取得してRSSフィードに追加
    for div_tag in soup.find_all('div', class_="css-19so664"):
        a_tag = div_tag.find('a', href=True)
        href = a_tag['href']
        if "newspicks.com/news" in href:
            title_tag = a_tag.find(class_="typography css-iom819")
            subtitle_tag = a_tag.find(class_="typography css-xgbdwh")
            time_tag = a_tag.find('time', datetime=True)

            if title_tag and subtitle_tag and time_tag:
                title = title_tag.text
                subtitle = subtitle_tag.text
                date = parse(time_tag['datetime'])

                full_title = title + " - " + subtitle

                feed.add_item(
                    title=full_title,
                    link=href,
                    pubdate=date,
                    description="",
                )

    # RSSフィードのXMLを出力
    xml_str = feed.writeString('utf-8')
    dom = parseString(xml_str)
    pretty_xml_str = dom.toprettyxml(indent="    ", encoding='utf-8')

    with open(exportfile, 'wb') as f:
        f.write(pretty_xml_str)

create_rss_feed()
