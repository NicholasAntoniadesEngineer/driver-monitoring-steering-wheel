#!/usr/bin/env python3
"""
BLE ECG Data Capture Script

This script runs on a Raspberry Pi 4B and connects to a BLE ECG device intended for the garment research project.
It connects to a selected device and writes all data to a single .csv file.

Author: Nicholas Antoniades
Start Date: 03/01/2022
Last Modified: 23/05/2022
"""

import datetime
import sys
from lib.constants import *
from lib.bluetooth_connection import BluetoothConnection
from lib.data_processing import DataProcessor
from lib.file_management import FileManager
from lib.header_configs import DEVICE_HEADERS

def get_device_config():
    """Configure device settings based on the selected device."""
    device_new = ""
    selected_device = device_new if device_new else DEVICE_OLD
    
    device_type = 'ECG_5LEAD' if selected_device == DEVICE_1 else 'ECG_IMU'
    
    file_config = {
        'test_name': 'Test',
        'device_name': 'Brain-Beta-v1-1' if selected_device == DEVICE_OLD else 'Older-Version',
        'file_prefix': 'ble_ecg',
        'headers': DEVICE_HEADERS[device_type]
    }
    
    return selected_device, file_config

def initialize_components(selected_device, num_channels_ecg, device_name):
    """Initialize all required components for data collection."""
    test_name = 'Test'
    file_manager = FileManager(test_name, device_name, selected_device)
    data_processor = DataProcessor(num_channels_ecg)
    bluetooth_connection = BluetoothConnection(selected_device)
    
    time_stamp = datetime.datetime.now()
    delta_time = datetime.timedelta(seconds=1/ECG_SAMPLING_PERIOD)
    return file_manager, data_processor, bluetooth_connection, time_stamp, delta_time

def main():
    """Main function to run the BLE ECG data capture."""
    selected_device, num_channels_ecg, device_name = get_device_config()
    
    file_manager, data_processor, bluetooth_connection, time_stamp, delta_time = initialize_components(
        selected_device, num_channels_ecg, device_name
    )
    
    while True:
        bluetooth_data = bluetooth_connection.connect()
        write_count, writer, f = file_manager.get_next_available_file(time_stamp)
        bluetooth_connection.collect_data(data_processor, writer, time_stamp, delta_time, f)

if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print('\nInterrupted')
            sys.exit(0)

