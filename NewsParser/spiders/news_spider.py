import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import datetime
import sqlite3
import json

class Source:
    def __init__(self, id: int, name: str, url: str, config: dict):
        self.id = id
        self.name = name
        self.url = url
        self.config = config

        # Извлечение данных из config
        self.rule = config.get("rule")
        self.next_page_rule = config.get("next_page_rule")
        self.title = config.get("title")
        self.content = config.get("content")
        self.date = config.get("date")

    def __repr__(self):
        return (
            f"Source(id={self.id}, name='{self.name}', url='{self.url}', "
            f"rule='{self.rule}', next_page_rule='{self.next_page_rule}', "
            f"title_rule='{self.title_rule}', content_rule='{self.content_rule}', "
            f"date_rule='{self.date_rule}')"
        )

dbConnection = sqlite3.connect(r'../SourceParserDB.db')

def GetSources():
    cur = dbConnection.cursor()
    cur.execute("SELECT * FROM sources")
    rows = cur.fetchall()

    sources = []  # Создаем пустой список для объектов Source
    for row in rows:
        # Преобразуем строку конфигурации из JSON в словарь
        config = json.loads(row[3])
        source = Source(id=row[0], name=row[1], url=row[2], config=config)  # Заменяем Source на source
        sources.append(source)  # Добавляем объект Source в список

    return sources

sources = GetSources()

for source in sources:
    print(source)

class NewsSpiderSpider(CrawlSpider):
    name = "news_spider"
    allowed_domains = ["nur.kz"]
    start_urls = ["http://www.nur.kz/latest"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//article/a[@class='article-preview-category__content']"), callback="parse_item", follow=True),        
        )

    def parse_item(self, response):
        item = {}
        item["source_id"] = 1
        item["link"] = response.url
        item["title"] = response.xpath("//article/h1[contains(@class, 'main-headline')]/text()").get()
        item["content"] = ''.join(response.xpath("//div[contains(@class, 'formatted-body__content--wrapper')]/p//text()").extract())
        item["date"] = response.xpath("//div[contains(@class, 'layout-content-type-page__wrapper-block')]/p/time[contains(@class, 'datetime datetime--publication')]/@datetime").get()
        item["created_at"] = datetime.datetime.now()
        return item
