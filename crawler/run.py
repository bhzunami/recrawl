
"""
https://github.com/fabienvauchelles/scrapoxy-python-api/blob/master/scrapoxy/downloadmiddlewares/scale.py

https://github.com/fabienvauchelles/scrapoxy-python-api/blob/master/scrapoxy/commander.py
"""
import time
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
from reanalytics.spiders.homegate import Homegate
from reanalytics.spiders.newhome import Newhome
from scrapy.utils.project import get_project_settings
from scrapoxy.commander import Commander
from threading import Thread
import pdb

# logging.basicConfig(level=logging.ERROR)
# logger = logging.getLogger(__name__)

class Crawlers(Thread):
    def __init__(self, process, spiders):
        Thread.__init__(self)
        self.process = process
        self.spiders = spiders

    def run(self):
        for spider in self.spiders:
            #crawler = self.process.create_crawler(spider)
            #logging.info("Set Name: {}".format(spider.name))
            #crawler.stats.set_value('spider', spider.name)
            ##self.process.crawlers.add(crawler)
            self.process.crawl(spider)

        self.process.start()
        # logging.debug("Finish with crawler thread")


def start_instances():
    pass


def main():
    settings = get_project_settings()
    commander = Commander(settings.get('API_SCRAPOXY'),
                          settings.get('API_SCRAPOXY_PASSWORD'))
    min_sc, required_sc, max_sc = commander.get_scaling()
    required_sc = max_sc
    commander.update_scaling(min_sc, required_sc, max_sc)
    wait_for_scale = settings.get('WAIT_FOR_SCALE')
    # logger.info("Started up instances. wait {} seconds to start crawling".format(wait_for_scale))
    time.sleep(wait_for_scale)

    process = CrawlerProcess(settings)
    crawl_thread = Crawlers(process=process, spiders=[Homegate, Newhome])
    crawl_thread.start()
    rounds = 0
    while crawl_thread.is_alive():
        # logger.info("Round {}".format(rounds))
        print("Round {}".format(rounds))
        if rounds == 10:
            break
        time.sleep(5)
        rounds += 1

    # logger.debug("Stopping all crawlers..")
    process.stop()
    #process.join()
    # logger.info("Send stop signal to all crawlers..")
    while crawl_thread.is_alive():
        # logger.debug("Wait for crawlers to clean up...")
        print("Wait for crawlers to clean up...")
        time.sleep(5)
    
    # logger.info("Set instances to 0")
    commander.update_scaling(min_sc, 0, max_sc)


    print("Everything closed now its time to show some stats:")
    import pdb
    pdb.set_trace()
    for crawler in process.crawlers:
        print("Stats for crawler")
        print("{}".format(crawler.stats.get_stats()))

if __name__ == "__main__":
    main()

