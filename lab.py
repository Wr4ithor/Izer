import PIL
import numpy as np
from PIL import Image
from pathlib import Path

from constants import RGB_TO_XYZ, WHITE_POINT

# Temp path
# IMG = Path("tests/test.jpeg")
IMG = Path("tests/test1.jpg")


def _is_img_file(file: Path) -> bool:
    """Checks whether a file is an image file or not"""
    if not file.is_file():
        return False

    try:
        with Image.open(file) as img:
            img.verify()
        return True
    except (IOError, OSError, Image.UnidentifiedImageError):
        return False


def _open_image(path: Path) -> Image.Image:
    """Opens an image using Pillow"""
    if not path or not path.exists():
        raise ValueError(f"'{path}' doesn't exists")

    try:
        if not _is_img_file(path):
            raise ValueError(f"{path} is not an image")
        
        img = Image.open(path) # Opens an image
        img = img.convert('RGB')
        return img
    except (Image.UnidentifiedImageError, Exception) as e:
        raise e


def _img_to_rgb(image: Image.Image):
    """Converts a PIL object into NumPy array"""
    try:
        return np.asarray(image)
    except Exception as e:
        raise e


def _rgb_to_linear(rgb):
    rgb_norm = rgb / 255.0 # Normalising RGB
    # Gamma correction
    rgb_corr = np.where(
        rgb_norm <= 0.04045,
        rgb_norm / 12.92,
        ((rgb_norm + 0.055) / 1.055) ** 2.4
    )

    return rgb_corr


def _rgb_to_xyz(rgb):
    xyz = rgb @ RGB_TO_XYZ.T
    return xyz


def _xyz_to_lab(xyz):
    xyz_norm = xyz / WHITE_POINT # Normalising XYZ
    # Nonlinear transformation
    xyz_nlt = np.where(
        xyz_norm > 0.008856,
        xyz_norm ** (1/3),
        7.787 * xyz_norm + 16/116
    )

    # Splitting XYZ to X, Y and Z
    fx = xyz_nlt[..., 0]
    fy = xyz_nlt[..., 1]
    fz = xyz_nlt[..., 2]

    L = 116 * fy - 16
    a = 500 * (fx - fy)
    b = 200 * (fy - fz)

    # Stitching together X, Y and Z
    lab = np.stack((L, a, b), axis=-1)
    return lab


def rgb_to_lab(image_path: Path):
    image = _open_image(image_path)
    rgb = _img_to_rgb(image)
    rgb = _rgb_to_linear(rgb)

    # RGB to XYZ
    xyz = _rgb_to_xyz(rgb)

    # XYZ to Lab
    lab = _xyz_to_lab(xyz)

    return lab


lab = rgb_to_lab(IMG)
print(type(lab))
print(f"Size: {lab.size}")
print(f"Shape: {lab.shape}")
print(f"\n\n{lab[:1]}")
