import PySimpleGUI as sg
import cv2
import numpy as np

"""
Demo program that displays a webcam using OpenCV and applies some very basic image functions
- functions from top to bottom -
none:	   no processing
threshold:  simple b/w-threshold on the luma channel, slider sets the threshold value
canny:	  edge finding with canny, sliders set the two threshold values for the function => edge sensitivity
contour:	colour finding in the frame, first slider sets the hue for the colour to find, second the minimum saturation
			for the object. Found objects are drawn with a red contour.
blur:	   simple Gaussian blur, slider sets the sigma, i.e. the amount of blur smear
hue:		moves the image hue values by the amount selected on the slider
enhance:	applies local contrast enhancement on the luma channel to make the image fancier - slider controls fanciness.
"""

	
def main():
	sg.theme('LightGreen')

	# define the window layout
	layout = [
	  	[sg.Text('OpenCV Demo', size=(40, 1), justification='center')],
	  	[sg.Image(filename='', key='image')	],
	  	[sg.Button('Exit', size=(10, 1))]
	]

	# create the window and show it without the plot
	window = sg.Window('Demo Application - OpenCV Integration',
				layout,
				location=(800, 400),
				finalize=True)

	cap = cv2.VideoCapture(0)
	while True:
		event, values = window.read(timeout=0, timeout_key='timeout')
		if event == 'Exit' or event is None:
			break

		ret, frame = cap.read()
		imgbytes = cv2.imencode('.png', frame)[1].tobytes()
		window['image'].update(data=imgbytes)

	window.close()

main()