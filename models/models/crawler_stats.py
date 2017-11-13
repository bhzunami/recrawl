# -*- coding: utf-8 -*-
"""
Statistical data for a crawler
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from .utils import Base


class CrawlerStats(Base):
    """Advertisment class to store in the database
    """
    __tablename__ = 'crawler_stats'

    id = Column(Integer, primary_key=True)
    crawler = Column(String)         # The name of the crawler
    started = Column(DateTime)
    ended = Column(DateTime)
    errors = Column(Integer)
    exceptions = Column(Integer)
    warnings = Column(Integer)
    infos = Column(Integer)
    requests = Column(Integer)
    responses = Column(Integer)
    ignored = Column(Integer)
    items = Column(Integer)
    finish_reason = Column(String)

    def __init__(self, data):
        self.merge(data)

    def merge(self, data):
        self.crawler = data.get('crawler')
        self.started = data.get('start_time')
        self.ended = data.get('finish_time')
        self.errors = data.get('log_count/ERROR')
        self.exceptions = data.get('downloader/exception_count')
        self.warnings = data.get('log_count/WARNING')
        self.infos = data.get('log_count/INFO')
        self.requests = data.get('downloader/request_count')
        self.responses = data.get('downloader/response_count')
        self.ignored = data.get('downloader/exception_type_count/scrapy.exceptions.IgnoreRequest')
        self.items = data.get('item_scraped_count')
        self.finish_reason = data.get('finish_reason')

    def __str__(self):
        return "CrawlerStats [crawler={}, started={}, ended={}, items_scraped={}]".format(self.crawler, self.started, self.ended, self.items)

