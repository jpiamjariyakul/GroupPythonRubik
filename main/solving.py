#Algorithm of the code assuming:
# 1.Motor is turning CLOCKWISE for red with orange on the opposite side to combat the struggle of
#   the colour detection for detecting red and orange
# 2.Camera will take a screen-shot of one face, which could consist of a list of four colours
#   which is green, white, blue and yellow

'''
#	Defines test case given the following assumption:
#	1)	Red is the face that the motor turns, thus is not considered
#	2)	Hence, orange is also not considered since the opposite face of red is also thus hidden
#	3)	The cube is at its final stage & given 1 & 2 one knows the adjacent colors of the solved cube
#	4) Motor turns clockwise (looking into red/motor face/POV)
#	5)	Given 3, the adjacent colors are per following (looking in from red/motor face/POV):
#			Y
#		B	R	G	=>	[	B	->	Y	->	G	->	W	]
#			W
testCase = 	[	
				["B", "B", "B"]	,
				["G", "G", "G"]	,
				["G", "G", "G"]
			]
'''

def algorithmSolve(cubelets):
	#	Assumes all cubelets in row are the same color
	#	Steps taken:
	#	1)	Checks leftmost cubelet of middle row - per assumption the rightmost cubelet is also the same color (one does not check the middle face since it's connected to motor & thus is unnecessary)
	#	2)	Checks leftmost cubelet of top row - per assumption the rightmost cubelet is also the same cubelet, thus the middle cubelet is also the same color
	#	3)	Determine number of necessary turns required to match the top row with the middle row
	cubeletStatic = cubelets[1][0]
	cubeletMoving = cubelets[0][0]

	if cubeletStatic == "B":
		if cubeletMoving == "B":
			turn = 0
		elif cubeletMoving == "Y":
			turn = 1
		elif cubeletMoving == "G":
			turn = 2
		elif cubeletMoving == "W":
			turn = 3

	elif cubeletStatic == "Y":
		if cubeletMoving == "Y":
			turn = 0
		elif cubeletMoving == "G":
			turn = 1
		elif cubeletMoving == "W":
			turn = 2
		elif cubeletMoving == "B":
			turn = 3

	elif cubeletStatic == "G":
		if cubeletMoving == "G":
			turn = 0
		elif cubeletMoving == "W":
			turn = 1
		elif cubeletMoving == "B":
			turn = 2
		elif cubeletMoving == "Y":
			turn = 3

	elif cubeletStatic == "W":
		if cubeletMoving == "W":
			turn = 0
		elif cubeletMoving == "B":
			turn = 1
		elif cubeletMoving == "Y":
			turn = 2
		elif cubeletMoving == "G":
			turn = 3

	return turn

#n = algorithmSolve(testCase)
#print("Turns required: " + str(n))
