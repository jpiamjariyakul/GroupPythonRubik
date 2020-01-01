# import kocSolve
import display

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

def convertColorToFace(cube_color, dict_color):
    cube_face = []
    for face in range(6):
        cube_face.append([])
        for row in range(3):
            cube_face[face].append([])
            for column in range(3):
                cube_face[face][row].append(dict_color.get(cube_color[face][row][column]))
    return cube_face

cube_test = [
    [['G', 'Y', 'W'], ['W', 'B', 'W'], ['W', 'O', 'Y']], 
    [['G', 'G', 'R'], ['B', 'R', 'B'], ['O', 'R', 'W']],
    [['O', 'G', 'R'], ['O', 'W', 'R'], ['R', 'Y', 'G']],
    [['B', 'B', 'W'], ['B', 'G', 'Y'], ['Y', 'R', 'G']],
    [['Y', 'O', 'B'], ['G', 'O', 'Y'], ['O', 'W', 'Y']],
    [['B', 'G', 'O'], ['O', 'Y', 'R'], ['R', 'W', 'B']]
]

# Predefined color assignments corresponding to faces
# Defined by static cubelets in middle of face
dict_color ={
    'B': 'U',   # Defines UP    as BLUE
    'R': 'R',   # Defines RIGHT as RED
    'W': 'F',   # Defines FRONT as WHITE
    'G': 'D',   # Defines DOWN  as GREEN
    'O': 'L',   # Defines LEFT  as ORANGE
    'Y': 'B'    # Defines BACK  as YELLOW
}


cube_face = convertColorToFace(cube_test, dict_color)
display.printCube(cube_face) # Expect gridded view of the faces
str_cube = kocSolve.parseCubeString(cube_face) # Parses such cube to Koc-compatible input string
print(str_cube)
print(kocSolve.solveCubeKoc(str_cube)) # Outputs list of moves required, in the following format: ('[face to turn]', [does face turn anti-clockwise?])