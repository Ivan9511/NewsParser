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

class NewsSpiderSpider(CrawlSpider):
    name = "news_spider"
    
    sources = GetSources()
    allowed_domains = [source.name for source in sources]
    start_urls = [source.url for source in sources]

    rules = []
    for source in sources:
        if source.next_page_rule:
            rules.extend([
                Rule(LinkExtractor(restrict_xpaths=source.rule), callback='parse_item', follow=True, cb_kwargs={'source': source}),
                Rule(LinkExtractor(restrict_xpaths=source.next_page_rule), follow=True)
            ])
        else:
            rules.extend([
                Rule(LinkExtractor(restrict_xpaths=source.rule), callback='parse_item', follow=True, cb_kwargs={'source': source})
            ])
    rules = tuple(rules)

    def parse_item(self, response, source):
        item = {}
        item["source_id"] = source.id
        item["link"] = response.url
        title_raw = response.xpath(source.config["title"]).get()
        item["title"] = title_raw.strip() if title_raw else None
        content_raw = response.xpath(source.config["content"]).extract()
        item["content"] = ''.join(content_raw).strip()      
        item["date"] = response.xpath(source.config["date"]).get()
        item["created_at"] = datetime.datetime.now()
        
        self.save_to_db(item)
        return item
    
    def save_to_db(self, item):
        with dbConnection:
            dbConnection.execute("""
            INSERT INTO items (source_id, link, title, content, date, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                item["source_id"], 
                item["link"], 
                item["title"], 
                item["content"], 
                item["date"], 
                item["created_at"]
            ))
            
# CLOSESPIDER_ITEMCOUNT = 30 в settings.py
# Запуск в директории ...\NewsParser\NewsParser> scrapy crawl news_spider