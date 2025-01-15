"""
File Management for Data Capture
"""

import csv
import datetime
import os

class FileManager:
    """Class to manage file operations for data capture."""

    def __init__(self, config):
        """Initialize FileManager with configuration.
        
        Args:
            config (dict): Configuration dictionary containing:
                - test_name (str): Name of the test
                - device_name (str): Name of the device
                - file_prefix (str): Prefix for file names
                - headers (dict): Header configuration containing:
                    - columns (list): Column names
                    - metadata (dict): Additional metadata to write
        """
        self.test_name = config['test_name']
        self.device_name = config['device_name']
        self.file_prefix = config.get('file_prefix', 'data_capture')
        self.headers = config['headers']

    def update_file_path(self, time_stamp):
        """Creates a custom file path."""
        current_date = str(time_stamp.date())
        current_time = time_stamp.strftime("%-H-%S")
        version = 'v'
        file_path = f"{self.file_prefix}_{self.test_name}_{current_time}_{current_date}_{version}"
        return file_path

    def initialise_csv(self, ver_counter, file_path):
        """Initialise the CSV file for data capture."""
        ver_counter += 1
        f = open(file_path + str(ver_counter) + '.csv', 'w')
        writer = csv.writer(f)

        # Write metadata
        for key, value in self.headers['metadata'].items():
            writer.writerow([f'# {key}: {value}'])
        writer.writerow([f'# Recording time: {datetime.datetime.now()}'])
        writer.writerow([])

        # Write column headers
        writer.writerow(self.headers['columns'])

        return 0, writer, f

    def get_next_available_file(self, time_stamp):
        """Get the next available file path and CSV writer."""
        file_path = self.update_file_path(time_stamp)
        ver_counter = 0
        
        while os.path.isfile(file_path + str(ver_counter) + '.csv'):
            ver_counter += 1
        
        write_count, writer, f = self.initialise_csv(ver_counter, file_path)
        return write_count, writer, f

    def write_data_rows(self, writer, data_rows):
        """Write multiple rows of data to the CSV file."""
        for row in data_rows:
            writer.writerow(row)