import numpy as np
from palettes import Palette, PaletteColor


def _validate_inputs(image: np.ndarray, palette: Palette) -> None:
    # If image is grayscale
    if image.ndim == 2:
        image = image[:, :, np.newaxis]

    if len(image.shape) != 3 or image.shape[2] != 3:
        raise ValueError(f"The image must be of the shape (H, W, 3). Got: {image.shape}")

    if len(palette.shape) != 2 or palette.lab.shape[1] != 3:
        raise ValueError(f"The palette must be of the shape (N, 3). Got: {palette.shape}")


def _flatten(image: np.ndarray) -> np.ndarray:
    return image.reshape(-1, 3)

