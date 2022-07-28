# ECG Steering wheel
This folder contains all the code and schematics required to assemble and run the prototype Steering wheel and it's individual elements. 


**Known Bugs**
- Running the Accelerometer module on start up works fine, but after running NFC module the accelerometer code no longer produces data, 
    -> this seems to be something to do with a clash in the SPI channels, or changes in the configurations of the channels between the two different code sets.
- Dual camera module not running yet.


**Accelerometer**
 - Running ./BMI160_Accl.py script will print the raw accelerometer values to the command line.
 - By changing the function called in the while loop Gyroscope and Accelerometer values can be read.
 - Data sheet found at : https://www.digikey.com/en/datasheets/bosch-sensortec/bosch-sensortec-bst-bmi160-ds000-07 

**Audio**
 - Running ./audio.py will play the applause-1.wav audio file.
 - The audio volume can ve varied on the physical audio driver by rotating the small pot next to the A+ pin.

**GPS**
 - Opening GPS/examples and running ./latlon.py will run the GPS module printing the current GPS latitude and longitude.

**NFC**
 - Running ./ example_get_uid.py will print to the terminal the ID of any NFC tag nearby.
 
 
**Fresh Installation**
1. Flash new RaspberryPi image
    - Using Raspberry Pi Imager flash the latest version of RASPBERRY PI OS LITE (32-BIT) onto the SD-Card that will hold the Pis OS.
  
    - Once complete insert into Pi and power it up.
        - Username: pi
        - Password: raspberry

2. Initialise network connections
    - Enable SSH:
        - sudo raspi-config,
            - In interface options enable SSH

    - Connect to the wifi network, tutorial found in the following link.
       (https://desertbot.io/blog/headless-raspberry-pi-4-ssh-wifi-setup)
    
2. Download the repository from git.
    - sudo apt update
    - sudo apt upgrade
    - set the ip address of the Pi
    - sudo apt install git
    - sudo apt clone https://github.com/NicholasAntoniadesEngineer/ECG-Steering-Wheel.git
    
3. Install I2C and SPI dependencies
    - Enable I2C,SPI:
        - run sudo raspi-config,
            - In interface options enable SPI,I2C,Serial
    - sudo apt install python
    - sudo apt install pip
    - sudo pip install spidev
    - pip3 install RPi.GPIO
    - pip3 install spidev
    - pip3 install pygame
    - sudo apt-get install libsdl-ttf2.0-0
    - Initialization of multiple SPI channels, tutorial found in the following link.
      (https://raspberrypi.stackexchange.com/questions/61430/i-want-to-use-spi0-and-spi1-at-the-same-time)

4. Install GPS libraries in I2C/PA1010D
    - sudo install.sh
    - sudo pip install smbus0
    
6. Install NFC hat libraries
    - pip install serial
    - pip3 install serial
