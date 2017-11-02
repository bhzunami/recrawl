# -*- coding: utf-8 -*-
"""
Find the correct municipality

"""
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import ObjectType
from ..settings import DATABASE_URL

logger = logging.getLogger(__name__)

class ObjectTypeFinderPipeline(object):
    def open_spider(self, spider):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=engine, expire_on_commit=True)

    def process_item(self, item, spider):
        self.session = self.Session()

        object_str = item.get('objecttype', '').lower()
        # Check if the type of the object is already in the Database
        # If we do not have the type we store a new type.
        logger.debug("Search for type %s", object_str)
        obtype = self.session.query(ObjectType).filter(ObjectType.name == object_str).first()
        if not obtype:
            logger.info("New objecttype found: {}".format(object_str))
            # Store new ObjectType
            obtype = ObjectType(name=object_str)
            self.session.add(obtype)
            # To get the new id
            self.session.commit()
            logger.debug("Objecttype stored with id: %i", obtype.id)

        # Set the correct id
        item['obtype_id'] = obtype.id
        return item

    def close_spider(self, spider):
        self.session.close()