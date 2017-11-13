# -*- coding: utf-8 -*-
"""
Store advertisement in database

"""
import logging
import json
from datetime import date, datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Advertisement, ObjectType, Municipality
from models.utils import extract_number, get_place, extract_municipality
from ..settings import DATABASE_URL

logger = logging.getLogger(__name__)

class DatabaseWriterPipeline(object):

    def open_spider(self, spider):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        logger.info("Open spider Database wirter")
        engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):
        """after item is processed
        """
        self.session = self.Session()
        ad = Advertisement(item)

        # Store the add in the database
        try:
            self.session.add(ad)
            self.session.commit()
        except Exception as exception:
            logger.error("Could not save advertisement %s cause %s", ad.object_id, exception)
            self.session.rollback()

        return item


