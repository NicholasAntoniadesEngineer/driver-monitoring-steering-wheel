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
                - selected_device (str): Selected device identifier
        """
        self.test_name = config['test_name']
        self.device_name = config['device_name']
        self.selected_device = config['selected_device']

    def update_file_path(self, time_stamp):
        """Creates a custom file path."""
        current_date = str(time_stamp.date())
        current_time = time_stamp.strftime("%-H-%S")
        version = 'v'
        file_path = f"{self.test_name}_{self.device_name}_{current_time}_{current_date}_{version}"
        return file_path

    def initialise_csv(self, ver_counter, file_path):
        """Initialise the CSV file for data capture."""
        ver_counter += 1
        f = open(file_path + str(ver_counter) + '.csv', 'w')
        writer = csv.writer(f)

        time_stamp = datetime.datetime.now()
        writer.writerow(['# Recorded using POD_Data_Capture.py'])
        writer.writerow(['# Recorded on:     ' + str(time_stamp)])
        writer.writerow(['# Device address:   ' + self.device_name])
        writer.writerow(['# Device ID:        ' + self.selected_device])
        writer.writerow([])

        if self.selected_device == DEVICE_1:
            data_header = ['ECG_1', 'ECG_2', 'ECG_3', 'ECG_4', 'ECG_5', 'tstamp']
        else:
            data_header = ['ECG_LOD', 'ECG_1', 'ECG_2', 'A_X', 'A_Y', 'A_Z', 'G_X', 'G_Y', 'G_Z', 'M_X', 'M_Y', 'M_Z', 'tstamp']
        writer.writerow(data_header)

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