"""
This class takes care of Async Communication with RabbitMQ broker.
"""
__author__ = 'Md Shifuddin Al Masud'
__email__ = 'shifuddin.masud@gmail.com'
__license__ = 'MIT License'

from meter.Broker import Broker
from aio_pika import connect, Message
import logging


class RabbitMQAsyncBroker(Broker):

    __connection = object
    __channel = object
    __broker_queue = object

    def __init__(self, broker_address: str, broker_queue_name: str):
        """

        :param broker_address:
        :param broker_queue_name:
        """
        # initialize broker properties
        self.__broker_address = broker_address
        self.__broker_queue_name = broker_queue_name
        logging.info("Broker address: %s and Queue %s set",  broker_address, broker_queue_name)

    async def connect_to_server(self):
        # Perform connection
        self.__connection = await connect(self.__broker_address)

        # Creating a channel
        self.__channel = await self.__connection.channel()

        # Declaring queue
        self.__broker_queue = await self.__channel.declare_queue(self.__broker_queue_name)
        logging.info("Connection to server: %s achieved.", self.__broker_address)

    async def publish(self, message: str):
        logging.debug("Publishing %s", message)
        await self.__channel.default_exchange.publish(
            Message(message.encode('utf-8')),
            routing_key=self.__broker_queue_name
        )

    async def register_consumer(self, consumer):
        await self.__broker_queue.consume(consumer.on_message, no_ack=True)
        logging.info("%s is registered as consumer", consumer.__str__())

    async def close_connection(self):
        await self.__connection.close()
        logging.info("Connection to server closed.")


