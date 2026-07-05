import numpy as np
from palettes import Palette


def _validate_inputs(image: np.ndarray, palette: Palette) -> None:
    if len(image.shape) != 3 or image.shape[2] != 3:
        raise ValueError(f"The image must be of the shape (H, W, 3). Got: {image.shape}")

    if len(palette.lab.shape) != 2 or palette.lab.shape[1] != 3:
        raise ValueError(f"The palette must be of the shape (N, 3). Got: {palette.lab.shape}")


def _flatten(image: np.ndarray) -> np.ndarray:
    H, W, _ = image.shape # Storing original dimensions
    return image.reshape(-1, 3), H, W


def _calc_distances(image: np.ndarray, palette: np.ndarray) -> np.ndarray:
    # Current image shape: (H*W, 3)
    expanded = image[:, np.newaxis, :] # creates a "blank" space between H*X and 3,
    diff = expanded - palette.lab # Finds the difference between each pixel and each palette color
    sdiff = diff ** 2
    distance = np.sum(sdiff, axis=-1)
    return distance


def _map_colors(distance: np.ndarray, palette: Palette) -> np.ndarray:
    nearest_color = np.argmin(distance, axis=1)
    mapped_pixels = palette.lab[nearest_color]
    return mapped_pixels


def map_image(image: np.ndarray, palette: Palette, chunk_size: int = 8192) -> np.ndarray:
    _validate_inputs(image, palette)
    flat, H, W = _flatten(image)
    
    mapped = np.empty_like(flat)
    
    i = 0 # REMOVE THIS!!

    for start in range(0, len(flat), chunk_size):
        end = start + chunk_size
        chunk = flat[start:end]
        
        distance = _calc_distances(chunk, palette)
        mapped_chunk = _map_colors(distance, palette)

        mapped[start:end] = mapped_chunk
        i += 1
        print(f"Chunk: {i}")
    print("Done")
    return mapped.reshape(H, W, 3)


