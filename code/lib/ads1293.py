"""
ADS1293 Device Interface

This module provides an interface to the ADS1293 device for ECG data collection.
"""

# Constants for ADS1293
ADS1293_REG_REVID = 0x40
ADS1293_REG_STOP_CONVERSION = 0x00
ADS1293_REG_CHANNEL_SETUP = 0x01
ADS1293_REG_COMMON_MODE = 0x0A
ADS1293_REG_RLD_OUTPUT = 0x0C
ADS1293_REG_CLOCK = 0x12
ADS1293_REG_CHANNEL_CONFIG = 0x13
ADS1293_REG_SHUTDOWN = 0x14
ADS1293_REG_DECIMATION_R2 = 0x21
ADS1293_REG_DECIMATION_R3_CH1 = 0x22
ADS1293_REG_DECIMATION_R3_CH2 = 0x23
ADS1293_REG_DECIMATION_R1 = 0x25
ADS1293_REG_DRDYB_SOURCE = 0x27
ADS1293_REG_LOOP_READBACK = 0x2F
ADS1293_REG_DATA_LOOP = 0x50

ECG_DATA_BYTES = 3

class ADS1293:
    """Class to interface with the ADS1293 device."""

    def __init__(self, spi, gpio, config):
        """Initialize ADS1293 with configuration.
        
        Args:
            spi: SPI interface instance
            gpio: GPIO interface instance
            config (dict): Configuration dictionary containing:
                - cs_pin (str): Chip select pin name
        """
        self.spi = spi
        self.gpio = gpio
        self.cs_pin = config['cs_pin']

    def reg_read(self, reg_address):
        """Read a single byte from a register."""
        self.gpio.set_output(self.cs_pin, 0)
        read_command = reg_address | 0x80
        self.spi.transfer([read_command])
        data = self.spi.transfer([0x0])
        self.gpio.set_output(self.cs_pin, 1)
        return data

    def reg_write(self, reg_address, data):
        """Write a single byte to a register."""
        self.gpio.set_output(self.cs_pin, 0)
        self.spi.transfer([reg_address, data])
        self.gpio.set_output(self.cs_pin, 1)

    def test_connection(self):
        """Test connection to the ADS1293 by reading a known register."""
        self.reg_write(ADS1293_REG_STOP_CONVERSION, 0x0)
        data = self.reg_read(ADS1293_REG_REVID)
        if str(data[0]) == '1':
            print('Success: ' + str(data[0]) + '\n')
            return True
        else:
            print('Failure, returned value: ' + str(data[0]) + '\n')
            return False

    def init_1lead(self):
        """Initialize the ADS1293 for 1-lead ECG operation."""
        self.reg_write(ADS1293_REG_STOP_CONVERSION, 0x0)
        self.reg_write(ADS1293_REG_CHANNEL_SETUP, 0x11)
        self.reg_write(ADS1293_REG_COMMON_MODE, 0x03)
        self.reg_write(ADS1293_REG_RLD_OUTPUT, 0x04)
        self.reg_write(ADS1293_REG_CLOCK, 0x04)
        self.reg_write(ADS1293_REG_CHANNEL_CONFIG, 0x1B)
        self.reg_write(ADS1293_REG_SHUTDOWN, 0x36)
        self.reg_write(ADS1293_REG_DECIMATION_R2, 0x10)
        self.reg_write(ADS1293_REG_DECIMATION_R3_CH1, 0x10)
        self.reg_write(ADS1293_REG_DECIMATION_R3_CH2, 0x10)
        self.reg_write(ADS1293_REG_DECIMATION_R1, 0x00)
        self.reg_write(ADS1293_REG_DRDYB_SOURCE, 0x08)
        self.reg_write(ADS1293_REG_LOOP_READBACK, 0x30)
        self.reg_write(ADS1293_REG_STOP_CONVERSION, 0x01)
        print('ADS1293 1 lead mode programmed \n')

    def read_ecg_data_ch1_ch2(self):
        """Read data from CH1 and CH2 of the ADS1293."""
        self.gpio.set_output(self.cs_pin, 0)
        read_command = ADS1293_REG_DATA_LOOP | 0x80
        self.spi.transfer([read_command])
        data = self.spi.transfer([0x0] * (ECG_DATA_BYTES * 2))
        self.gpio.set_output(self.cs_pin, 1)
        return data
