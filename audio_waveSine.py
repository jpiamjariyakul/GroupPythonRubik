import numpy as np
import scipy.signal
import pygame, pygame.sndarray
# from matplotlib import pyplot as plt

# Reference:  	http://shallowsky.com/blog/programming/python-play-chords.html
#				https://docs.scipy.org/doc/numpy/reference/generated/numpy.sin.html

# NumPy can only generate sin waves
# SciPy can generate square waves and sawtooth waves

# Generation of sine wave code based from such references per stated above

def playAudio(frqc, ms):
	# Code obtained
	def sine_wave(hz, amplitude=4096, sample_rate=44100):
		# Compute N samples of a sine wave with given frequency and peak amplitude
		# Number of samples per second == sample rate == 44.1k Hz
		length = sample_rate / float(hz) # Sets sample length given sample rate
		w = (np.pi * 2) / length # Obtain 
		t = np.arange(int(length)) * w
		onecycle = amplitude * np.sin(t)
		waveFull = np.resize(onecycle, sample_rate).astype(np.int16)
		return waveFull
	# Converts array into sound (via make_sound())
	sound = pygame.sndarray.make_sound(sine_wave(frqc))
	sound.play(-1) # Plays the sound
	pygame.time.delay(ms) # Delays output for a given number of milliseconds
	sound.stop() # Stops the sound

def audioPlayMove(frqcCurrent):
	# duration = int(50) # Duration of audio in ms
	duration = int(50) # Duration of audio in ms
	pygame.mixer.init(channels=1) # Sets audio to output in channel 1
	playAudio(frqcCurrent, duration) # 2 added ad hoc since output frqc is half intended

def audioInputSeq(ls_moves):# Receives list of moves
	dict_frqcFilter = { # All of these values are in kHz
		'U': 00.5,	'R': 03.5,
		'F': 08.5,	'D': 12.5,
		'L': 15.0 ,	'B': 20.5	} # L: 16.5 originally
	ls_frqc = [(float(dict_frqcFilter.get(moveCurrent[0]) * 1000), moveCurrent[1]) for moveCurrent in ls_moves] # Maps moves in list to frequency (in kHz)
	for frqcCurrent in ls_frqc:
		print("Playing audio for " + str(frqcCurrent[0]) + " Hz, given mode " + str(frqcCurrent[1]))
		for turn in range(frqcCurrent[1]): audioPlayMove(frqcCurrent[0]) # Plays audio corresponding to moves in list

#audioInputSeq([('L', 1)])
