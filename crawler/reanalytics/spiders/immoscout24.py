# -*- coding: utf-8 -*-

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

        # price, number of rooms, living area
        for div in response.xpath('//div[contains(@class, "layout--columns")]/div[@class="column" and ./div[@class="data-label"]]'):
            key, value, *_ = [x.strip() for x in div.xpath('div//text()').extract()]
            try:
                key = self.settings['KEY_FIGURES'][key]
                ad[key] = value
            except KeyError:
                self.logger.warning("Key not found: {}".format(key))
                ad['additional_data'][key] = value

        # location
        loc = response.xpath('//table//div[contains(@class, "adr")]')
        ad['street'] = loc.xpath('div[contains(@class, "street-address")]/text()').extract_first()
        ad['place'] = "{} {}".format(loc.xpath('span[contains(@class, "postal-code")]/text()').extract_first().strip(),
                                     loc.xpath('span[contains(@class, "locality")]/text()').extract_first())

        # description
        ad['description'] = ' '.join(response.xpath(
            '//div[contains(@class, "description")]//text()').extract()).strip()

        # more attributes
        ad['characteristics'] = {}

        for elm in response.xpath('//div[contains(@class, "description")]/following-sibling::h2[@class="title-secondary"]'):
            for entry in elm.xpath('./following-sibling::table[1]//tr'):
                key, value = entry.xpath('td')
                key = key.xpath('text()').extract_first()
                if len(value.xpath('span[contains(@class, "tick")]')) == 1:
                    # checkmark
                    value = True
                else:
                    # text
                    value = value.xpath('text()').extract_first()

                # write to additional data, or to structured field
                try:
                    key = self.settings['KEY_FIGURES'][key]
                    ad[key] = value
                except KeyError:
                    ad['characteristics'][key] = value

        yield ad
