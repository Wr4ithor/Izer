import numpy as np
from PIL import Image
from pathlib import Path


def open_image(path: Path) -> np.ndarray:
    """Opens an image using Pillow"""
    if not path or not path.exists():
        raise ValueError(f"'{path}' doesn't exist")

    try:
        with Image.open(path) as img: # Opens an image
            img = img.convert('RGB')
            return np.asarray(img)
    except (Image.UnidentifiedImageError, Exception) as e:
        raise e


def save_image(
        rgb_array: np.ndarray,
        dest_dir: Path = Path("results/"),
        name: str = "output",
        fmt: str = "png"
    ) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    path = dest_dir / f"{name}.{fmt}"

    try:
        Image.fromarray(rgb_array).save(path)
    except (Exception, OSError, FileIOError) as e:
        raise e
