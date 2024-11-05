#!/usr/bin/env python3
"""
ECG and Grip Force Monitoring Script

This script interfaces with the ADS1293 and ADS1241 devices to read ECG and ADC data.
It uses the Raspberry Pi's SPI interface for communication.

Author: Nicholas Antoniades
Date: 2020-11-04
"""

import spidev
import RPi.GPIO as GPIO
import time
from ads1293 import ADS1293
from ads1241 import ADS1241

# GPIO Pin Constants
CS1_PIN = 24
CS2_PIN = 23

# SPI Constants
SPI_BUS = 0
SPI_DEVICE = 0
SPI_MAX_SPEED_HZ = 32000

# Other Constants
SHORT_COUNTER_LIMIT = 7
SLEEP_INTERVAL = 0.005

class SPIInterface:
    """Class to handle SPI communication with devices."""

    def __init__(self, bus, device, max_speed_hz=SPI_MAX_SPEED_HZ):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = max_speed_hz
        print('SPI initialized')

    def transfer(self, data):
        """Transfer data over SPI."""
        return self.spi.xfer(data)

    def close(self):
        """Close the SPI connection."""
        self.spi.close()

class GPIOInterface:
    """Class to handle GPIO operations."""

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(CS1_PIN, GPIO.OUT)
        GPIO.setup(CS2_PIN, GPIO.OUT)
        GPIO.output(CS1_PIN, 1)
        GPIO.output(CS2_PIN, 1)

    def set_output(self, pin, state):
        """Set the output state of a GPIO pin."""
        GPIO.output(pin, state)

def main():
    """Main function to run the ECG and ADC data collection."""
    gpio = GPIOInterface()
    spi = SPIInterface(SPI_BUS, SPI_DEVICE)

    ecg_device = ADS1293(spi, gpio, CS1_PIN)
    adc_device = ADS1241(spi, gpio, CS2_PIN)

    adc_device.program_adc()

    while True:
        print('Checking device on CS1')
        if ecg_device.test_connection():
            print('Initialize Device 1 to 1 lead mode')
            ecg_device.init_1lead()

            short_counter = 0
            while True:
                adc_device.input_select(ADS1241_P_AIN0)
                p_ain0_data = adc_device.fetch_adc_data()
                p_ain0_raw = ((p_ain0_data[0] & 0xFF) << 16) | ((p_ain0_data[1] & 0xFF) << 8) | (p_ain0_data[2] & 0xFF)

                while short_counter <= SHORT_COUNTER_LIMIT:
                    data = ecg_device.read_ecg_data_ch1_ch2()
                    ch1data_raw = ((data[0] & 0xFF) << 16) | ((data[1] & 0xFF) << 8) | (data[2] & 0xFF)
                    print(ch1data_raw, p_ain0_raw)
                    short_counter += 1
                    time.sleep(SLEEP_INTERVAL)
                short_counter = 0
        else:
            print('Cannot detect device!')
            time.sleep(0.1)

if __name__ == '__main__':
    main()
    