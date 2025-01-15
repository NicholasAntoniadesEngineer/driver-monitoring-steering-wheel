"""
Hardware Interface Management

This module provides interfaces for hardware communication (SPI and GPIO)
for the ECG and Grip Force monitoring system.
"""

import spidev
import RPi.GPIO as GPIO

class SPIInterface:
    """Class to handle SPI communication with devices."""

    def __init__(self, config):
        """Initialize SPI interface with configuration.
        
        Args:
            config (dict): Configuration dictionary containing:
                - bus (int): SPI bus number
                - device (int): SPI device number
                - max_speed_hz (int): Maximum speed in Hz
        """
        self.spi = spidev.SpiDev()
        self.spi.open(config['bus'], config['device'])
        self.spi.max_speed_hz = config.get('max_speed_hz', 32000)
        print('SPI initialized')

    def transfer(self, data):
        """Transfer data over SPI."""
        return self.spi.xfer(data)

    def close(self):
        """Close the SPI connection."""
        self.spi.close()

class GPIOInterface:
    """Class to handle GPIO operations."""

    def __init__(self, config):
        """Initialize GPIO interface with configuration.
        
        Args:
            config (dict): Configuration dictionary containing:
                - pins (dict): Dictionary of pin names to pin numbers
                - mode (str, optional): GPIO mode ('BCM' or 'BOARD'), defaults to 'BCM'
                - initial_states (dict, optional): Dictionary of pin names to initial states
        """
        self.config = config
        self.pins = config['pins']
        
        # Set GPIO mode
        mode = config.get('mode', 'BCM')
        if mode == 'BCM':
            GPIO.setmode(GPIO.BCM)
        elif mode == 'BOARD':
            GPIO.setmode(GPIO.BOARD)
            
        GPIO.setwarnings(False)
        
        # Setup pins
        for pin_name, pin_number in self.pins.items():
            GPIO.setup(pin_number, GPIO.OUT)
            initial_state = config.get('initial_states', {}).get(pin_name, 1)
            GPIO.output(pin_number, initial_state)

    def set_output(self, pin_name, state):
        """Set the output state of a GPIO pin.
        
        Args:
            pin_name (str): Name of the pin as defined in config
            state (int): Output state (0 or 1)
        """
        if pin_name in self.pins:
            GPIO.output(self.pins[pin_name], state)
        else:
            raise ValueError(f"Pin name '{pin_name}' not found in configuration")

    def cleanup(self):
        """Clean up GPIO resources."""
        GPIO.cleanup() 