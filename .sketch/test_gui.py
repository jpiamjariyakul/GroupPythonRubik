import PySimpleGUI as sg

#sg.theme('DarkAmber')	# Add a touch of color

# All the stuff inside your window.
layout_1 = [  [sg.Text('Some text on Row 1')],
			[sg.Text('Enter something on Row 2'), sg.InputText()],
			[sg.Button('Ok'), sg.Button('Cancel')] ]

# Create the Window
window_1 = sg.Window('Window Title', layout_1)
# Event Loop to process "events" and get the "values" of the inputs
while True:
	event, values = window_1.read()
	if event in (None, 'Cancel'):	# if user closes window or clicks cancel
		break
	print('You entered ', values[0])
window_1.close()

'''
'''

# All the stuff inside your window.
layout_2 = [  [sg.Text('Some text on Row 3')],
			[sg.Text('Enter something on Row 4'), sg.InputText()],
			[sg.Button('Test'), sg.Button('End')] ]

# Create the Window
window_2 = sg.Window('Window Title', layout_2)
# Event Loop to process "events" and get the "values" of the inputs
while True:
	event, values = window_2.read()
	if event in (None, 'End'):	# if user closes window or clicks cancel
		break
	print('You entered ', values[0])
window_2.close()