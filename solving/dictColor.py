# Predefined color assignments corresponding to faces
# Defined by static cubelets in middle of face

dict_faceColor = {
        'U': 'B',   # Defines UP    as BLUE
        'R': 'R',   # Defines RIGHT as RED
        'F': 'W',   # Defines FRONT as WHITE
        'D': 'G',   # Defines DOWN  as GREEN
        'L': 'O',   # Defines LEFT  as ORANGE
        'B': 'Y'    # Defines BACK  as YELLOW
    }

dict_colorFace = dict((reversed(color) for color in dict_faceColor.items()))