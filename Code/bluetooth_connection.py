"""
Bluetooth Connection Management
"""

import pexpect
import time
from constants import *

class BluetoothConnection:
    """Class to manage Bluetooth connections."""

    def __init__(self, selected_device):
        self.selected_device = selected_device
        self.connection_request = f"connect {selected_device}"
        self.attempt_counter = 0

    def connect(self):
        """Attempts connection to the selected Bluetooth device."""
        print("\nRunning gatttool...")
        bluetooth_data = pexpect.spawn("gatttool -I")
        print(f"Attempting to connect to: {self.selected_device}")

        try:
            bluetooth_data.sendline(self.connection_request)
            bluetooth_data.expect("Connection successful", timeout=0.5)
            print("Connected!\n")
        except Exception:
            print("Cannot connect to Bluetooth device\n")
            while True:
                try:
                    bluetooth_data.sendline(self.connection_request)
                    bluetooth_data.expect("Connection successful", timeout=0.5)
                    print("\nConnected!\n")
                    break
                except Exception:
                    print(f"\nAttempting to connect, attempt: {self.attempt_counter}\n")
                    self.attempt_counter += 1
                    time.sleep(0.05)

        bluetooth_data.sendline(MTU_VALUE)
        if self.selected_device in [DEVICE_3, DEVICE_4]:
            bluetooth_data.sendline(STREAM_REQUEST_NEW)
            bluetooth_data.expect(ACK_HANDLE_NEW, timeout=1)
        else:
            bluetooth_data.sendline(STREAM_REQUEST_OLD)
            bluetooth_data.expect(ACK_HANDLE_OLD, timeout=1)

        return bluetooth_data 