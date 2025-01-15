#!/usr/bin/env python3
"""
ECG and Grip Force Monitoring Script

This script interfaces with the ADS1293 and ADS1241 devices to read ECG and ADC data.
It uses the Raspberry Pi's SPI interface for communication.

Author: Nicholas Antoniades
Date: 2020-11-04
"""

import sys
from lib.data_collection import DataCollector
from lib.ads1241 import ADS1241_P_AIN0

# Configuration for the data collection system
SYSTEM_CONFIG = {
    'spi_config': {
        'bus': 0,
        'device': 0,
        'max_speed_hz': 32000
    },
    'gpio_config': {
        'mode': 'BCM',
        'pins': {
            'cs1': 24,  # ECG CS pin
            'cs2': 23   # ADC CS pin
        },
        'initial_states': {
            'cs1': 1,
            'cs2': 1
        }
    },
    'sampling_config': {
        'short_counter_limit': 7,
        'sleep_interval': 0.005
    },
    'file_config': {
        'test_name': 'ECG_Grip_Force',
        'device_name': 'ADS1293_ADS1241',
        'device_id': 'LOCAL'
    },
    'devices': {
        'ecg': {
            'cs_pin_name': 'cs1',
            'type': 'ADS1293'
        },
        'adc': {
            'cs_pin_name': 'cs2',
            'type': 'ADS1241',
            'input_channel': ADS1241_P_AIN0
        }
    }
}

def main():
    """Main function to run the ECG and ADC data collection."""
    data_collector = DataCollector(SYSTEM_CONFIG)
    data_collector.start_data_collection()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted')
        sys.exit(0)
    
