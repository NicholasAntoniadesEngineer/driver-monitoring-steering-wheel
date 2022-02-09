from pygame import mixer

# Initialize pygame mixer
mixer.init()


# Load the sounds
sound = mixer.Sound('/home/pi/RaspberryPi_Dev/Audio/applause-1.wav')

while True:
    sound.play()
