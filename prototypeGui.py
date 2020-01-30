import PySimpleGUI as sg

'''
layout_1 =	[	[sg.Text('Some text on Row 1')],
				[sg.Text('Enter something on Row 2'), sg.InputText()],
				[sg.Button('Ok'), sg.Button('Cancel')]
			]
window = sg.Window('Window Title', layout_1)
while True:
	event, values = window.read()
	if event in (None, 'Cancel'):
		break
	print('You entered ', values[0])
window.close()
'''

#sg.theme('DarkAmber')	# Add a touch of color
def wrapStage1(isNotTerminated):
	print("Stage 1 initialised")
	layout_1 =	[	[sg.Text("Stage 1 - Image Parsing & Processing")],
					[sg.Text("Click OK once cube positions are in place")],
					[sg.Text("See OpenCV windows")],
					[sg.Button("OK"), sg.Button("Next"), sg.Button("Cancel")]
				]
	window_1 = sg.Window("Stage 1", layout_1)
	while True:
		event, values = window_1.read()
		if event in (None, "Cancel"):
			isNotTerminated = False
			break
		elif event in (None, "Next"):
			break
		elif event in (None, "OK"):
			print("OK Clicked")
	window_1.close()
	return isNotTerminated

def wrapStage2(isNotTerminated):
	print("Stage 2 initialised")
	layout_2 =	[	[sg.Text("Stage 2 - Solving Algorithm", key="_test_")],
					[sg.Text("Click OK once cube positions are in place")],
					[sg.Text("See OpenCV windows")],
					[sg.Button("OK"), sg.Button("Next"), sg.Button("Cancel")]
				]
	window_2 = sg.Window("Stage 2", layout_2)
	while True:
		event, values = window_2.read()
		if event in (None, "Cancel"):
			isNotTerminated = False
			break
		elif event in (None, "Next"):
			break
		elif event in (None, "OK"):
			print("OK Clicked")
			window_2["_test_"].update("Hello!")
	window_2.close()
	return isNotTerminated

def main():
	isNotTerminated = True
	while (isNotTerminated == True):
		isNotTerminated = wrapStage1(isNotTerminated)
		break
	while (isNotTerminated == True):
		isNotTerminated = wrapStage2(isNotTerminated)
		break

main()

