"""
Data Collection Management

This module provides the data collection functionality for the ECG and Grip Force
monitoring system, managing the interaction between hardware devices and data storage.
"""

import time
import datetime
from .ads1293 import ADS1293
from .ads1241 import ADS1241
from .hardware_interfaces import SPIInterface, GPIOInterface
from .file_management import FileManager

class DataCollector:
    """Class to manage data collection from ECG and ADC devices."""

    def __init__(self, config):
        """Initialize data collector with configuration.
        
        Args:
            config (dict): Configuration dictionary containing:
                - spi_config (dict): SPI interface configuration
                - gpio_config (dict): GPIO interface configuration
                - sampling_config (dict): Sampling parameters
                - file_config (dict): File management configuration
                - devices (dict): Device-specific configuration
        """
        self.config = config
        self.gpio = GPIOInterface(config['gpio_config'])
        self.spi = SPIInterface(config['spi_config'])
        
        # Initialize devices based on config
        devices_config = config['devices']
        self.ecg_device = ADS1293(
            self.spi, 
            self.gpio, 
            devices_config['ecg']['cs_pin_name']
        )
        self.adc_device = ADS1241(
            self.spi, 
            self.gpio, 
            devices_config['adc']['cs_pin_name']
        )
        
        # Initialize file manager
        file_config = config['file_config']
        self.file_manager = FileManager(
            file_config['test_name'],
            file_config['device_name'],
            file_config['device_id']
        )
        
        # Store sampling configuration
        self.sampling_config = config['sampling_config']

    def initialize_devices(self):
        """Initialize both ECG and ADC devices."""
        self.adc_device.program_adc()
        if not self.ecg_device.test_connection():
            raise ConnectionError('Cannot detect ECG device!')
        print('Initialize Device 1 to 1 lead mode')
        self.ecg_device.init_1lead()

    def collect_data_sample(self):
        """Collect one sample of data from both devices."""
        self.adc_device.input_select(self.config['devices']['adc']['input_channel'])
        p_ain0_data = self.adc_device.fetch_adc_data()
        p_ain0_raw = ((p_ain0_data[0] & 0xFF) << 16) | ((p_ain0_data[1] & 0xFF) << 8) | (p_ain0_data[2] & 0xFF)

        data = self.ecg_device.read_ecg_data_ch1_ch2()
        ch1data_raw = ((data[0] & 0xFF) << 16) | ((data[1] & 0xFF) << 8) | (data[2] & 0xFF)
        
        return ch1data_raw, p_ain0_raw

    def start_data_collection(self):
        """Start the continuous data collection process."""
        try:
            self.initialize_devices()
            
            time_stamp = datetime.datetime.now()
            write_count, writer, f = self.file_manager.get_next_available_file(time_stamp)
            
            while True:
                short_counter = 0
                while short_counter <= self.sampling_config['short_counter_limit']:
                    ch1data_raw, p_ain0_raw = self.collect_data_sample()
                    writer.writerow([ch1data_raw, p_ain0_raw, datetime.datetime.now().isoformat()])
                    print(ch1data_raw, p_ain0_raw)
                    short_counter += 1
                    time.sleep(self.sampling_config['sleep_interval'])

        except KeyboardInterrupt:
            print('\nData collection interrupted')
            f.close()
            self.cleanup()
        except Exception as e:
            print(f'\nError during data collection: {str(e)}')
            f.close()
            self.cleanup()
            raise

    def cleanup(self):
        """Clean up resources."""
        self.spi.close()
        self.gpio.cleanup() 