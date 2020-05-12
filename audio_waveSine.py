import numpy as np
import scipy.signal
import pygame, pygame.sndarray
from matplotlib import pyplot as plt

# Codebase:  	http://shallowsky.com/blog/programming/python-play-chords.html
#				https://docs.scipy.org/doc/numpy/reference/generated/numpy.sin.html

# NumPy can only generate sin waves
# SciPy can generate square waves and sawtooth waves

# Generation of sine wave code based from such references per stated above

def playAudio(frqc, duration):
	def waveSine(frqc, amplitude=4096, f_s=44100):
		# Compute N samples of a sine wave with given frequency and peak amplitude
		# Number of samples per second == sample rate == 44.1k Hz

		F = float(frqc) / f_s  # Obtain normalised frequency
		N_cycle = 1/F # Samples per cycle
		n = np.arange(0, int(N_cycle), 1) # Sets array of sampling indices
		t = n / f_s # Obtain timestamps to sample signal
		w = (2 * np.pi) * float(frqc) # Obtain angular frequency
		x_one = np.sin(w * t) # Samples signal at given timestamps
		x_full = np.resize((amplitude * x_one), f_s).astype(np.int16)

		'''
		T = np.arange(0, (sample_rate * duration), 1)
		# How many samples to take per second
		w = (2 * np.pi) * float(hz)
		x_one = np.sin(w * N / sample_rate)
		x_full = (amplitude * x_one).astype(np.int16)
		'''
		return x_full
	# Converts array into sound (via make_sound())
	audio = pygame.sndarray.make_sound(waveSine(frqc))
	audio.play(-1) # Plays the sound
	pygame.time.delay(duration) # Delays output for a given number of milliseconds
	audio.stop() # Stops the sound

def audioPlayMove(frqcCurrent):
	# duration = int(50) # Duration of audio in ms
	duration = int(50) # Duration of audio in ms
	pygame.mixer.init(channels=1) # Sets audio to output in channel 1
	playAudio(frqcCurrent, duration) # 2 added ad hoc since output frqc is half intended

def audioInputSeq(ls_moves):# Receives list of moves
	dict_frqcFilter = { # All of these values are in kHz
		'U': 0.42,	'R': 01.2,
		'F': 02.4,	'D': 4.9,
		'L': 10.2 ,	'B': 19.0	} # L: 16.5 originally
	ls_frqc = [(float(dict_frqcFilter.get(moveCurrent[0]) * 1000), moveCurrent[1]) for moveCurrent in ls_moves] # Maps moves in list to frequency (in kHz)
	for frqcCurrent in ls_frqc:
		print("Playing audio for " + str(frqcCurrent[0]) + " Hz, given mode " + str(frqcCurrent[1]))
		for turn in range(frqcCurrent[1]): audioPlayMove(frqcCurrent[0]) # Plays audio corresponding to moves in list

#audioInputSeq([('L', 1)])
