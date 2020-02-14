import solving.kocSolve as kocSolve
import solving.colorFace as colorFace
import misc
import imageParse.colorCheck as colorCheck

'''
Testbench for testing kociemba functionality
'''

# cube_test = obtain_new.obtainVirCube(True, 4)
# Amend this array as you want - as long as it corresponds to the faces & colors everything should be g
# cube_test = [
#     [['L', 'F', 'F'], ['B', 'U', 'D'], ['D', 'D', 'L']], 
#     [['U', 'R', 'R'], ['B', 'R', 'L'], ['B', 'R', 'L']],
#     [['F', 'L', 'F'], ['B', 'F', 'U'], ['B', 'B', 'D']],
#     [['U', 'D', 'L'], ['F', 'D', 'U'], ['R', 'D', 'B']],
#     [['R', 'L', 'R'], ['F', 'L', 'R'], ['B', 'L', 'L']],
#     [['U', 'R', 'D'], ['U', 'B', 'U'], ['U', 'F', 'B']]
# ]

cube_test = [
    [['G', 'Y', 'W'], ['W', 'B', 'W'], ['W', 'O', 'Y']], 
    [['G', 'G', 'R'], ['B', 'R', 'B'], ['O', 'R', 'W']],
    [['O', 'G', 'R'], ['O', 'W', 'R'], ['R', 'Y', 'G']],
    [['B', 'B', 'W'], ['B', 'G', 'Y'], ['Y', 'R', 'G']],
    [['Y', 'O', 'B'], ['G', 'O', 'Y'], ['O', 'W', 'Y']],
    [['B', 'G', 'O'], ['O', 'Y', 'R'], ['R', 'W', 'B']]
]

#

cube_face = colorFace.convertColorToFace(cube_test)
misc.printCube(cube_face) # Expect gridded view of the faces
str_cube = kocSolve.parseCubeString(cube_face) # Parses such cube to Koc-compatible input string
print(str_cube)
print(kocSolve.solveCubeKoc(str_cube)) # Outputs list of moves required, in the following format: ('[face to turn]', [does face turn anti-clockwise?])