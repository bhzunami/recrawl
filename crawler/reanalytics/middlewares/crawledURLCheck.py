# -*- coding: utf-8 -*-
"""
    Checks if the given URL was already processed
"""
import logging
import datetime
from scrapy.exceptions import IgnoreRequest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Advertisement
from ..settings import DATABASE_URL

class CrawledURLCheck(object):

    def __init__(self):
        engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=engine, expire_on_commit=True)


    def process_request(self, request, spider):
        """check if the url was already crawled
        """
        if type(spider).__name__ == "DefaultSpider":
            return
        clean_url = spider.get_clean_url(request.url)
        logging.debug("Check if %s is already in database?", clean_url)
        session = self.Session()
        advertisement = session.query(Advertisement).filter(Advertisement.url == clean_url).first()
        if advertisement:
            logging.info("This url %s was already crawled update last seen", clean_url)
            advertisement.last_seen = datetime.datetime.now()
            session.add(advertisement)
            session.commit()
            raise IgnoreRequest

        session.close()
        logging.debug("URL %s was not found in database.", clean_url)
        return None
