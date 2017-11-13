import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from scrapy import signals
from models import CrawlerStats as Stats
from ..settings import DATABASE_URL

class CrawlerStats(object):
    def __init__(self, crawler):
        self.crawler = crawler
        engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=engine, expire_on_commit=True)
        crawler.signals.connect(self.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(self.spider_closed, signal=signals.spider_closed)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)


    def spider_opened(self, spider):
        self.crawler.stats.set_value('crawler', spider.name)


    def spider_closed(self, spider):
        self.session = self.Session()
        try:
            stats = Stats(self.crawler.stats.get_stats())
            self.session.add(stats)
            self.session.commit()
        except Exception as exception:
            logging.error("Could not save crawler statistics %s cause %s", stats, exception)
            self.session.rollback()
        finally:
            self.session.close()
