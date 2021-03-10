import sensors_pack.humidity_pack.dht22 as dht22
import json

from time import sleep
from elasticsearch import Elasticsearch
from datetime import date
from datetime import datetime
from veggie_utils import *
from elastic_utils import es_connect

with open('config.json') as json_file:
    conf = json.load(json_file)

override_conf_from_env_array(conf, 'elastic_hosts')
override_conf_from_env(conf, 'log_level')
override_conf_from_env(conf, 'pin')
override_conf_from_env(conf, 'elastic_port')
override_conf_from_env(conf, 'elastic_scheme')
override_conf_from_env(conf, 'elastic_subpath')
override_conf_from_env(conf, 'elastic_username')
override_conf_from_env(conf, 'elastic_password')
override_conf_from_env(conf, 'wait_time')
override_conf_from_env(conf, 'index_prefix')

LOG_LEVEL = conf['log_level']
ES_HOSTS = conf['elastic_hosts']
ES_SUBPATH = conf['elastic_subpath']
ES_PORT = int(conf['elastic_port'])
ES_USER = conf['elastic_username']
ES_PASS = conf['elastic_password']
ES_SCHEME = conf['elastic_scheme']
INDEX_PREFIX = conf['index_prefix']
WAIT_TIME = cast_int(conf['wait_time'])
DATA_PIN = conf['pin']

es = es_connect(LOG_LEVEL, ES_SCHEME, ES_HOSTS, ES_PORT, ES_USER, ES_PASS, ES_SUBPATH)

while True:
    index_name = "{}_{}".format(INDEX_PREFIX, date.today().strftime("%Y%m%d"));
    es.indices.create(index=index_name, ignore=400)

    humid, temp = dht22.read_humidity_and_temperature(DATA_PIN)
    if humid is not None and temp is not None:
        log_msg(LOG_LEVEL, "info", "Temperature={0:0.1f}*C Humidity={1:0.1f}%".format(temp, humid))
        timestamp = datetime.now()
        es.index(index=index_name, id=timestamp, body={"temperature": temp, "humidity": humid, "timestamp": timestamp})
    else:
        log_msg("error", "Failed to retrieve values...")
    sleep(WAIT_TIME)
