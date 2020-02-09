from .variables import dict_colorFace

def convertColorToFace(cube_color):
    cube_face = []
    for face in range(6):
        cube_face.append([])
        for row in range(3):
            cube_face[face].append([])
            for column in range(3):
                cube_face[face][row].append(dict_colorFace.get(cube_color[face][row][column]))
    return cube_face