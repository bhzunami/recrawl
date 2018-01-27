# -*- coding: utf-8 -*-

# Scrapy settings for reanalytics project
#
import os
import datetime

BOT_NAME = 'reanalytics'

SPIDER_MODULES = ['reanalytics.spiders']
NEWSPIDER_MODULE = 'reanalytics.spiders'

# OWN SETTINGS:
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://localhost:5432/immo')
#LOG_ENABLED = False
#LOG_LEVEL = 'ERROR'
LOG_STDOUT = True
LOG_LEVEL = "ERROR"

PROXY = os.environ.get('PROXY_URL', 'http://127.0.0.1:8888/?noconnect')
SCRAPOXY_URL = os.environ.get('SCRAPOXY_URL', '127.0.0.1')
SCRAPOXY_PORT = os.environ.get('SCRAPOXY_PORT', 8888)
API_SCRAPOXY = os.environ.get('API_SCRAPOXY', 'http://127.0.0.1:8889/api')
API_SCRAPOXY_PASSWORD = os.environ.get('API_SCRAPOXY_PASSWORD', 'CHANGE_THIS_PASSWORD')
WAIT_FOR_SCALE = int(os.environ.get('WAIT_FOR_SCALE', 5))
WAIT_FOR_START = int(os.environ.get('WAIT_FOR_START', 5))
ADMIN_BASE_URL = 'https://api3.geo.admin.ch/rest/services/api/SearchServer'
SPLASH_URL = os.environ.get('SPLASH_URL', 'http://localhost:8050')

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 4  # Anzahl maximalen gleichzeitigen Anfragen
CONCURRENT_ITEMS = 100

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5  # Wie lange wird gewartet bis zum nächsten request

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
DOWNLOADER_MIDDLEWARES = {
    'reanalytics.middlewares.crawledURLCheck.CrawledURLCheck': 100,
    'scrapoxy.downloadmiddlewares.proxy.ProxyMiddleware': 101,
    'scrapoxy.downloadmiddlewares.wait.WaitMiddleware': 102,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
EXTENSIONS = {
    'reanalytics.extensions.crawlerStats.CrawlerStats': 100,
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
#    'reanalytics.pipelines.jsonWriter.JSONWriterPipeline': 300,
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
    'Bruttomiete (Monat)': 'price_brutto',  # immoscout24
    'Nebenkosten (Monat)': 'additional_costs', # immoscout24
    'Nettomiete (Monat)': 'price_netto', # immoscout24
    'Kaufpreis': 'price_brutto',  # immoscout24
    'Preis Garage': 'additional_costs',  # newhome
    'Preis Abstellplatz': 'additional_costs', # newhome
    'Nettomiete / Monat': 'price_netto', # newhome
    'Nebenkosten / Monat': 'additional_costs', # newhome
    'Miete / Monat': 'price_brutto', # newhome
    'Etage': 'floor',     # homegate, urbanhome
    'Stockwerk': 'floor', # newhome, immoscout24
    'Anzahl Etagen': 'num_floors',  # homegate
    'Etagen im Haus': 'num_floors',  # newhome, urbanhome
    'Anzahl Stockwerke': 'num_floors', # immoscout24
    'Verfügbar': 'available',  # homegate, urbanhome
    'Bezug': 'available',  # newhome
    'Verfügbarkeit': 'available',  # immoscout24
    'Objekttyp': 'objecttype',  # homegate
    'Objektart': 'objecttype', # newhome
    'Zimmer': 'num_rooms',  # homegate, newhome, urbanhome
    'Anzahl Zimmer': 'num_rooms',
    'Wohnfläche': 'living_area',  # homegate, newhome, urbanhome, immoscout24
    'Baujahr': 'build_year',  # homegate, newhome, immoscout24
    'Nutzfläche': 'effective_area', # homegate, immoscout24
    'Kubatur': 'cubature',  # homegate, newhome, immoscout24
    'Raumhöhe': 'room_height',  # homegate
    'Grundstückfläche': 'plot_area',  # homegate, newhome
    'Grundstücksfläche': 'plot_area',  # immoscout24
    'Grundstück': 'plot_area',  # urbanhome
    'Zustand': 'condition',  # newhome
    'Letzte Renovation': 'last_renovation_year',  # homegate, immoscout24
    'Renoviert im Jahr': 'last_renovation_year',  # newhome
    'Immocode' : 'object_id',  # newhome
    'ImmoScout24-Code': 'object_id', # immoscout24
    'Inserate-Nr': 'object_id', # urbanhome
    'Objektnummer': 'reference_no', # newhome
    'Referenz': 'reference_no', # immoscout24
    'Objekt-Referenz': 'reference_no', # urbanhome
    'Qualitätslabel': 'quality_label',  # newhome
}

# Logging configuration
current_time = datetime.datetime.now()

LOGGING_SETTINGS = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        "file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "simple",
            "filename": "logs/log_crawler-{}-{}-{}.log".format(
                current_time.day,
                current_time.month,
                current_time.year),
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["file_handler", "console"]
    },
    "loggers": {
        "scrapy": {
            "level": "INFO",
            "handlers": ["console"],
        },
        "scrapy.core.engine": {
            "level": "INFO",
            "handlers": ["file_handler"],
        },
        "twisted": {
            "level": "ERROR",
            "handlers": ["file_handler"]
        },
        "run": {
            "level": "INFO",
            "handlers": ["console", "file_handler"]
        },
        "reanalytics": {
            "level": "ERROR",
            "handlers": ["console", "file_handler"],
            "propagate": "yes",
        }
    }
}
