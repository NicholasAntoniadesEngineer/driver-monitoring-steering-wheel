# ECG Driver Monitoring Steering Wheel

## Overview
As part of an Innovate UK funded project (May 2021), this project explores the feasibility of recording heart rate variability (HRV) data of a driver in a vehicle using bipotential recording directly from the steering wheel. The system faces unique challenges in dealing with electromagnetic interference, noise management, and signal consistency as drivers move their hands along and occasionally off the steering wheel.

## Project Goals
- Research and analyze vehicle ambient and driver-movement noise within the expected application setting
- Develop a proof-of-concept demonstrator comprising:
  - Multiple steering wheel cover versions with different electrode technologies
  - Simple steering wheel test rig for tabletop placement
  - Biopotential capture electronics with user display
  - R-peak extraction and HRV calculation capabilities

## System Architecture

### Hardware Components
- Raspberry Pi 4B (main controller)
- ADS1293 ECG sensor
- ADS1241 ADC for grip force monitoring
- Bluetooth Low Energy (BLE) communication module
- Custom steering wheel electrodes
- Display screen for real-time visualization

### Software Components
1. **Data Acquisition**
   - BLE communication handling
   - ECG signal sampling (500Hz)
   - Grip force monitoring
   - Real-time data processing

2. **Signal Processing**
   - Bandpass filtering
   - R-peak detection
   - HRV calculation
   - Noise reduction algorithms

