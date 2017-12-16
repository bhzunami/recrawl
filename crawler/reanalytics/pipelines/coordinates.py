# -*- coding: utf-8 -*-
"""
Get longitude and latitude from the openstreetmap

Example for URL request
https://api3.geo.admin.ch/rest/services/api/SearchServer?searchText=Holeestrass3 160&type=locations&limit=5

"""
import logging
import requests
from ..settings import ADMIN_BASE_URL

logger = logging.getLogger(__name__)

class CoordinatesPipeline(object):
    """ Get longitude and latitude for a specific address from the api3.geo.admin.ch
    """

    def process_item(self, item, spider):
        """after item is processed
        """
        logger.debug("Execute coordinate assignment for item %s %s from Spider[%s]",
                      item.get('street', None),
                      item.get('place', None),
                      spider.name)

        if not item.get('street', None) or 'auf anfrage' in item.get('street', '').lower():
            logger.info("Ignore street %s for finding coordinates", item.get('street', None))
            item['street'] = ''

        params = {'type': 'locations',
                  'limit': 1,
                  'searchText': '{} {}'.format(item.get('street', ''), item.get('place', ''))}

        req = requests.get(ADMIN_BASE_URL, params=params)
        if req.status_code != 200:
            logger.warning("Could not get long and lat for addres %s, %s",
                            item.get('street', None),
                            item.get('place', None))
            return item

        # At the moment always get frist element
        response = req.json()
        item['address_fuzzy'] = False
        if response.get("fuzzy", False):
            item['address_fuzzy'] = True
            logger.info("Request for address %s seems fuzzy", params.get('searchText', ''))

        addresses = response.get('results', [])
        # Did not get an answer
        if len(addresses) != 1:
            logger.warning("Could not get long lat for address %s", params.get('searchText', ''))
            return item

        address = addresses[0]
        item['longitude'] = address.get('attrs', {}).get('lon', None)
        item['latitude'] = address.get('attrs', {}).get('lat', None)
        item['lv03_easting'] = address.get('attrs', {}).get('y', None)
        item['lv03_northing'] = address.get('attrs', {}).get('x', None)
        logger.debug("Found long {} lat {} for address {}".format(item.get('longitude', None),
                                                                   item.get('latitude', None),
                                                                   params.get('searchText', None)))
        return item
