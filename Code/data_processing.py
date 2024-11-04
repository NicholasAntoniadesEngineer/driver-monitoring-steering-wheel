"""
Data Processing for ECG and IMU
"""

import numpy as np
from constants import *

class DataProcessor:
    """Class to process raw ECG and IMU data."""

    def __init__(self, num_channels_ecg):
        self.num_channels_ecg = num_channels_ecg
        self.total_samples_ecg = num_channels_ecg * SAMPLES_PER_CHANNEL_ECG
        self.total_samples_imu = NUM_CHANNEL_IMU * SAMPLES_PER_CHANNEL_IMU
        self.single_sample_ecg = [1] * self.total_samples_ecg
        self.raw_adc_ecg = [1] * self.total_samples_ecg
        self.raw_lod_ecg = [1]
        self.single_sample_imu = [1] * self.total_samples_imu
        self.converted_voltage_ecg = np.array([[1] * SAMPLES_PER_CHANNEL_ECG] * num_channels_ecg, dtype=float)
        self.raw_imu = np.array([[1] * SAMPLES_PER_CHANNEL_IMU] * NUM_CHANNEL_IMU, dtype=float)
        self.multi_axis_imu = np.array([[1] * SAMPLES_PER_CHANNEL_ECG] * NUM_CHANNEL_IMU, dtype=float)

    def adc_to_voltage_ecg(self, adc_value):
        """Converts raw ECG ADC value to Voltage."""
        convert_value = adc_value / ADC_MAX
        convert_value -= 0.5
        convert_value *= V_REF * 2
        voltage_ecg = convert_value / 3.5
        return voltage_ecg

    def bytes_to_data_ecg(self, three_bytes):
        """Converts 3 bytes into a 24-bit value."""
        converted_data = (int(three_bytes[0], 16) << 16) + (int(three_bytes[1], 16) << 8) + int(three_bytes[2], 16)
        return converted_data

    def bytes_to_data_imu(self, two_bytes):
        """Converts 2 bytes into a signed 16-bit value."""
        converted_data = (int(two_bytes[1], 16) << 8) + int(two_bytes[0], 16)
        if converted_data > (2**15):
            converted_data -= 2**16
        return converted_data

    def process_data(self, bluetooth_data):
        """Process the raw ECG and IMU data."""
        ecg_lod = bluetooth_data.before[1:4]
        self.raw_lod_ecg[0] = int(ecg_lod, 16)

        x = 0
        for i in range(4, 183, 9):
            self.single_sample_ecg[x] = (bluetooth_data.before[i:i+2], bluetooth_data.before[i+3:i+5], bluetooth_data.before[i+6:i+8])
            self.raw_adc_ecg[x] = self.bytes_to_data_ecg(self.single_sample_ecg[x])
            x += 1

        for h in range(self.num_channels_ecg):
            x = 0
            for j in range(h, self.total_samples_ecg, self.num_channels_ecg):
                self.converted_voltage_ecg[h, x] = self.adc_to_voltage_ecg(self.raw_adc_ecg[j])
                x += 1

        x = 0
        for i in range(184, 238, 6):
            self.single_sample_imu[x] = (bluetooth_data.before[i:i+2], bluetooth_data.before[i+3:i+5])
            self.raw_imu[x] = self.bytes_to_data_imu(self.single_sample_imu[x])
            for i in range(3):
                self.multi_axis_imu[i, x] = self.raw_imu[x] / IMU_SCALE_FACTOR
            x += 1 