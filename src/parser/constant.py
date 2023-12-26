END_OF_SHAPE = 0
PEN_DOWN = 1
PEN_UP = 2
DIVIDE_VECTOR = 3
MULTIPLY_VECTOR = 4
PUSH_STACK = 5
POP_STACK = 6
DRAW_SUBSHAPE = 7
XY_DISPLACEMENT = 8
POLY_XY_DISPLACEMENT = 9  # 0,0 terminated
OCTANT_ARC = 0xA
FRACTIONAL_ARC = 0xB  # 5 bytes, start, end, high radius, radius, ±0SC
BULGE_ARC = 0xC  # dx, dy, bulge
POLY_BULGE_ARC = 0xD  # 0,0 terminated BULGE_ARC
COND_MODE_2 = 0x0E  # PROCESS this command *only if mode=2*