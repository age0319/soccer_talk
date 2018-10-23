import csv
import feedparser
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os

UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/files/'


class Scrape:

    def __init__(self, csv_name="default.csv", json_name="default.json"):
        self.csv_name = csv_name
        self.json_name = json_name

    def scrape_ranking(self):

        # URLの指定
        html = urlopen("https://www.jleague.jp/standings/j2/")
        bs = BeautifulSoup(html, "html.parser")

        # テーブルを指定
        table = bs.findAll("table", {"class": "scoreTable01 J2table tablesorter"})[0]
        rows = table.findAll("tr")

        path = os.path.join(UPLOAD_DIR, self.csv_name)
        csv_file = open(path, 'wt', newline='', encoding='utf-8')
        writer = csv.writer(csv_file)

        try:
            for row in rows:
                csv_row = []
                for cell in row.findAll(['td', 'th']):
                    # <td>の中にspanがある場合はチーム名が２つ取れてしまう。
                    if cell.find('span'):
                        csv_row.append(cell.span.get_text())
                    else:
                        csv_row.append(cell.get_text())
                writer.writerow(csv_row)

        finally:
            csv_file.close()

    def scrape_news(self):
        # 取得する記事の数、最大で20個
        entry_num = 20

        url = "https://news.google.com/news/rss/search/section/q/j2%e3%83%aa%e3%83%bc%e3%82%b0/j2%e3%83%aa%e3%83%bc%e3" \
              "%82%b0?ned=jp&hl=ja&gl=JP"

        d = feedparser.parse(url)
        news = list()

        for i, entry in enumerate(d.entries[:entry_num], 1):
            p = entry.published_parsed
            sortkey = "%04d%02d%02d%02d%02d%02d" % (p.tm_year, p.tm_mon, p.tm_mday, p.tm_hour, p.tm_min, p.tm_sec)

            tmp = {
                "no": i,
                "title": entry.title,
                "link": entry.link,
                "published": entry.published,
                "sortkey": sortkey
            }

            news.append(tmp)

        news = sorted(news, key=lambda x: x['sortkey'], reverse=True)

        path = os.path.join(UPLOAD_DIR, self.json_name)

        with open(path, 'w') as f:
            json.dump(news, f)


if __name__ == '__main__':

    ins = Scrape(csv_name="ranking.csv", json_name="news.json")
    ins.scrape_news()
    ins.scrape_ranking()

