from . import generate
from . import scramble
#import display

# Generates & returns new (optionally scrambled) virtual cube
def obtainVirCube(isScrambled, scrambles=0):
	cubelets = generate.generate()
	if isScrambled == True: 
		#print(isScrambled)
		cubelets = scramble.scramble(cubelets, scrambles)
	return cubelets

#display.printCube(obtainVirCube(True, 4))