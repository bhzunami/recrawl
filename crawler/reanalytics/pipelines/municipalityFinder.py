# -*- coding: utf-8 -*-
"""
Find the correct municipality

"""
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Municipality
from models.utils import extract_number, get_place, extract_municipality
from ..settings import DATABASE_URL

class MunicipalityFinderPipeline(object):

    def open_spider(self, spider):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=engine, expire_on_commit=True)


    def process_item(self, item, spider):
        """
        process the crawled item to find the correct municipality
        """
        session = self.Session()

        # Next we have to find our place from the zip and name from the database
        # Get zip
        zip_code, *name = get_place(item.get('place'))
        name = extract_municipality(' '.join(name))
        # Search in database
        municipalities = session.query(Municipality) \
            .filter(Municipality.zip == extract_number(zip_code)) \
            .all()

        # It is possible to get more than one municipality so if this happens
        # we search through all
        municipality = None

        # Only one was found
        if len(municipalities) == 1:
            municipality = municipalities[0]
            logging.debug("Found exact one %s ", municipality.name)

        if len(municipalities) > 1:
            logging.debug("Found more than one {} search for {}".format(len(municipalities), name))
            for mun in municipalities:
                if mun.name.startswith(name) or name in mun.alternate_names:
                    municipality = mun
                    logging.debug("Found the municipality '%s' for input: %s",
                                  municipality.name,
                                  item.get('place'))
                    break

        if municipality:
            item['municipality_id'] = municipality.id
            logging.debug("Found municipality: {} {}".format(municipality.zip, municipality.name))
        else:
            item['municipality_id'] = None
            logging.warning("Could not find zip_code {} {} in database".format(zip_code, name))

        return item
