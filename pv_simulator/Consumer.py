"""
This is a generic consumer interface which facilitates power value consumption and connection closer
with broker.
"""
__author__ = 'Md Shifuddin Al Masud'
__email__ = 'shifuddin.masud@gmail.com'
__license__ = 'MIT License'

from aio_pika import IncomingMessage


class Consumer:
    def start_consuming_power_value(self) -> None:
        """Read message from broker"""
        pass

    def close_connection(self):
        """Close connection with the broker"""
        pass

    def on_message(self, message: IncomingMessage):
        """
        Callback function for message receive
        :param message:
        :return:
        """


