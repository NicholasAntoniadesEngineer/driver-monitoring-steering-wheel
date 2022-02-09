# Kymira-Fuell_Black-Box

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
    
2. Download Kymira-Fuell_Black-Box repository from git.
    - sudo apt update
    - sudo apt upgrade
    - set the ip address of the Pi
    - sudo apt install git
    - sudo apt clone https://github.com/nicholasantoniades/Kymira-Fuell_Black-Box.git
    
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



