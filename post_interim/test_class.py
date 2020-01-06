# URFDLB
class cube:
	tp_face = "URFDLB"
	dict_color = {}
	ls_face = [[None] for i in range(6)]
	def __init__(self, color):
		tempFace = face('U')
		for i in range(6):
			self.dict_color[self.tp_face[i]] = color[i]
			print(self.dict_color)
			self.ls_face[i] = face(color[i]).__class__
			print(self.ls_face[0].cubelet)

class face:
	cubelet = [[None] * 3 for i in range(3)]
	def __init__(self, color):
		self.cubelet[1][1] = color
		# Leave for now

test = cube("WROYGB")
print(test.ls_face[3].cubelet)