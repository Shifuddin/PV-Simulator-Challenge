"""
This is a generic producer interface which supports publishing and connection close.
"""
__author__ = 'Md Shifuddin Al Masud'
__email__ = 'shifuddin.masud@gmail.com'
__license__ = 'MIT License'


class Producer:
    def connect_with_broker(self):
        """
        Connect to the broker
        And declare a queue there.
        :return:
        """
        pass

    def publish_message(self, power_value: int) -> None:
        """
        Receives power value in watt and publish it to broker
        :param power_value:
        :return:
        """
        pass

    def close_connection(self):
        """Close Connection with the broker"""
        pass
