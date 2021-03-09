# Humidity and temperature sensor

This project aims to collect the data from a humidity and temperature sensor plugged in a raspberrypi and index those data into Elasticsearch and make some alerts with elastalert.

The elasticstack images used are available [here](https://gitlab.comwork.io/oss/elasticstack/elasticstack-arm) in opensource too.

This project is used by the [veggiepi.com](https://www.veggiepi.com) project.

## Table of content

[[_TOC_]]

## Git repository

* Main repo: https://gitlab.comwork.io/oss/veggiepi/humidity_and_temperature
* Github mirror backup: https://github.com/idrissneumann/rpi_humidity_and_temperature
* Gitlab mirror backup: https://gitlab.com/ineumann/rpi_humidity_and_temperature

## Run locally using docker-compose

Pick the [docker-compose.yml](./docker-compose.yml) file and follow the steps below.

### Run elasticsearch

```shell
$ docker-compose up -d es01
```

Then wait until it answer on the 9200 port (you can check the logs with `docker logs veggie_es01`):

```shell
$ curl localhost:9200
{
  "name" : "elasticsearch",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "v22OI4ILQZ-xfmlArtmHUw",
  "version" : {
    "number" : "7.10.2",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "747e1cc71def077253878a59143c1f785afa92b9",
    "build_date" : "2021-01-13T00:42:12.435326Z",
    "build_snapshot" : false,
    "lucene_version" : "8.7.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

### Run Kibana

```shell
$ docker-compose up -d kib01
```

Then wait until the UI of Kibana is loading on http://127.0.0.1:5601 (you can change the ip by your local network ip if you want to load the Kibana UI from another computer and you can check the logs with `docker logs veggie_kib01`).

### Run the service

```shell
$ docker-compose up -d vhat01
```

Then you can check the logs with `docker logs veggie_vhat01` and check the data on Kibana!
