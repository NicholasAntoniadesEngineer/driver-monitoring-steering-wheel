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
from constants import *
from bluetooth_connection import BluetoothConnection
from data_processing import DataProcessor
from file_management import FileManager

def main():
    device_new = ""
    selected_device = device_new if device_new else DEVICE_OLD
    test_name = 'Test'

    if selected_device == DEVICE_1:
        num_channels_ecg = 5
    elif selected_device == DEVICE_4:
        num_channels_ecg = 2
    else:
        num_channels_ecg = 2

    device_name = 'Brain-Beta-v1-1' if selected_device == DEVICE_OLD else 'Older-Version'

    file_manager = FileManager(test_name, device_name, selected_device)
    data_processor = DataProcessor(num_channels_ecg)
    bluetooth_connection = BluetoothConnection(selected_device)

    time_stamp = datetime.datetime.now()
    delta_time = datetime.timedelta(seconds=1/ECG_SAMPLING_PERIOD)
    file_path = file_manager.update_file_path(time_stamp)

    while True:
        write_count = 0
        ver_counter = 0

        bluetooth_data = bluetooth_connection.connect()

        while True:
            if os.path.isfile(file_path + str(ver_counter) + '.csv'):
                ver_counter += 1
            else:
                write_count, writer, f = file_manager.initialise_csv(ver_counter, file_path)
                break

        while True:
            try:
                if selected_device in [DEVICE_3, DEVICE_4]:
                    bluetooth_data.expect("Notification handle = 0x0015 value:", timeout=1)
                else:
                    bluetooth_data.expect("Notification handle = 0x001c value:", timeout=1)
            except Exception:
                print("\nConnection lost!\n")
                f.close()
                break

            data_processor.process_data(bluetooth_data)

            time_val = [time_stamp + delta_time * k for k in range(SAMPLES_PER_CHANNEL_ECG)]

            if write_count >= SKIP_NUM:
                for l in range(SAMPLES_PER_CHANNEL_ECG):
                    data_to_write = [0] * (NUM_CHANNEL_IMU + num_channels_ecg + 2)
                    data_to_write[0] = data_processor.raw_lod_ecg[0]

                    for m in range(num_channels_ecg):
                        data_to_write[NUM_LOD_CHANNELS + m] = data_processor.converted_voltage_ecg[m, l]

                    for m in range(NUM_CHANNEL_IMU):
                        data_to_write[num_channels_ecg + NUM_LOD_CHANNELS + m] = data_processor.multi_axis_imu[0, m]

                    data_to_write[12] = time_val[l].isoformat()
                    writer.writerow(data_to_write)

                    print(bluetooth_data.before[1:180])
            else:
                write_count += 1

if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print('\nInterrupted')
            sys.exit(0)

