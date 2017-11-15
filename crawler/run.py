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
from scrapy.utils.project import get_project_settings
from scrapoxy.commander import Commander
from threading import Thread
from models import Advertisement
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pdb

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
        crawl_thread = Crawlers(process=process, spiders=[Homegate, Newhome])
        crawl_thread.start()
        rounds = 0
        while crawl_thread.is_alive():
            if rounds == (5*12):
                logging.info("Run into time out")
                break
            time.sleep(5)
            rounds += 1

        logging.debug("Stopping all crawlers..")
        process.stop()
        #process.join()
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
    app = App()
    app.prepare_instances()
    app.runCrawlers()
    app.shutdown_instances()

if __name__ == "__main__":
    # Prepare log system, do not use scrpay as root logger 
    configure_logging(install_root_handler=False)
    current_time = datetime.datetime.now()
    if not os.path.isdir('logs'):
        os.mkdir('logs')
    
    logging.basicConfig(
        filename='logs/log_crawler-{}-{}-{}_{}:{}:{}.log'.format(
            current_time.day,
            current_time.month,
            current_time.year,
            current_time.hour,
            current_time.minute,
            current_time.second
        ),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG
    )
    logging.getLogger().addHandler(logging.StreamHandler())
    main()

