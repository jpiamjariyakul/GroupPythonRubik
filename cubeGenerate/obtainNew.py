from . import generate
from . import scramble
#import display

# Generates & returns new (optionally scrambled) virtual cube
def obtainVirCube(scrambles=0):
	cubelets = generate.generate()
	if scrambles != 0: 
		#print(isScrambled)
		cubelets = scramble.scramble(cubelets, scrambles)
	return cubelets