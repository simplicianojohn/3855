#a01167425

import os
import yaml
import connexion
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from connexion import NoContent
from order_request import OrderRequest
from food_delivery_request import FoodDeliveryRequest
import requests
import logging
import logging.config
import datetime

from pykafka import KafkaClient
import json
from pykafka.common import OffsetType
from threading import Thread


# DB_ENGINE = create_engine("mysql+pymysql://root:Password@localhost:3306/events")
#
# Base.metadata.bind = DB_ENGINE
# DB_SESSION = sessionmaker(bind=DB_ENGINE)

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




DB_ENGINE = create_engine('mysql+pymysql://' + app_config['datastore']['user'] + ':' +
                          app_config['datastore']['password'] + '@' +app_config['datastore']['hostname'] +
                          ':' + str(app_config['datastore']['port']) + '/' + app_config['datastore']['db'])

Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def process_messages():
    """ Process event messages """
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    # Create a consume on a consumer group, that only reads new messages
    # (uncommitted messages) when the service re-starts (i.e., it doesn't
    # read all the old messages from the history in the message queue).
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',
                                         reset_offset_on_start=False,
                                         auto_offset_reset=OffsetType.LATEST)
    # This is blocking - it will wait for a new message
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        payload = msg["payload"]
        if msg["type"] == "delivery":  # Change this to your event type
            delivery_request(payload)
        elif msg["type"] == "order":  # Change this to your event type
            add_order(payload)
        # Commit the new message as being read
    consumer.commit_offsets()




def delivery_request(body):
    """receives a delivery request"""

    session = DB_SESSION()

    fdr = FoodDeliveryRequest(body['customer_id'],
                              body['driver_id'],
                              body['customer_address'],
                              body['order_id'])

    session.add(fdr)

    session.commit()
    session.close()


    logger.debug("Received event delivery request with a unique id of " + str(body["customer_id"]))
    return NoContent, 201

def get_delivery_request(timestamp):
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    print(timestamp_datetime)
    readings = session.query(FoodDeliveryRequest).filter(FoodDeliveryRequest.date_created >= timestamp_datetime)
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for delivery requests after %s returns %d results" % (timestamp, len(results_list)))
    return results_list, 200

def add_order(body):
    """receives an order"""


    session = DB_SESSION()

    order = OrderRequest(body['customer_id'],
                         body['order_id'],
                         body['date'])

    session.add(order)

    session.commit()
    session.close()


    logger.debug("Received event order request with a unique id of " + str(body["customer_id"]))
    return NoContent, 201


def get_order_request(timestamp):
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    print(timestamp_datetime)
    readings = session.query(OrderRequest).filter(OrderRequest.date_created >= timestamp_datetime)
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for order requests after %s returns %d results" % (timestamp, len(results_list)))
    return results_list, 200

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml",
            strict_validation=True,
            validate_responses=True)


if __name__ == '__main__':
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    logger.info("Hostname: " + str(app_config['datastore']['hostname']) + " Port: " + str(app_config['datastore']['port']))
    app.run(port=8090)

