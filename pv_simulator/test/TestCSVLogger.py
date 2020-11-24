"""
This test class verifies method of CSVLogger class.
"""

import unittest
from pv_simulator.CSVFileWriter import CSVLogger
import csv
from datetime import datetime


class TestCSVLogger(unittest.TestCase):

    __meter_power_value = 3.4
    __simulator_power_value = 4.1
    __combined_power_value = 7
    __test_file_name = "resources/pv_simulator.csv"

    def test_write_when_added_one_new_line(self):
        """
        Test write method of CSVLogger after adding one more line.
        :return:
        """
        file_content_before_write = TestCSVLogger.__read_file_content(self.__test_file_name)
        csv_logger = CSVLogger(self.__test_file_name)
        csv_logger.write(datetime.now(), self.__meter_power_value, self.__simulator_power_value,
                         self.__combined_power_value)
        file_content_after_write = TestCSVLogger.__read_file_content(self.__test_file_name)
        self.assertNotEqual(file_content_before_write, file_content_after_write)
        self.assertEqual(len(file_content_before_write) + 1, len(file_content_after_write))
        difference_in_file_content = TestCSVLogger.__difference_between_two_list(file_content_after_write,
                                                                                 file_content_before_write)
        self.assertEqual(difference_in_file_content[0][1], str(self.__meter_power_value))
        self.assertEqual(difference_in_file_content[0][2], str(self.__simulator_power_value))
        self.assertEqual(difference_in_file_content[0][3], str(self.__combined_power_value))

    @staticmethod
    def __read_file_content(file: str) -> list:
        with open(file, mode='r') as csv_file:
            csv_file_reader = csv.reader(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            return [row for row in csv_file_reader]

    @staticmethod
    def __difference_between_two_list(first_list: list, second_list: list) -> list:
        return [item for item in first_list if item not in second_list]


if __name__ == '__main__':
    unittest.main()
