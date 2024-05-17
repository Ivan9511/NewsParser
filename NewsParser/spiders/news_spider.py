import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import datetime
import sqlite3
import json
import sys
import os

# Добавляем путь к директории выше в список путей поиска модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# После этого можно импортировать модуль source.py
from models.source import Source

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

# scrapy crawl news_spider -o output.json -a count=5