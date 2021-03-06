"""
This is a generic broker interface.
"""
__author__ = 'Md Shifuddin Al Masud'
__email__ = 'shifuddin.masud@gmail.com'
__license__ = 'MIT License'

from pv_simulator.Consumer import Consumer


class Broker:
    def connect_to_server(self):
        """
        Connect to the broker server.
        :return:
        """
        pass

    def publish(self, value: str):
        """
        Publish give value.
        :param value:
        :return:
        """
        pass

    def register_consumer(self, consumer: Consumer):
        """
        Consume message by registering the consumer to the
        broker.
        :param consumer:
        :return:
        """
        pass

    def close_connection(self):
        """
        Close connection with the server.
        :return:
        """
        pass

