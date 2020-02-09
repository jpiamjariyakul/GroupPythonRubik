import numpy as np
import scipy.signal
import pygame, pygame.sndarray

# NumPy can only generate sin waves
# SciPy can generate square waves and sawtooth waves

def square_wave(hz, peak=80000, duty_cycle=.5, n_samples=sample_rate):
    """	Compute N samples of a square wave with given frequency and peak amplitude.
       	Defaults to one second.
    """
	sample_rate = 44100 # General sampling rate of 44.1 kHz
    t = np.linspace(0, 1, 500 * 440/(2*hz), endpoint=False)
    #numpy.linspace(start, stop, samping size, endpoint=True, retstep=False, dtype=None, axis=0)
	# TODO: Generate sine wave with rate of 44.1k Hz
	# wave = np.sin()
	#wave = scipy.signal.sine(2 * numpy.pi * 5 * t, duty=duty_cycle)
    #The square wave has a period 2*pi, has value +1 from 0 to 2*pi*duty and -1 from 2*pi*duty to 2*pi. duty must be in the interval [0,1].
    wave = np.resize(wave, (n_samples,))
    return (peak / 2 * wave.astype(np.int16)).astype(np.int16)

def playAudio(sample_wave, ms, n):
    sound = pygame.sndarray.make_sound(sample_wave) # Converts array into sound (via make_sound())
    sound.play(1) # Plays the sound
    pygame.time.delay(ms) # Pause for a given number of milliseconds. This function will use the processor (rather than sleeping) in order to make the delay more accurate
    sound.stop() # Stosp the sound

#ms = int(n * 1.013 * 1000)
pygame.mixer.init(channels=1)
playAudio(square_wave(50), ms, n)

# Reference:  	https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.square.html
#            	http://shallowsky.com/blog/programming/python-play-chords.html
#				https://docs.scipy.org/doc/numpy/reference/generated/numpy.sin.html