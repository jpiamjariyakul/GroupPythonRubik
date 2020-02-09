import kociemba
import random
from copy import deepcopy

class solving(object):
	def __init__(self):
		pass

	'''
	Convert color notation to face notation
	'''
	@staticmethod
	def convertColorToFace(self, cube_color):
		cube_face = []
		for face in range(6):
			cube_face.append([])
			for row in range(3):
				cube_face[face].append([])
				for column in range(3):
					cube_face[face][row].append(dict_colorFace.get(cube_color[face][row][column]))
		return cube_face

	'''
	Kociemba implementation
	'''
	# Parses cube list (including debug-generated) into single string
	# In order of Kociemba faces
	@staticmethod
	def parseCubeString(self, cube):
		str_cube = ""
		for face in range(6):
			for row in range(3):
				str_cube = str_cube + "".join(cube[face][row])
		return str_cube

	# Passes cubeString to Kociemba & return solving steps
	# Additionally un-parses results into list
	@staticmethod
	def solveCubeKoc(self, str_cube):
		str_kocSolve = kociemba.solve(str_cube).split(" ") # Removes white-spaces & places all Koc-output moves into list
		ls_kocSolve = []
		for moveSolve in str_kocSolve:
			if len(moveSolve) != 1:
				if moveSolve[1] == "'":
					ls_kocSolve.append((moveSolve[0], 3)) # Rotate thrice
				elif moveSolve[1] == "2":
					ls_kocSolve.append((moveSolve[0], 2)) # Rotate twice
			else: ls_kocSolve.append((moveSolve, 1)) # Rotate once
		return ls_kocSolve, str_kocSolve

class cubeGenerate(object):
	def __init__(self):
		pass

	@staticmethod
	def printCube(self, cube):
		gap = 18 * " "
		print(gap + str(cube[0][0]))
		print(gap + str(cube[0][1]))
		print(gap + str(cube[0][2]))
		print(17 * " " + + 17 * "-")
		print(str(cube[4][0]) + " | " + str(cube[2][0]) + " | " + str(cube[1][0]) + " | " + str(cube[5][0]))
		print(str(cube[4][1]) + " | " + str(cube[2][1]) + " | " + str(cube[1][1]) + " | " + str(cube[5][1]))
		print(str(cube[4][2]) + " | " + str(cube[2][2]) + " | " + str(cube[1][2]) + " | " + str(cube[5][2]))
		print(17 * " " + + 17 * "-")
		print(gap + str(cube[3][0]))
		print(gap + str(cube[3][1]))
		print(gap + str(cube[3][2]))

	# Generates full cube set, faces in URFDLB
	@staticmethod
	def generate(self):
		ls_faces = ("U", "R", "F", "D", "L", "B")
		cubelets = []
		for face in range(len(ls_faces)):
			cubelets.append([])
			for row in range(3):
				cubelets[face].append([])
				for column in range(3):
					cubelets[face][row].append(ls_faces[face])
		return cubelets

	# Generates & returns new (optionally scrambled) virtual cube
	@staticmethod
	def obtainVirCube(scrambles=0):
		cubelets = self.generate()
		if scrambles != 0: 
			cubelets = self.scramble(cubelets, scrambles)
		return cubelets

cubeClass = cubeGenerate()
cube = cubeClass.obtainVirCube()
cubeClass.printCube(cube)