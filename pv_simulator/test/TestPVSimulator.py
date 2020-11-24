"""
This test class verifies method of PVSimulator class.
"""

import unittest
from pv_simulator.PVSimulator import PVSimulator
from pv_simulator.FileWriter import FileWriter
from pv_simulator.Broker import Broker
from pv_simulator.Consumer import Consumer
import asyncio
import datetime
from aio_pika.exceptions import AMQPConnectionError
from aio_pika import Message


class TestHomePVSimulator(unittest.TestCase):
    __meter_power_value = 3
    __min_power_value = 0
    __max_power_value = 10
    __simulated_power_value = 4
    __combined_power_value = 7
    __broker_address = "does not matter"
    __broker_queue_name = "does not matter"

    def test_write_power_value(self):
        dummy_csv_logger = DummyCSVLogger()
        dummy_broker = DummyBroker(self.__broker_address, self.__broker_queue_name)

        pv_simulator = PVSimulator(broker=dummy_broker, min_power_value=self.__min_power_value,
                                   max_power_value=self.__max_power_value,
                                   simulator_pv_generator=lambda x, y: self.__meter_power_value,
                                   csv_filer_writer=dummy_csv_logger)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(pv_simulator.write_power_value(self.__meter_power_value, self.__simulated_power_value,
                                       self.__combined_power_value))

        self.assertTrue(dummy_csv_logger.get_write_status())

    def test_generate_power_value_when_power_value_in_range(self):
        """
        Tests read_consumed_power_value() from HomeMeter when power value
        is within min-max range
        :return:
        """
        dummy_csv_logger = DummyCSVLogger()
        dummy_broker = DummyBroker(self.__broker_address, self.__broker_queue_name)

        pv_simulator = PVSimulator(broker=dummy_broker, min_power_value=self.__min_power_value,
                                   max_power_value=self.__max_power_value,
                                   simulator_pv_generator=lambda x, y: self.__meter_power_value,
                                   csv_filer_writer=dummy_csv_logger)
        self.assertEqual(pv_simulator.generate_power_value(), self.__meter_power_value)
        self.assertTrue(pv_simulator.generate_power_value() in range(int(self.__min_power_value),
                                                                     int(self.__max_power_value) + 1))

    def test_generate_power_value_when_power_value_out_of_range(self):
        """
        Tests read_consumed_power_value() from HomeMeter when power value
        is outside of min-max range
        :return:
        """
        dummy_csv_logger = DummyCSVLogger()
        dummy_broker = DummyBroker(self.__broker_address, self.__broker_queue_name)

        pv_simulator = PVSimulator(broker=dummy_broker, min_power_value=self.__min_power_value,
                                   max_power_value=self.__max_power_value,
                                   simulator_pv_generator=lambda x, y: -1,
                                   csv_filer_writer=dummy_csv_logger)
        self.assertEqual(pv_simulator.generate_power_value(), -1)
        self.assertFalse(pv_simulator.generate_power_value() in range(int(self.__min_power_value),
                                                                      int(self.__max_power_value) + 1))

    def test_connect_with_broker(self):
        dummy_csv_logger = DummyCSVLogger()
        dummy_broker = DummyBroker(self.__broker_address, self.__broker_queue_name)

        pv_simulator = PVSimulator(broker=dummy_broker, min_power_value=self.__min_power_value,
                                   max_power_value=self.__max_power_value,
                                   simulator_pv_generator=lambda x, y: -1,
                                   csv_filer_writer=dummy_csv_logger)
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(pv_simulator.connect_with_broker())
            self.assertTrue(dummy_broker.connect_to_server_invoked)
        except AMQPConnectionError:
            self.assertTrue(False)

    def test_close_connection(self):
        dummy_csv_logger = DummyCSVLogger()
        dummy_broker = DummyBroker(self.__broker_address, self.__broker_queue_name)

        pv_simulator = PVSimulator(broker=dummy_broker, min_power_value=self.__min_power_value,
                                   max_power_value=self.__max_power_value,
                                   simulator_pv_generator=lambda x, y: -1,
                                   csv_filer_writer=dummy_csv_logger)
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(pv_simulator.close_connection())
            self.assertTrue(dummy_broker.close_connection_invoked)
        except AMQPConnectionError:
            self.assertTrue(False)

    def test_on_message(self):
        message = Message(b'81')
        dummy_csv_logger = DummyCSVLogger()
        dummy_broker = DummyBroker(self.__broker_address, self.__broker_queue_name)

        pv_simulator = PVSimulator(broker=dummy_broker, min_power_value=self.__min_power_value,
                                   max_power_value=self.__max_power_value,
                                   simulator_pv_generator=lambda x, y: 10,
                                   csv_filer_writer=dummy_csv_logger)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(pv_simulator.on_message(message))
        self.assertTrue(dummy_csv_logger.get_write_status())


class DummyCSVLogger(FileWriter):
    __write_successful = False

    async def write(self, timestamp: datetime, meter_power_value: int, simulator_power_value: int,
                    combined_power_value: int) -> None:
        self.__write_successful = True

    def get_write_status(self):
        return self.__write_successful


class DummyBroker(Broker):
    connect_to_server_invoked = False
    publish_invoked = False
    close_connection_invoked = False
    register_consumer_invoked = False

    def __init__(self, broker_address: str, broker_queue_name: str):
        self.__broker_address = broker_address
        self.__broker_queue = broker_queue_name

    async def connect_to_server(self):
        self.connect_to_server_invoked = True

    async def publish(self, value: str):
        self.publish_invoked = True

    async def close_connection(self):
        self.close_connection_invoked = True

    def register_consumer(self, consumer: Consumer):
        self.register_consumer_invoked= True


if __name__ == "__main__":
    unittest.main()
