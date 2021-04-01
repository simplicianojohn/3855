import yaml
import os
import connexion
from connexion import NoContent
import requests
import logging
import logging.config
import datetime
import json
from pykafka import KafkaClient

MAX_EVENTS = 10
EVENT_FILE = "events.json"
LIST = []


#a01167425

# with open('app_conf.yml', 'r') as f:
#     app_config = yaml.safe_load(f.read())


# with open('log_conf.yml', 'r') as f:
#     log_config = yaml.safe_load(f.read())
#     logging.config.dictConfig(log_config)

# logger = logging.getLogger('basicLogger')



if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"

with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())

# External Logging Configuration
with open(log_conf_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)




def delivery_request(body):
    """receives a delivery request"""
    status_code = 201

    client = KafkaClient(hosts='lab6-3855.westus2.cloudapp.azure.com:9092')
    topic = client.topics[str.encode('events')]
    producer = topic.get_sync_producer()
    msg = {"type": "delivery",
           "datetime":
               datetime.datetime.now().strftime(
                   "%Y-%m-%dT%H:%M:%S"),
           "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))


    logger.info("Received event delivery request with a unique id of " + str(body["customer_id"]))
    # status_code = requests.post('http://localhost:8090/requests/delivery', json=body).status_code
    logger.info("Returned event delivery response ID:" + str(body["customer_id"]) + " with status " + str(status_code))
    return NoContent, 201


def add_order(body):
    """receives an order"""
    status_code = 201


    client = KafkaClient(hosts='lab6-3855.westus2.cloudapp.azure.com:9092')
    topic = client.topics[str.encode('events')]
    producer = topic.get_sync_producer()
    msg = {"type": "order",
           "datetime":
               datetime.datetime.now().strftime(
                   "%Y-%m-%dT%H:%M:%S"),
           "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info("Received event order request with a unique id of " + str(body["customer_id"]))
    # status_code = requests.post('http://localhost:8090/requests/order', json=body).status_code

    logger.info("Returned event order response ID:" + str(body["customer_id"]) + " with status " + str(status_code))


    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml",
            strict_validation=True,
            validate_responses=True)


if __name__ == '__main__':
    app.run(port=8080)
