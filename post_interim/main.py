### Imports prerequisites & libraries
import cv2 as cv2
import numpy as np
import colorDetect.checkColor as color
import openCV.runCamera as runCamera

'''
Order of Kociemba algorithm input is in following order: URFDLB
'''

# Creates a resizable window frame - one loads video/image into it
#cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
# Program functions perfectly normal w/out line in

def main():
	"""Stage 1.1: Obtain masks for each individual color in image"""
	#frame = cv2.imread("image_prescaled.jpg", cv2.IMREAD_COLOR)	# Debug purposes only
	result_combined, result_color = runCamera.runCamera(cv2, np, color.coord_yx)
	#n = solving.algorithmSolve(cubelets)
	# n = 0
	#print("File written")
	cubelets = []   # Defines individual faces & its cubelets
	for face in range(3):
		cubelets.append([]) # Creates sublist for face
		for row in range(3):	# Loop to fill all rows/columns
			cubelets[face].append([]) # Creates sublist for rows
			for column in range(3):
				cubelets[face][row].append(color.verifyColor(	face, row, column, result_combined,
																result_color[0], result_color[1], result_color[2],
																result_color[3], result_color[4], result_color[5]
																))
	print(str(cubelets[0][0]) + " | " + str(cubelets[1][0]) + " | " + str(cubelets[2][0]))
	print(str(cubelets[0][1]) + " | " + str(cubelets[1][1]) + " | " + str(cubelets[2][1]))
	print(str(cubelets[0][2]) + " | " + str(cubelets[1][2]) + " | " + str(cubelets[2][2]))
	print("Done!")
main()