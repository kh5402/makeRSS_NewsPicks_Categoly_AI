import os
import requests
from bs4 import BeautifulSoup
from feedgenerator import Rss201rev2Feed
from dateutil.parser import parse
from xml.dom.minidom import parseString

# 環境変数からファイルパスを取得
exportfile = "NewsPicks_Categoly_AI_feed.xml"

# 拡張子を追加
exportfile += ".xml"

def create_rss_feed():
    url = "https://newspicks.com/theme-news/9980/"
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
                    pubdate=date, # 日付をRSSリーダーで取得したときの日付として使用
                    description="", # descriptionを空にする
                )

    # RSSフィードのXMLを出力
    xml_str = feed.writeString('utf-8')
    dom = parseString(xml_str)
    pretty_xml_str = dom.toprettyxml(indent="    ", encoding='utf-8')

    with open('feed.xml', 'wb') as f:
        f.write(pretty_xml_str)

create_rss_feed()
