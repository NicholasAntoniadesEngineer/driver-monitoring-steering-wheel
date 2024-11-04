"""
File Management for Data Capture
"""

import csv
import datetime
import os

class FileManager:
    """Class to manage file operations for data capture."""

    def __init__(self, test_name, device_name, selected_device):
        self.test_name = test_name
        self.device_name = device_name
        self.selected_device = selected_device

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