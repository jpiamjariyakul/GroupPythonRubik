# Predefined color assignments corresponding to faces
# Defined by static cubelets in middle of face

dict_color = {
        'B': 'U',   # Defines UP    as BLUE
        'R': 'R',   # Defines RIGHT as RED
        'W': 'F',   # Defines FRONT as WHITE
        'G': 'D',   # Defines DOWN  as GREEN
        'O': 'L',   # Defines LEFT  as ORANGE
        'Y': 'B'    # Defines BACK  as YELLOW
    }

def convertColorToFace(cube_color):
    cube_face = []
    for face in range(6):
        cube_face.append([])
        for row in range(3):
            cube_face[face].append([])
            for column in range(3):
                cube_face[face][row].append(dict_color.get(cube_color[face][row][column]))
    return cube_face