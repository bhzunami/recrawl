# -*- coding: utf-8 -*-

import random
import json
import scrapy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, desc
from models import Advertisement
from ..models import Ad

CRAWLER_NAME = "comparis"

class Comparis(scrapy.Spider):
    name = CRAWLER_NAME
    start_urls = "https://www.comparis.ch/immobilien/marktplatz/details/show/"

    def __init__(self, *args, **kwargs):
        super(Comparis, self).__init__(*args, **kwargs)
        # Set up database connection
        engine = create_engine(self.settings['DATABASE_URL'])
        self.Session = sessionmaker(bind=engine)

    def get_clean_url(self, url):
        """Returns clean ad url for storing in database
        """
        return url

    def start_requests(self):
        session = self.Session()
        last_ad = session.query(Advertisement) \
                .filter(Advertisement.crawler==CRAWLER_NAME) \
                .order_by(desc(Advertisement.id)) \
                .first()
        if last_ad:
            start_url_counter = int(last_ad.url.split('/')[-1])
        else:
            start_url_counter = 2
        
        for id in range(start_url_counter, start_url_counter + 5000):
            url = "{}{}".format(self.start_urls, id)
            yield scrapy.Request(url=url, callback=self.parse_ad)

    def parse_ad(self, response):
        ad = Ad()
        ad['crawler'] = CRAWLER_NAME
        ad['url'] = self.get_clean_url(response.url)
        yield ad
