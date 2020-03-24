# Coord positions follow Kociemba convention
# NB: Coords in form (Y, X)
coord_yx =  (
			(	# Coordinates for the first camera
                (	# Pixels on face UP
                    (   (42,    150),   (62,    185),   (80,    228)    ),
                    (   (62,    115),   (80,    150),   (105,   190)    ),
                    (   (80,     72),   (105,   110),   (130,   150)    )   ),
                (	# Pixels on face RIGHT
                    (	(170,	170),	(142,	210),	(116,	246)	),
                    (   (208,	168),	(182,	206),	(150,	240)	),
                    (   (242,   170),	(214,	204),	(190,	236)	)   ),
                (	# Pixels on face FRONT
                    (   ( 116,	54),	(142,	90),	(170,	130)	),
                    (   ( 150,	60),	(182,	94),	(208,	132)	),
                    (   ( 190,	64),	(214,	96),	(242,	130)	)   )
			),
			(	#	Coordinates for the second camera
                (	# Pixels on face DOWN
                    (   (220,   228),   (238,   185),   (258,   150)    ),
                    (   (195,   190),   (220,   150),   (238,   115)    ),
                    (   (170,   150),   (195,   110),   (220,   72)     )   ),
                (	# Pixels on face LEFT
                    (	(58,	170),	(86,	204),	(110,	236)	),
                    (	(92,	168),	(118,	206),	(150,	240)	),
                    (	(130,	170),	(158,	210),	(184,	246)	)   ),
                (	# Pixels on face BACK
                    (   (110,   64),    (86,    96),    (58,    130)    ),
                    (   (150,   60),    (118,   94),    (92,    132)    ),
                    (	(184,	54),	(158,	90),	(130,	130)	)
                )
            )
		)

default_hsv = [ [	[0, 0, 176],		[34, 115, 255]	], 	# Bound of white
				[	[0, 132, 35],		[12, 255, 255]	],	# Bound of red_low
				[	[170, 50, 50],		[180, 255, 255]	],	# Bound of red_high
				[	[0, 173, 200],		[31, 237, 255]	],	# Bound of orange
				[	[16, 132, 194],		[100, 160, 255]	],	# Bound of yellow
				[	[45, 53, 88],		[91, 255, 255]	],	# Bound of green
				[	[101, 128, 128],	[150, 255, 255]	]	# Bound of blue
				]

# Predefined color assignments corresponding to faces
# Defined by static cubelets in middle of face

dict_faceColor = {
        'U': 'B',   # Defines UP    as BLUE
        'R': 'R',   # Defines RIGHT as RED
        'F': 'W',   # Defines FRONT as WHITE
        'D': 'G',   # Defines DOWN  as GREEN
        'L': 'O',   # Defines LEFT  as ORANGE
        'B': 'Y',   # Defines BACK  as YELLOW
        'X': 'X'    # Defines for any invalid values - placeholder
    }

dict_colorFace = dict((reversed(color) for color in dict_faceColor.items()))