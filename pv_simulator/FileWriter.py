"""
Generic Interface for writing values.
"""
__author__ = 'Md Shifuddin Al Masud'
__email__ = 'shifuddin.masud@gmail.com'
__license__ = 'MIT License'

from datetime import datetime
import decimal


class FileWriter:
    def write(self, timestamp: datetime, meter_power_value: decimal, simulator_power_value: decimal,
              combined_power_value: decimal) -> None:
        """Write content to destination"""
        pass

