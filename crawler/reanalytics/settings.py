# -*- coding: utf-8 -*-

# Scrapy settings for reanalytics project
#

import os

BOT_NAME = 'reanalytics'

SPIDER_MODULES = ['reanalytics.spiders']
NEWSPIDER_MODULE = 'reanalytics.spiders'

# OWN SETTINGS:
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://localhost:5432/immo')
LOG_ENABLED = True
LOG_LEVEL = 'INFO'

PROXY = os.environ.get('PROXY', 'http://127.0.0.1:8888/?noconnect') 
API_SCRAPOXY = os.environ.get('API_SCRAPOXY', 'http://127.0.0.1:8889/api')
API_SCRAPOXY_PASSWORD = os.environ.get('API_SCRAPOXY_PASSWORD', 'CHANGE_THIS_PASSWORD')
WAIT_FOR_SCALE = os.environ.get('WAIT_FOR_SCALE', 5)
WAIT_FOR_START = os.environ.get('WAIT_FOR_START', 5)
ADMIN_BASE_URL = 'https://api3.geo.admin.ch/rest/services/api/SearchServer'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 10
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'reanalytics.middlewares.crawledURLCheck.CrawledURLCheck': 100,
#    'scrapoxy.downloadmiddlewares.proxy.ProxyMiddleware': 101,
#    'scrapoxy.downloadmiddlewares.wait.WaitMiddleware': 102,
#    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
EXTENSIONS = {
    'reanalytics.extensions.simpleStatsextension.SimpleStats': 100,
#    'scrapy.extensions.telnet.TelnetConsole': None,
}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'reanalytics.pipelines.municipalityFinder.MunicipalityFinderPipeline': 110,
    'reanalytics.pipelines.objectTypeFinder.ObjectTypeFinderPipeline': 120,
    'reanalytics.pipelines.duplicateCheck.DuplicateCheckPipeline': 130,
    'reanalytics.pipelines.coordinates.CoordinatesPipeline': 140,
    'reanalytics.pipelines.databaseWriter.DatabaseWriterPipeline': 200,
    # 'reanalytics.pipelines.jsonWriter.JSONWriterPipeline': 300,
}


# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# FIELDS
KEY_FIGURES = {
    'Verkaufspreis': 'price_brutto',  # homegate, immoscout24
    'Preis': 'price_brutto',  # newhome
    'Kaufpreis': 'price_brutto',  # immoscout24
    'Preis Garage': 'additional_costs',  # newhome
    'Preis Abstellplatz': 'additional_costs', # newhome
    'Etage': 'floor',     # homegate, urbanhome
    'Stockwerk': 'floor', # newhome, immoscout24
    'Anzahl Etagen': 'num_floors',  # homegate
    'Etagen im Haus': 'num_floors',  # newhome, urbanhome
    'Anzahl Etagen des Objektes': 'num_floors', # immoscout24
    'Verfügbar': 'available',  # homegate, urbanhome
    'Bezug': 'available',  # newhome
    'Objekttyp': 'objecttype',  # homegate
    'Objektart': 'objecttype', # newhome
    'Zimmer': 'num_rooms',  # homegate, newhome, urbanhome
    'Anzahl Zimmer': 'num_rooms',
    'Wohnfläche': 'living_area',  # homegate, newhome, urbanhome
    'Baujahr': 'build_year',  # homegate, newhome, immoscout24
    'Nutzfläche': 'effective_area', # homegate, immoscout24
    'Kubatur': 'cubature',  # homegate, newhome, immoscout24
    'Raumhöhe': 'room_height',  # homegate
    'Grundstückfläche': 'plot_area',  # homegate, newhome, immoscout24
    'Grundstück': 'plot_area',  # urbanhome
    'Zustand': 'condition',  # newhome
    'Letzte Renovation': 'last_renovation_year',  # homegate
    'Renoviert im Jahr': 'last_renovation_year',  # newhome
    'Letztes Renovationsjahr': 'last_renovation_year', # immoscout24
    'Immocode' : 'object_id',  # newhome
    'ImmoScout24-Code': 'object_id', # immoscout24
    'Inserate-Nr': 'object_id', # urbanhome
    'Objektnummer': 'reference_no', # newhome
    'Referenz': 'reference_no', # immoscout24
    'Objekt-Referenz': 'reference_no', # urbanhome
    'Qualitätslabel': 'quality_label',  # newhome
}
