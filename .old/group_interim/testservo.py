import numpy
import scipy.signal
import pygame, pygame.sndarray

frequency = 1/20
dutyCycle = 0.5

def PWM(t, frequency, dutyCycle):
    period = 1 / frequency
    pt = tt / period
    pt = tt * frequency # "period" time, where 1 unit is 1 period on the "real" time stamp.
    tc = pt - trunc(pt) # cycle time within 1 period. 0..1.
    return 1 if tc < dutyCycle else 0 # where 1 means on and 0 means off

def PWM(t, frequency, dutyCycle): #Filtering
    return dutyCycle

