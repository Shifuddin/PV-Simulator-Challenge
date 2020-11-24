"""
This is the entry script for Meter producer
"""
__author__ = 'Md Shifuddin Al Masud'
__email__ = 'shifuddin.masud@gmail.com'
__license__ = 'MIT License'

from meter.Meter import Meter
import random
import logging
import os
from aio_pika.exceptions import AMQPConnectionError
import asyncio
from meter.RabbitMQAsyncBroker import RabbitMQAsyncBroker
import time


async def main():
    try:
        # configure logging
        logging.basicConfig(filename="./log/producer.txt", filemode="a", level=logging.INFO,
                            format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

        # read values from environment
        broker_address = os.environ['broker_address']
        broker_queue_name = os.environ['broker_msg_queue']
        min_pv = int(os.environ['min_pv'])
        max_pv = int(os.environ['max_pv'])
        publishing_interval_seconds = int(os.environ['publishing_interval_seconds'])
        initial_sleep_for_broker = int(os.environ['initial_sleep'])

        logging.info("Broker address: %s, Message Queue: %s, Min_PV: %s Max_PV: %s Publish Interval (Second): %s",
                     broker_address, broker_queue_name, min_pv, max_pv, publishing_interval_seconds)
        broker = RabbitMQAsyncBroker(broker_address=broker_address, broker_queue_name=broker_queue_name)
        meter = Meter(broker=broker, min_power_value=min_pv,
                      max_power_value=max_pv, power_value_generator=lambda x, y: random.randrange(x, y))
        try:
            # initial sleep for the broker to be ready
            time.sleep(initial_sleep_for_broker)
            # connect with broker
            await meter.connect_with_broker()
            # start publishing
            await meter.start_publishing(producing_interval_seconds=publishing_interval_seconds)
        except KeyboardInterrupt as key:
            logging.error("Producer(Meter) stopped: " + key.__str__())
        except AMQPConnectionError as amp:
            logging.error("Connection Error: ", amp)
        except Exception as error:
            logging.error("[Startup Error] Cannot start producer(Meter): ", error)

        finally:
            if meter is not None:
                # close connection to the broker
                try:
                    await meter.close_connection()
                except AttributeError as ae:
                    logging.error("Meter is closed before successful connection to the broker", ae.__str__().__str__())
    except KeyError as key_err:
        logging.error("[Startup Error] Unable to find env variable : " + key_err.__str__())
    except ValueError as value_err:
        logging.error("[Startup Error] Value Error.", value_err)
    except TypeError as te:
        logging.error("[Startup Error] ", te)


if __name__ == "__main__":
    asyncio.run(main())
