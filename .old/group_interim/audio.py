import numpy
import scipy.signal
import pygame, pygame.sndarray
#
#numpy can only generate sin waves
#scipy can generate square waves and sawtooth waves

# Objective: make function play audio corresponding to the n parameter provided
# Include any necessary dependencies above - numpy has been provided
sample_rate = 44100 #typical value


def playAudio(sample_wave, ms, n):
	# Write function here
    sound = pygame.sndarray.make_sound(sample_wave) #make_sound converts array into sound
    sound.play(1) #play the sound
    pygame.time.delay(ms) #Will pause for a given number of milliseconds. This function will use the processor (rather than sleeping) in order to make the delay more accurate
    sound.stop() #stop the sound

def square_wave(hz, peak=100000, duty_cycle=0.09, n_samples=sample_rate):
    """Compute N samples of a square wave with given frequency and peak amplitude.
       Defaults to one second.
    """
    t = numpy.linspace(0, 1, 500 * 440/(2*hz), endpoint=False)
    #numpy.linspace(start, stop, samping size, endpoint=True, retstep=False, dtype=None, axis=0)
    wave = scipy.signal.square(2 * numpy.pi * 5 * t, duty=duty_cycle)
    #The square wave has a period 2*pi, has value +1 from 0 to 2*pi*duty and -1 from 2*pi*duty to 2*pi. duty must be in the interval [0,1].
    wave = numpy.resize(wave, (n_samples,))
    return (peak / 2 * wave.astype(numpy.int16)).astype(numpy.int16)

# user_input = [4] # 4 is max possible - look into issue (TODO)
# n = random.choice(user_input)
# print (n)

def outputAudioTurns(n):
    # Depending on number of turns needed, duration of audio increases
    if n == 0:
        factor = 1

    elif n == 1:
        factor = 1.05

    elif n == 2:
        factor = 1.05

    elif n == 3:
        factor = 1.03

    elif n == 4:
        factor = 100

    ms = int(n * factor * 1000)
    pygame.mixer.init(channels=1)
    playAudio(square_wave(50.8), ms, n)


#outputAudioTurns(1)

# Number of moves required by robot to solve final face
# Defined per following: 0 <= n < 4

# Plays audio corresponding to value of "n"
# NB: 50Hz SQuaRe wave for 1s turns 90 deg - n seconds to be played for "n"

#reference:  https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.square.html
#            http://shallowsky.com/blog/programming/python-play-chords.html
