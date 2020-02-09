### Imports prerequisites & libraries
import imgParse_colorCheck as colorCheck
import imgParse_runCamera as runCamera
import cubeGen_display as cubeDisplay

from variables import dict_colorFace

'''
Order of Kociemba algorithm input is in following order: URFDLB
'''

def main():
	#frame = cv2.imread("image_prescaled.jpg", cv2.IMREAD_COLOR)	# Debug purposes only
	result_combined, result_color = runCamera.runCamera()
	cubelets_0 = []   # Defines individual faces & its cubelets
	cubelets_1 = []
	for face in range(0, 3): # Runs for camera affiliated with URF faces
		cubelets_0.append([]) # Creates sublist for face
		print("Current face: " + str(face))
		for row in range(3):	# Loop to fill all rows/columns
			cubelets_0[face].append([]) # Creates sublist for rows
			for column in range(3):
				cubelets_0[face][row].append(
					dict_colorFace.get(
						colorCheck.verifyColor(	0, face, row, column,
												result_combined[0],
												result_color[0][0], result_color[0][1], 
												result_color[0][2], result_color[0][3],
												result_color[0][4], result_color[0][5]
												)))
	for face in range(0, 3): # Runs for camera affiliated with DLB faces
		cubelets_1.append([]) # Creates sublist for face
		for row in range(3):	# Loop to fill all rows/columns
			cubelets_1[face].append([]) # Creates sublist for rows
			for column in range(3):
				cubelets_1[face][row].append(
					dict_colorFace.get(
						colorCheck.verifyColor(	1, face, row, column,
												result_combined[1],
												result_color[1][0], result_color[1][1],
												result_color[1][2], result_color[1][3],
												result_color[1][4], result_color[1][5]
												)))
	cubelets = cubelets_0 + cubelets_1
	cubeDisplay.printCube(cubelets)
	print("Done!")
	
main()