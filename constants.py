import numpy as np

RGB_TO_XYZ = np.array([
    [0.4124564, 0.3575761, 0.1804375],
    [0.2126729, 0.7151522, 0.0721750],
    [0.0193339, 0.1191920, 0.9503041],
], dtype=np.float64)

XYZ_TO_RGB = np.linalg.inv(RGB_TO_XYZ)

WHITE_POINT = np.array([
    0.95047,
    1.0,
    1.08883
])

DELTA = 6 / 29
EPSILON = DELTA ** 3
