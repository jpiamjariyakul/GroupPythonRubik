import cubeGen_generate as cg_g
import cubeGen_scramble as cg_s
import cubeGen_display as cg_d

# Generates & returns new (optionally scrambled) virtual cube
def obtainVirCube(scrambles=0):
	cubelets = cg_g.generate()
	if scrambles != 0: 
		#print(isScrambled)
		cubelets = cg_s.scramble(cubelets, scrambles)
	return cubelets

#cg_d.printCube(obtainVirCube(3))