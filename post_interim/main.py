### Imports prerequisites & libraries
import colorDetect.checkColor as color
import openCV.runCamera as runCamera

'''
Order of Kociemba algorithm input is in following order: URFDLB
'''

def main():
	#frame = cv2.imread("image_prescaled.jpg", cv2.IMREAD_COLOR)	# Debug purposes only
	result_combined, result_color = runCamera.runCamera(color.coord_yx)
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