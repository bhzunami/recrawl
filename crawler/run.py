# -*- coding: utf-8 -*-
"""
https://github.com/fabienvauchelles/scrapoxy-python-api/blob/master/scrapoxy/downloadmiddlewares/scale.py

https://github.com/fabienvauchelles/scrapoxy-python-api/blob/master/scrapoxy/commander.py
"""
import time
import os
import datetime
import logging
import csv
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from reanalytics.spiders.homegate import Homegate
from reanalytics.spiders.newhome import Newhome
from reanalytics.spiders.immoscout24 import Immoscout24

from scrapy.utils.project import get_project_settings
from scrapoxy.commander import Commander
from threading import Thread
from models import Advertisement
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pdb

# Prepare log system, do not use scrpay as root logger 
current_time = datetime.datetime.now()
if not os.path.isdir('logs'):
    os.mkdir('logs')

SETTINGS = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        '': {
            'level': 'ERROR',
            'propagate': True,
        },
        'scrapy': {
            'level': 'WARN',
        },
        'twisted': {
            'level': 'ERROR',
        },
        'run': {
            'level': 'INFO',
        },
        'reanalytics.middlewares.crawledURLCheck': {
            'level': 'INFO',
        }, 
        'reanalytics': {
            'level': 'ERROR',
        }
    }
}
# logging.basicConfig(
#     filename='logs/log_crawler-{}-{}-{}.log'.format(
#         current_time.day,
#         current_time.month,
#         current_time.year
#     ),
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     level=logging.INFO
# )
# logger = logging.getLogger("run")

class Crawlers(Thread):
    def __init__(self, process, spiders):
        Thread.__init__(self)
        self.process = process
        self.spiders = spiders

    def run(self):
        for spider in self.spiders:
            self.process.crawl(spider)

        self.process.start()
        logging.debug("Finish with crawler thread")

class App(object):
    def __init__(self):
        self.settings = get_project_settings()
        self.commander = Commander(self.settings.get('API_SCRAPOXY'),
                                   self.settings.get('API_SCRAPOXY_PASSWORD'))

    
    def prepare_instances(self):
        if len(self.settings.get('DOWNLOADER_MIDDLEWARES', {})) <= 1:
            logging.info("Do not run crawler over proxy")
            return
        min_sc, required_sc, max_sc = self.commander.get_scaling()
        required_sc = max_sc
        self.commander.update_scaling(min_sc, required_sc, max_sc)
        wait_for_scale = self.settings.get('WAIT_FOR_SCALE')
        time.sleep(wait_for_scale)


    def runCrawlers(self):
        process = CrawlerProcess(self.settings)
        crawl_thread = Crawlers(process=process, spiders=[Homegate, Newhome, Immoscout24])
        crawl_thread.start()
        rounds = 0
        while crawl_thread.is_alive():
            if rounds == (4320):  # 4320*10(sleep) = 12h
                logging.info("Run into time out")
                break
            rounds += 1
            time.sleep(10)

        logging.debug("Stopping all crawlers..")
        process.stop()
        while crawl_thread.is_alive():
            logging.debug("Wait for crawlers to clean up...")
            time.sleep(5)

    def shutdown_instances(self):
        if len(self.settings.get('DOWNLOADER_MIDDLEWARES', {})) <= 1:
            logging.info("Nothing to stop, because no instances were started")
            return
        min_sc, required_sc, max_sc = self.commander.get_scaling()
        self.commander.update_scaling(min_sc, 0, max_sc)

    def getCrawledData(self):
        engine = create_engine(self.settings.get('DATABASE_URL'))
        Session = sessionmaker(bind=engine, expire_on_commit=True)
        session = Session()
        from_time = datetime.datetime.now() - datetime.timedelta(days=1)
        ads = session.query(Advertisement).filter(Advertisement.last_seen >= from_time).all()
        with open("crawled_ads.csv", "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow([column.key for column in Advertisement.__table__.columns])
            for ad in ads:
                csvwriter.writerow(list(ad))
        print(len(ads))

def main():
    # Wait 5 seconds until all containers are started
    time.sleep(5)
    configure_logging(SETTINGS, install_root_handler=False)
    app = App()
    app.prepare_instances()
    app.runCrawlers()
    app.shutdown_instances()

if __name__ == "__main__":
    main()
