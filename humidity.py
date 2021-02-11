import sensors_pack.humidity_pack.dht22 as dht22
import json

from time import sleep
from elasticsearch import Elasticsearch
from datetime import date
from datetime import datetime

def is_not_empty ( var ):
    return var is not None and "" != var and "null" != var and "nil" != var

def is_empty ( var ):
    return not is_not_empty(var)

def override_conf_from_env( conf, key ):
    env_key = "VEGGIEPI_{}".format(key)
    if os.environ.get(env_key) is not None:
        conf[key] = os.environ[env_key]
    elif not key in conf:
        conf[key] = "nil"

def override_conf_from_env_array( conf, key ):
    env_key = "VEGGIEPI_{}".format(key)
    if os.environ.get(env_key) is not None:
        if is_empty(os.environ[env_key]):
            conf[key] = []
        else:
            conf[key] = os.environ[env_key].split(",")

def check_log_level ( log_level ):
    if LOG_LEVEL == "debug" or LOG_LEVEL == "DEBUG":
        return True
    else:
        return log_level != "debug" and log_level != "DEBUG"

def log_msg ( log_level, message ):
    if check_log_level(log_level):
        print ("[{}] {}".format(log_level, message))

with open('humidity_conf.json') as json_file:
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
WAIT_TIME = conf['wait_time']
DATA_PIN = conf['pin']

if is_not_empty(ES_USER) and is_not_empty(ES_PASS) and is_not_empty(ES_SUBPATH):
    es_url_tpl = "{}://{}:{}@{}:{}/{}"
    es_url = es_url_tpl.format(ES_SCHEME, ES_USER, "{}", ES_HOSTS[0], ES_PORT, ES_SUBPATH)
    log_msg("debug", "Connect to elastic search with url = {}".format(es_url.format("XXXXXX")))
    es = Elasticsearch([es_url.format(ES_PASS)], http_auth=(ES_USER, ES_PASS))
elif is_not_empty(ES_USER) and is_not_empty(ES_PASS):
    es_url_tpl = "{}://{}:{}"
    es_url = es_url_tpl.format(ES_SCHEME, ES_HOSTS[0], ES_PORT)
    log_msg("debug", "Connect to elastic search with url = {} and username = {}".format(es_url, ES_USER))
    es = Elasticsearch(ES_HOSTS, http_auth=(ES_USER, ES_PASS), scheme = ES_SCHEME, port = ES_PORT)
elif is_not_empty(ES_SUBPATH):
    es_url_tpl = "{}://{}:{}/{}"
    es_url = es_url_tpl.format(ES_SCHEME, ES_HOSTS[0], ES_PORT, ES_SUBPATH)
    log_msg("debug", "Connect to elastic search with url = {}".format(es_url))
    es = Elasticsearch([es_url])
else:
    es_url_tpl = "{}://{}:{}"
    es_url = es_url_tpl.format(ES_SCHEME, ES_HOSTS[0], ES_PORT)
    log_msg("debug", "Connect to elastic search with url = {}".format(es_url))
    es = Elasticsearch(ES_HOSTS, scheme = ES_SCHEME, port = ES_PORT)

while True:
    index_name = "{}_{}".format(INDEX_PREFIX, date.today().strftime("%Y%m%d"));
    es.indices.create(index=index_name, ignore=400)

    humid, temp = dht22.read_humidity_and_temperature(DATA_PIN)
    if humid is not None and temp is not None:
        log_msg("info", "Temperature={0:0.1f}*C Humidity={1:0.1f}%".format(temp, humid))
        timestamp = datetime.now()
        es.index(index=index_name, id=timestamp, body={"temperature": temp, "humidity": humid, "timestamp": timestamp})
    else:
        log_msg("error", "Failed to retrieve values...")
    sleep(WAIT_TIME)
