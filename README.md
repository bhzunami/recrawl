# Crawler for real estate

Start the application with `docker-compose`:

```shell
docker-compuse up -d
```

Every container needs his own environment variables which are set in the *.env files:

## Environment files

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

## Amazon EC2

To run scrapoxy on amazon it is suggested to copy an existing AMI to your favorite region.
Suggestet AMI: `eu-west-1 / t2.nano: ami-06220275`.