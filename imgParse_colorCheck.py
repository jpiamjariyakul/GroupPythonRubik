import numpy as np
from variables import coord_yx
from variables import dict_faceColor
### Declares faces visible to camera & to be analysed
# Tuple storing pixels to check in image - amended later to accommodate rig
# NB: OpenCV uses a (Y,X) coordinate system
# Concerns interim submision - detects only one face

'''
Order of Kociemba algorithm input is in following order: URFDLB
One sets UP color as WHITE - change according to necessary
'''

# Defines color at coordinates given
def checkColor(	hsv_combined,
				hsv_white, hsv_red, hsv_orange,
				hsv_yellow, hsv_green, hsv_blue):
	# Only uses array values & not the images themselves
	if np.any(hsv_combined == hsv_blue): return "B"
	elif np.any(hsv_combined == hsv_white): return "W"
	elif np.any(hsv_combined == hsv_red): return "R"
	elif np.any(hsv_combined == hsv_orange): return "O"
	elif np.any(hsv_combined == hsv_yellow): return "Y"
	elif np.any(hsv_combined == hsv_green): return "G"


# Verifies color at pixel & its surroundings whether it's black or otherwise
def verifyColor(	camera, face, row, column, c_combined,
					c_white, c_red, c_orange,
					c_yellow, c_green, c_blue):
	coord_row, coord_col = coord_yx[camera][face][row][column][0], coord_yx[camera][face][row][column][1]
	#print("XY [" + str(face) + " " + str(row) + " " + str(column) + "]: (" + str(coord_row) + ", " + str(coord_col) + ")")
	#print("Found on first attempt: " + str(np.any(c_combined[coord_row][coord_col] != 0)))
	# Check if at specified coords there are colors
	if (row == 1) and (column == 1): 
		# In case of middle cubelet, one can simply assume color has been pre-assigned
		# Such middke cubelets' faces are goals for which the surrounding cubelets are to match
		if camera == 0:
			if face == 0: color = dict_faceColor.get("U")
			elif face == 1: color = dict_faceColor.get("R")
			elif face == 2: color = dict_faceColor.get("F")
		elif camera == 1:
			if face == 0: color = dict_faceColor.get("D")
			elif face == 1: color = dict_faceColor.get("L")
			elif face == 2: color = dict_faceColor.get("B")
	else:
		if np.any(c_combined[coord_row][coord_col] != 0):
			# Passes HSV values instead of the images
			color = checkColor(	c_combined[coord_row][coord_col],	\
								c_white[coord_row][coord_col], 		\
								c_red[coord_row][coord_col], 		\
								c_orange[coord_row][coord_col], 	\
								c_yellow[coord_row][coord_col], 	\
								c_green[coord_row][coord_col], 		\
								c_blue[coord_row][coord_col])
			#print("Color at (" + str(coord_row) + ", " + str(coord_col) + "): " + str(color))
			#print("------------------------")
		else: # Otherwise, iterate through 2 layers	until color found, or error
			layerMax = 3 # Max number of iterational layers to expand from original point
			i = j = -1 * layerMax
			i_initial = i
			while (True):
				if np.any(c_combined[coord_row + j][coord_col + i] != 0) and (i != 0) and (j != 0):
					color = checkColor(	c_combined[coord_row + j][coord_col + i],	\
										c_white[coord_row + j][coord_col + i], 		\
										c_red[coord_row + j][coord_col + i], 		\
										c_orange[coord_row + j][coord_col + i], 	\
										c_yellow[coord_row + j][coord_col + i], 	\
										c_green[coord_row + j][coord_col + i], 		\
										c_blue[coord_row + j][coord_col + i])
					#print("Color at (" + str(coord_row + j) + ", " + str(coord_col + i) + "): " + str(color))
					#print("------------------------")
					break
				else:
					#print("!!! - Invalid color at " + str(coord_row + j) + ", " + str(coord_col + i) + " - adding range")
					if i >= layerMax:
						i = i_initial
						j += 1
					else: i += 1
					if j >= layerMax:
						color = "X"
						#print("ERROR - color undefined")
						#print("------------------------")
						break
	return color