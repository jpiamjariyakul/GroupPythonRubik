### Imports prerequisites & libraries
import imgParse_colorCheck as colorCheck
import imgParse_getColor as camColor
import cubeGen_getNew as cubeDisplay

from variables import dict_colorFace

'''
Order of Kociemba algorithm input is in following order: URFDLB
'''

def verifyEachCamera(camera, result_combined, result_color):
	cubeletTemp = []
	for face in range(0, 3): # Runs for camera affiliated with URF faces
		cubeletTemp.append([]) # Creates sublist for face
		for row in range(3):	# Loop to fill all rows/columns
			cubeletTemp[face].append([]) # Creates sublist for rows
			for column in range(3):
				#print("camera = " + str(camera))
				cubeletTemp[face][row].append(
							colorCheck.verifyColor(	camera, face, row, column,
													result_combined[camera],
													result_color[camera][0], result_color[camera][1], 
													result_color[camera][2], result_color[camera][3],
													result_color[camera][4], result_color[camera][5]))
				#print(colorTemp)
				#cubeletTemp[face][row].append(dict_colorFace.get(colorTemp))
	return cubeletTemp

def cam_obtainCubelets(result_combined, result_color):
	cubelets = verifyEachCamera(0, result_combined, result_color) \
				 + verifyEachCamera(1, result_combined, result_color)
	return cubelets

def initCamera():
	#frame = cv2.imread("image_prescaled.jpg", cv2.IMREAD_COLOR)	# Debug purposes only
	result_combined, result_color = camColor.runCamera()
	cubelets = cam_obtainCubelets(result_combined, result_color)
	cubeDisplay.printCube(cubelets)
	return cubelets