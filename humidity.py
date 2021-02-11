import sensors_pack.humidity_pack.dht22 as dht22
import json

from time import sleep
from elasticsearch import Elasticsearch
from datetime import date
from datetime import datetime

with open('humidity_conf.json') as json_file:
    conf = json.load(json_file)
    DATA_PIN = conf['pin']
    ES_HOST = conf['elastic_host']
    ES_PORT = conf['elastic_port']
    ES_SCHEME = conf['elastic_scheme']
    ES_URL = "{}://{}:{}".format(ES_SCHEME, ES_HOST, ES_PORT)
    WAIT_TIME = conf['wait_time']
    INDEX_PREFIX = conf['index_prefix']

es = Elasticsearch(ES_URL)

while True:
    index_name = "{}_{}".format(INDEX_PREFIX, date.today().strftime("%Y%m%d"));
    es.indices.create(index=index_name, ignore=400)

    humid, temp = dht22.read_humidity_and_temperature(DATA_PIN)
    if humid is not None and temp is not None:
        print("Temperature={0:0.1f}*C Humidity={1:0.1f}%".format(temp, humid))
        timestamp = datetime.now()
        es.index(index=index_name, id=timestamp, body={"temperature": temp, "humidity": humid, "timestamp": timestamp})
    else:
        print("Failed to retrieve values...")
    sleep(WAIT_TIME)
