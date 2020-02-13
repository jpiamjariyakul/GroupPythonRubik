import PySimpleGUI as sg

def main():
	sg.theme('LightGreen')

	frame_cam_input = [
		[sg.Text("Click to run cameras", key="_textRunCam_"), sg.Button("Get", key="_get_"), sg.Button("Confirm", key="_confirm_", disabled=True)]
		]
	frame_cam_img = [	[	sg.Image(filename='', key='frame_0'),
							sg.Image(filename='', key='frame_1')	]	]
	frame_cam = [[sg.Frame("Howdy", frame_cam_input), sg.Frame("Boujour", frame_cam_img)]]
	# define the window layout
	layout = frame_cam

	# create the window and show it without the plot
	window = sg.Window('Demo Application - OpenCV Integration',
				layout,
				location=(800, 400),
				finalize=True)
	while True:
		event, values = window.read(timeout=0, timeout_key='timeout')
		if event == 'Exit' or event is None:
			break
	window.close()
main()