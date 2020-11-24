"""
This test class verifies method of Meter class.
"""
__author__ = 'Md Shifuddin Al Masud'
__email__ = 'shifuddin.masud@gmail.com'
__license__ = 'MIT License'

import unittest
from meter.Meter import Meter
from aio_pika.exceptions import AMQPConnectionError
from meter.Broker import Broker
import asyncio


class DummyBroker(Broker):
    connect_to_server_invoked = False
    publish_called = False
    close_connection_invoked = False

    def __init__(self, broker_address: str, broker_queue_name: str):
        self.__broker_address = broker_address
        self.__broker_queue = broker_queue_name

    async def connect_to_server(self):
        self.connect_to_server_invoked = True

    async def publish(self, value: str):
        self.publish_called = True

    async def close_connection(self):
        self.close_connection_invoked = True


class TestHomeMeter(unittest.TestCase):
    __min_power_value = 0
    __max_power_value = 10
    __power_value = 3
    __broker_address = "does not matter"
    __broker_queue_name = "does not matter"

    def test_generate_power_value_when_power_value_in_range(self):
        """
        Tests generate_power_value() when power value
        is within min-max range
        :return:
        """
        dummy_broker = DummyBroker(self.__broker_address, self.__broker_queue_name)
        meter = Meter(broker=dummy_broker, min_power_value=self.__min_power_value, max_power_value=self.__max_power_value,
                      power_value_generator=lambda x, y: self.__power_value)
        self.assertEqual(meter.generate_power_value(), self.__power_value)
        self.assertTrue(meter.generate_power_value() in range(int(self.__min_power_value),
                                                              int(self.__max_power_value) + 1))

    def test_generate_power_value_when_power_value_out_of_range(self):
        """
        Tests generate_power_value() when power value
        is outside of min-max range
        :return:
        """
        self.__power_value = 50
        dummy_broker = DummyBroker(self.__broker_address, self.__broker_queue_name)
        meter = Meter(broker=dummy_broker, min_power_value=self.__min_power_value, max_power_value=self.__max_power_value,
                      power_value_generator=lambda x, y: self.__power_value)
        self.assertEqual(meter.generate_power_value(), -1)
        self.assertFalse(meter.generate_power_value() in range(int(self.__min_power_value),
                                                               int(self.__max_power_value) + 1))

    def test_connect_with_broker(self):
        """
        Tests connection with broker
        :return:
        """
        dummy_broker = DummyBroker(self.__broker_address, self.__broker_queue_name)
        meter = Meter(broker=dummy_broker, min_power_value=self.__min_power_value, max_power_value=self.__max_power_value,
                      power_value_generator=lambda x, y: self.__power_value)
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(meter.connect_with_broker())
            self.assertTrue(dummy_broker.connect_to_server_invoked)
        except AMQPConnectionError as ae:
            self.assertTrue(False)

    def test_close_connection(self):
        """
        Tests close connection
        :return:
        """
        dummy_broker = DummyBroker(self.__broker_address, self.__broker_queue_name)
        meter = Meter(broker=dummy_broker, min_power_value=self.__min_power_value, max_power_value=self.__max_power_value,
                      power_value_generator=lambda x, y: self.__power_value)
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(meter.close_connection())
            self.assertTrue(dummy_broker.close_connection_invoked)
        except AttributeError as ae:
            self.assertEqual(ae.__str__(), "type object 'object' has no attribute 'close'")

    def test_publish_power_message(self):
        """
        Tests publish power value
        :return:
        """
        dummy_broker = DummyBroker(self.__broker_address, self.__broker_queue_name)
        meter = Meter(broker=dummy_broker, min_power_value=self.__min_power_value, max_power_value=self.__max_power_value,
                      power_value_generator=lambda x, y: self.__power_value)
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(meter.publish_message(self.__power_value))
            self.assertTrue(dummy_broker.publish_called)
        except Exception:
            self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()
