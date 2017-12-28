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

logger = logging.getLogger(__name__)

class CrawledURLCheck(object):

    def __init__(self):
        engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=engine, expire_on_commit=True)


    def process_request(self, request, spider):
        """check if the url was already crawled
        """
        if type(spider).__name__ == "DefaultSpider":
            return None

        clean_url = spider.get_clean_url(request.url)

        # Do not check start_urls because these are not added to the database
        if clean_url in [spider.get_clean_url(u) for u in spider.start_urls]:
            return None

        logger.debug("Check if URL[{}] is in database for Spider[{}]".format(clean_url, spider.name))
        session = self.Session()
        advertisement = session.query(Advertisement).filter(Advertisement.url == clean_url).first()
        if advertisement:
            logger.info("The URL '{}' was already crawled. Update last seen".format(clean_url))
            advertisement.last_seen = datetime.datetime.now()
            session.add(advertisement)
            session.commit()
            raise IgnoreRequest

        session.close()
        return None
