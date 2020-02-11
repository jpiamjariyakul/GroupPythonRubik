import numpy as np
import scipy.signal
import pygame, pygame.sndarray

# Reference:  	http://shallowsky.com/blog/programming/python-play-chords.html
#				https://docs.scipy.org/doc/numpy/reference/generated/numpy.sin.html

# NumPy can only generate sin waves
# SciPy can generate square waves and sawtooth waves

def playAudio(frqc, ms):
	def sine_wave(hz, amplitude=4096, sample_rate=44100):
		# Compute N samples of a sine wave with given frequency and peak amplitude
		# Number of samples per second == sample rate == 44.1k Hz
		length = sample_rate / float(hz)
		omega = np.pi * 2 / length
		t = np.arange(int(length)) * omega
		onecycle = amplitude * np.sin(t)
		return (np.resize(onecycle, (sample_rate,)).astype(np.int16))
	# Converts array into sound (via make_sound())
	sound = pygame.sndarray.make_sound(sine_wave(frqc))
	sound.play(-1) # Plays the sound
	pygame.time.delay(ms) # Pause for a given number of milliseconds
	sound.stop() # Stops the sound

def audioPlayMove(frqcCurrent):
	duration = int(1000) # Duration of audio in ms
	pygame.mixer.init(channels=1) # Sets audio to output in channel 1
	playAudio(frqcCurrent, duration)

def audioInputSeq(ls_moves):# Receives list of moves
	dict_frqcFilter = { # All of these values are in kHz
		'U': 1.55303,	'R': 2.28267,
		'F': 0.5034,	'D': 0.05034,
		'L': 0.15247,	'B': 1.0707	}
	ls_frqc = [float(dict_frqcFilter.get(moveCurrent) * 1000) for moveCurrent in ls_moves]
	for frqcCurrent in ls_frqc: audioPlayMove(frqcCurrent)

audioInputSeq(['B', 'R', 'B'])
