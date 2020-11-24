"""
This class contains all the test cases for RabbitMQAsyncBroker
Test results of this class depends on whether rabbitmq is running on localhost or not.
"""
__author__ = 'Md Shifuddin Al Masud'
__email__ = 'shifuddin.masud@gmail.com'
__license__ = 'MIT License'

import unittest
from pv_simulator.RabbitMQAsyncBroker import RabbitMQAsyncBroker
import asyncio
from pv_simulator.Consumer import Consumer
from aio_pika import IncomingMessage


class TestRabbitMQAsyncBroker(unittest.TestCase):
    __broker_address = "amqp://guest:guest@localhost"
    __broker_queue_name = "pv"
    __message = "Hi There"

    def test_connect_to_server(self):
        rabbitmq = RabbitMQAsyncBroker(self.__broker_address, self.__broker_queue_name)
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(rabbitmq.connect_to_server())
            self.assertTrue(True)
        except ConnectionError:
            self.assertTrue(False)

    def test_publish(self):
        rabbitmq = RabbitMQAsyncBroker(self.__broker_address, self.__broker_queue_name)

        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(rabbitmq.connect_to_server())
            loop.run_until_complete(rabbitmq.publish(self.__message))
            self.assertTrue(True)
        except Exception:
            self.assertTrue(False)

    def test_publish_without_connection(self):
        rabbitmq = RabbitMQAsyncBroker(self.__broker_address, self.__broker_queue_name)

        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(rabbitmq.publish(self.__message))
            self.assertTrue(False)
        except AttributeError:
            self.assertTrue(True)

    def test_close_connection(self):
        rabbitmq = RabbitMQAsyncBroker(self.__broker_address, self.__broker_queue_name)

        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(rabbitmq.connect_to_server())
            loop.run_until_complete(rabbitmq.close_connection())
            self.assertTrue(True)
        except Exception:
            self.assertTrue(False)

    def test_close_connection_without_connection(self):
        rabbitmq = RabbitMQAsyncBroker(self.__broker_address, self.__broker_queue_name)

        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(rabbitmq.close_connection())
            self.assertTrue(False)
        except AttributeError:
            self.assertTrue(True)

    def test_register_consumer(self):
        dummy_consumer = DummyConsumer()
        rabbitmq = RabbitMQAsyncBroker(self.__broker_address, self.__broker_queue_name)
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(rabbitmq.connect_to_server())
            loop.run_until_complete( rabbitmq.register_consumer(dummy_consumer))
            loop.close()
            self.assertTrue(dummy_consumer.callback_executed)
        except AttributeError:
            self.assertTrue(False)


class DummyConsumer(Consumer):
    callback_executed = False

    async def on_message(self, message: IncomingMessage):
        self.callback_executed = True

