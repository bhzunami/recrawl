# -*- coding: utf-8 -*-

import random
import scrapy
from ..models import Ad


class Immoscout24(scrapy.Spider):
    name = "immoscout24"

    def get_clean_url(self, url):
        """Returns clean ad url for storing in database
        """
        return url.split('?')[0]

    def start_requests(self):
        # the l parameter describes the canton id
        urls = [
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-aargau?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-appenzell-ai?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-appenzell-ar?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-basel-landschaft?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-basel-stadt?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-bern?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-freiburg?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-genf?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-glarus?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-graubuenden?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-jura?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-luzern?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-neuenburg?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-nidwalden?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-obwalden?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-st-gallen?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-schaffhausen?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-schwyz?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-solothurn?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-thurgau?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-tessin?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-uri?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-waadt?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-wallis?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-zug?ps=120',
            'https://www.immoscout24.ch/de/immobilien/kaufen/kanton-zuerich?ps=120',
            # RENTS
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-aargau?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-appenzell-ai?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-appenzell-ar?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-basel-landschaft?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-basel-stadt?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-bern?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-freiburg?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-genf?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-glarus?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-graubuenden?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-jura?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-luzern?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-neuenburg?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-nidwalden?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-obwalden?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-st-gallen?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-schaffhausen?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-schwyz?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-solothurn?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-thurgau?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-tessin?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-uri?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-waadt?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-wallis?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-zug?ps=120',
            'https://www.immoscout24.ch/de/immobilien/mieten/kanton-zuerich?ps=120']

        random.shuffle(urls)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """ Parse the ad list """

        # find ads
        ad_link_path = '//a[@class="item-title"]/@href'

        for link in response.xpath(ad_link_path).extract():
            next_ad = response.urljoin(link)
            yield scrapy.Request(next_ad, callback=self.parse_ad)

        # find next page
        next_page_link = '//a[contains(@class, "next") and not(contains(@class, "disabled"))]/@href'
        next_page_url = response.xpath(next_page_link).extract_first()

        if next_page_url:
            self.logger.debug("Found next page: {}".format(next_page_url))
            next_page = response.urljoin(next_page_url)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_ad(self, response):
        ad = Ad()
        ad['crawler'] = 'immoscout24'
        ad['url'] = self.get_clean_url(response.url)
        ad['buy'] = True if 'kaufen' in ad['url'] else False
        ad['objecttype'] = response.url.split("/")[5].split("-")[0]
        ad['additional_data'] = {}
        ad['characteristics'] = {}
        # immoscout does have gibberish div names -> we are interessted in the h2 
        for selector in response.xpath('//h2'):
            article = selector.xpath('..')
            title = selector.xpath('text()').extract_first()
            if not title:
                continue
            title = title.lower()
            if 'zimmer' in title:
                ad['num_rooms'] = float(title.split()[0])
            if 'standort' in title:
                address =  article.xpath('p/text()').extract()
                # Missing street
                if len(address) == 4:
                    ad['street'] = None
                    ad['place'] = "{} {}".format(address[0], address[2])
                elif len(address) == 5:
                    ad['street'] = address[0]
                    ad['place'] = "{} {}".format(address[1], address[3])
            if 'hauptangaben' in title or 'preis' in title or 'grössenangaben' in title:
                for element in article.xpath('table/tbody/tr'):
                    try:
                        key, value = element.xpath('td/text()')
                    except ValueError as e:
                        self.logger.debug("Could not extract key value for {}".format(element.xpath('td/text()').extract()))
                        continue
                    key = key.extract()
                    try:
                        key = self.settings['KEY_FIGURES'][key]
                        ad[key] = value.extract()
                    except KeyError:
                        ad['characteristics'][key] = value.extract()
            if 'beschreibung' in title:
                ad['description'] = ' '.join(article.xpath('.//p//text()').extract())
            if 'innenraum' in title or 'aussenraum' in title or 'technik' in title:
                for element in article.xpath('table/tbody/tr'):
                    try:
                        key, value = element.xpath('td/text()').extract()
                        ad['characteristics'][key] = value
                    except ValueError:
                        key = element.xpath('td[1]/text()').extract_first()
                        ad['characteristics'][key] = True
            if 'merkmale' in title:
                for element in article.xpath('table/tbody/tr'):
                    try:
                        key, value = element.xpath('td/text()')
                    except ValueError as e:
                        key = element.xpath('td[1]/text()').extract_first()
                        ad['characteristics'][key] = True
                        continue
                    key = key.extract()
                    try:
                        key = self.settings['KEY_FIGURES'][key]
                        ad[key] = value.extract()
                    except KeyError:
                        ad['characteristics'][key] = value.extract()
        yield ad
