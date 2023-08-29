import os
import requests
import random
from bs4 import BeautifulSoup
from feedgenerator import Rss201rev2Feed
from dateutil.parser import parse
from xml.dom.minidom import parseString

# ファイル名
exportfile = "feed.xml"

def create_rss_feed():
    url = "https://newspicks.com/theme-news/9980/"

    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.902.84 Safari/537.36 Edg/92.0.902.84'
    ]
    return random.choice(user_agents)

    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept-Language': 'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    
    #response = requests.get(url)
    response = requests.get(url, headers=headers)
    content = response.text

    # HTMLの解析
    soup = BeautifulSoup(content, 'html.parser')
    #print('# HTMLの解析')
    #print(soup)

    # RSSフィードの生成
    feed = Rss201rev2Feed(
        title="NewsPicks Categoly：AI",
        link=url,
        description="最新のAI関連のニュースをお届けします",
    )

    # 最初の記事の情報を取得
    first_article_div = soup.find('div', class_="css-7q0s18")

    if first_article_div is None:
        print("first_article_div が None やで！クラス名やタグが正しいか確認してみてな！")
        # デバッグ情報として、対象のHTMLの一部を出力
        print(soup.prettify()[:500]) # 最初の500文字を出力
    else:
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

    # 2個目以降の記事の情報を取得してRSSフィードに追加
    for a_tag in soup.find_all('a', class_="css-dv7pnt", href=True):
        if a_tag is None:
            continue
        title_tag = a_tag.find(class_="typography css-1ta5siq")
        subtitle_tag = a_tag.find(class_="typography css-rvnxno")
        time_tag = a_tag.find('time', datetime=True)
        href = a_tag['href']

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
