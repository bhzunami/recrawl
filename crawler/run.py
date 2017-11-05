import time
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
from reanalytics.spiders.homegate import Homegate
from scrapy.utils.project import get_project_settings
from scrapoxy.commander import Commander
from threading import Thread
import pdb

class Crawlers(Thread):
    def __init__(self, process, crawlers):
        Thread.__init__(self)
        self.process = process
        self.crawlers = crawlers

    def run(self):
        for crawler in self.crawlers:
            self.process.crawl(crawler)
        self.process.start()


def start_instances():
    pass


def main():
    settings = get_project_settings()
    commander = Commander(settings.get('API_SCRAPOXY'),
                          settings.get('API_SCRAPOXY_PASSWORD'))
    min_sc, required_sc, max_sc = commander.get_scaling()
    required_sc = max_sc
    commander.update_scaling(min_sc, required_sc, max_sc)
    time.sleep(settings.get('WAIT_FOR_SCALE'))

    process = CrawlerProcess(settings)
    crawl_thread = Crawlers(process=process, crawlers=[Homegate])
    crawl_thread.start()

    for i in range(180):
        logging.info("Crawler stas:")
        for crawler in process.crawlers:
            logging.info(crawler.spider.name)
            logging.info(crawler.stats.get_stats())
        time.sleep(60)    
    process.stop()

    commander.update_scaling(min_sc, 0, max_sc)

if __name__ == "__main__":
    pdb.set_trace()
    main()
