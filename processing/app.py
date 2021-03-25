#a01167425

import os.path
from os import path
import yaml
import connexion
from apscheduler.schedulers.background import BackgroundScheduler
import json
# from base import Base
from connexion import NoContent
from flask_cors import CORS, cross_origin
# from order_request import OrderRequest
# from food_delivery_request import FoodDeliveryRequest
import requests
import logging
import logging.config
import datetime



with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())


with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')



def populate_stats():
    """ Periodically update stats """

    logger.info("Periodic processing has started ")

    # with open('data.json', 'r') as f:
    # #     # log_config = yaml.safe_load(f.read())
    #     data_json = json.load(f)
    #     # print(data_json)
    # #     # logging.config.dictConfig(log_config)
    # #     print(data_json)

        # num_of_customer_ids = data_json['num_of_customer_ids']
        # num_of_order_ids = data_json['num_of_customer_ids']
        # num_of_driver_ids = data_json['num_of_customer_ids']
        # num_of_customer_addresses = data_json['num_of_customer_ids']


    time = str(datetime.datetime.now())
    print(time)
    time = time.replace(" ", "T")
    time = time[:-7] + "Z"


    url1 = app_config['eventstore1']['url']
    url1 = url1 + "?timestamp=" + str(time)


    status_code1 = requests.get(url1)
    print(status_code1)
    status_code1_json = status_code1.json()
    print(status_code1_json, "THIS ONE1")

    if status_code1.status_code != 200:
        logger.error("error " + str(status_code1.status_code))
    else:
        logger.info("received: %d" % len(status_code1_json))

    url2 = app_config['eventstore2']['url']
    url2 = url2 + "?timestamp=" + str(time)

    status_code2 = requests.get(url2)
    print(status_code2)
    print(status_code2.status_code, "THIS IS THEW STATUS CODE 2")
    status_code2_json = status_code2.json()
    print(status_code2_json, "THIS ONE2")

    if status_code2.status_code != 200:
        logger.error("error " + str(status_code2.status_code))
    else:
        logger.info("received: %d" % len(status_code2_json))

    # for i in status_code1_json:
    #     print(i, "AJDBFIAJBDFIAJNBDIFJBNASIHBNGIADBNFGIHSBNDFIGUBNSIDUFG")
    #     num_of_customer_ids += 1
    #     num_of_order_ids += 1
    #
    # for i in status_code2_json:
    #     print(i, '00000000000000000000000000000000000')
    #     num_of_customer_addresses += 1
    #     num_of_driver_ids += 1

    with open('data.json', 'r') as f:
    #     # log_config = yaml.safe_load(f.read())
        data_json = json.load(f)
        num_of_customer_ids = data_json['num_of_customer_ids']
        num_of_order_ids = data_json['num_of_order_ids']
        num_of_driver_ids = data_json['num_of_driver_ids']
        num_of_customer_addresses = data_json['num_of_customer_addresses']
        last_updated = data_json["last_updated"]

    for i in status_code1_json:
        print(i, "AJDBFIAJBDFIAJNBDIFJBNASIHBNGIADBNFGIHSBNDFIGUBNSIDUFG")
        num_of_customer_ids += 1
        num_of_order_ids += 1

    for i in status_code2_json:
        print(i, '00000000000000000000000000000000000')
        num_of_customer_addresses += 1
        num_of_driver_ids += 1

    with open("data.json", "w") as f:
        new_file = {}
        new_file['num_of_customer_ids'] = num_of_customer_ids
        new_file['num_of_order_ids'] = num_of_order_ids
        new_file['num_of_driver_ids'] = num_of_driver_ids
        new_file['num_of_customer_addresses'] = num_of_customer_addresses
        new_file['last_updated'] = time
        json.dump(new_file, f)

    logger.debug(new_file)

    logger.info("Periodic processing has ended. ")


        # print(data_json)
    #     # logging.config.dictConfig(log_config)
    #     print(data_json)

def get_stats():
    logger.info("request has started ")
    if not path.exists('data.json'):
        logger.error("no file")
        return "Statistics do not exist", 404
    else:
        with open('data.json', 'r') as f:
            data_json = json.load(f)
            logger.debug(data_json)

    logger.info("request has completed")
    return data_json, 200


def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
                    'interval',
                    seconds=app_config['scheduler']['period_sec'])
    sched.start()


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml",
            strict_validation=True,
            validate_responses=True)


if __name__ == '__main__':

    init_scheduler()
    app.run(port=8100, use_reloader=False)
