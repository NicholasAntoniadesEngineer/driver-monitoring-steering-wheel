#!/usr/bin/env python3

import sys
sys.path.append('/home/pi/Kymira-Fuell_Black-Box')
import os

from pygame import mixer

# Initialize pygame mixer
mixer.init()


# Load the sounds
sound = mixer.Sound('/home/pi/Kymira-Fuell_Black-Box/Code/Audio/applause-1.wav')

while True:
    sound.play()
