# Crawler for real estate

Crawling real estates from switzerland to analyze the market.

## Prerequisites
* Python 3
* Docker / docker-compose
* Amazon AWS Account

## Environment setup
1. Clone the project into a folder `git clone https://github.com/bhzunami/recrawl`
2. Configure the secret environment files:
  * crawler/scrapy.secrets.env
  * crawler/scrapoxy.secerts.env
  * db/database.secrets.env
  * metabase/metabase.secrets.env
  * superset/superset.secrets.env
3. Check the settings.py file in the crawler/reanalytics folder.
4. Build all images with docker `docker-compose build`


Start the application with `docker-compose`:

```shell
docker-compose up -d

docker-compose up -d --force-recreate
```

# Design
TODO

## Setup database locally
To setup the database locally use the script create_database_local.sh located in the db folder. This script creates three new databases, user and inserts some default values. Be careful the script removes existing databases.

The recommended database is postgres but you can use your favorite one.

## Run without docker
Before every crawl you should decide if you want to crawl over the amazon instances as proxy servers or directly from your computer. If you only want to run quick crawling processes it is mostly not neccessairy to setup the proxy instances.

### Disable Amazon proxy instaces
To not use the proxy instances you have to disable the scrapoxy in the settings.py which is located in the crawler/reanalytics folder.
Uncomment the three scaproxy options in the section 'DOWNLOADER_MIDDLEWARES'.
To enable them again remove the comment.

To run the crawler locally without docker you have to set all the necessary environment variables, at least: 
* DATABASE_URL
* DATABASE_NAME
* POSTGRES_ADMIN
* POSTGRES_USER
* POSTGRES_PASSWORD

Then run the script run.py in the crawler folder.

### Run specific crawler
At the moment is not possible to run a specific crawler. But you can change the run.py file and only set the specific crawler.

### Environment files

Every thing that can be configured should be done over an environment file for the docker container.

***scrapy.env***

| Value           | Description   |
| ----------------| ------------- |
| PROXY_URL       | URL to reach the scrapoxy |
| API_SCRAPOXY    | URL to reach the scrapoxy api  |
| WAIT_FOR_SCALE  | How long the scrapy pause when an instance is scaled  |
| WAIT_FOR_START  | How long the scrapy should wait when started up before crawling |

***scrapy.secrets.env***

| Value                   | Description   |
| ------------------------| ------------- |
| DATABASE_URL            | The database url |
| API_SCRAPOXY_PASSWORD   | The password to login to the scrapoxy  |

***scrapoxy.env***

| Value                                     | Description   |
| ----------------------------------------- | ------------- |
| PROVIDERS_AWSEC2_REGION                   | In which region should the proxy server start |
| PROVIDERS_AWSEC2_INSTANCE_INSTANCETYPE    | Which type should be used  |
| PROVIDERS_AWSEC2_INSTANCE_IMAGEID         | The image which should be used when creating the server  |
| PROVIDERS_AWSEC2_INSTANCE_SECURITYGROUPS  | The security groups the machine belongs to |
| PROVIDERS_AWSEC2_MAXRUNNINGINSTANCES      | How many instances can be run at the same time max |
| PROVIDERS_AWSEC2_TAG                      | Tags which are set to the machines |
| INSTANCE_SCALING_MIN                      | How many instances should always run |
| INSTANCE_SCALING_MAX                      | How big is the step to increase the number of instances |
| INSTANCE_AUTORESTART_MINDELAY             | How long can an instance live at minimum |
| INSTANCE_AUTORESTART_MAXDELAY             | How long can an instance live at maximum |

***scrapoxy.secrets.env***

| Value                             | Description   |
| ----------------------------------| ------------- |
| COMMANDER_PASSWORD                | The password for login in to the web interface of scrapoxy |
| PROVIDERS_AWSEC2_ACCESSKEYID      | The amazon access key id  |
| PROVIDERS_AWSEC2_SECRETACCESSKEY  | The amazon secret access key  |

***database.env***

| Value                   | Description   |
| ------------------------| ------------- |
| PGDATA            | Where is the database stored in the filesystem |

***database.secrets.env***

| Value              | Description   |
| -------------------| ------------- |
| POSTGRES_PASSWORD  | Password for the database |
| POSTGRES_USER      | User for the database |
| DATABASE_NAME      | The database name |

#### Amazon EC2

To run scrapoxy on amazon it is suggested to copy an existing AMI to your favorite region.
Suggestet AMI: `eu-west-1 / t2.nano: ami-06220275`.