import PIL
import numpy as np
from PIL import Image
from pathlib import Path

from constants import RGB_TO_XYZ, WHITE_POINT, DELTA, EPSILON, XYZ_TO_RGB

# Temp path
# IMG = Path("tests/test.jpeg")
IMG = Path("tests/test1.jpg")
IMG2 = Path("tests/test.jpeg")


def _img_to_rgb(image: Image.Image) -> np.ndarray:
    """Converts a PIL object into NumPy array"""
    try:
        return np.asarray(image, dtype=np.uint8)
    except Exception as e:
        raise e


def open_image(path: Path) -> np.ndarray:
    """Opens an image using Pillow"""
    if not path or not path.exists():
        raise ValueError(f"'{path}' doesn't exists")

    try:
        img = Image.open(path) # Opens an image
        img = img.convert('RGB')
        rgb = _img_to_rgb(img)
        return rgb
    except (Image.UnidentifiedImageError, Exception) as e:
        raise e


def _srgb_to_linear(rgb: np.ndarray) -> np.ndarray:
    rgb_norm = rgb / 255.0 # Normalising RGB
    # Gamma correction
    rgb_corr = np.where(
        rgb_norm <= 0.04045,
        rgb_norm / 12.92,
        ((rgb_norm + 0.055) / 1.055) ** 2.4
    )

    return rgb_corr


def _rgb_to_xyz(rgb: np.ndarray) -> np.ndarray:
    return rgb @ RGB_TO_XYZ.T


def _xyz_to_lab(xyz: np.ndarray) -> np.ndarray:
    xyz_norm = xyz / WHITE_POINT # Normalising XYZ
    # Nonlinear transformation
    xyz_nlt = np.where(
        xyz_norm > EPSILON,
        np.cbrt(xyz_norm),
        # 7.787 * xyz_norm + 16/116
        xyz_norm / (3 * DELTA**2) + 4/29
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


def rgb_to_lab(rgb: np.ndarray) -> np.ndarray:
    rgb = _srgb_to_linear(rgb)

    # RGB to XYZ
    xyz = _rgb_to_xyz(rgb)

    # XYZ to Lab
    lab = _xyz_to_lab(xyz)

    return lab


def _lab_to_xyz(lab: np.ndarray) -> np.ndarray:
    # Splitting Lab into L, a and b
    L = lab[..., 0]
    a = lab[..., 1]
    b = lab[..., 2]

    # Recover X, Y and Z
    fy = (L + 16) / 116
    fx = fy + a / 500
    fz = fy - b / 200

    xyz = np.stack((fx, fy, fz), axis=-1)

    # Undoing nonlinear transformation
    xyz = np.where(
        xyz > DELTA,
        xyz ** 3,
        (xyz - 16/116) / 7.787
    )

    xyz = WHITE_POINT * xyz
    return xyz 


def _xyz_to_rgb_linear(xyz: np.ndarray) -> np.ndarray:
    return xyz @ XYZ_TO_RGB.T


def _linear_to_rgb(rgb: np.ndarray) -> np.ndarray:
    rgb = np.clip(rgb, 0.0, None)
    # Inverse Gamma Correction
    rgb = np.where(
        rgb <= 0.0031308,
        rgb * 12.92,
        (1.055 * (np.power(rgb, 1/2.4))) - 0.055
    )

    rgb *= 255.0
    rgb = np.clip(rgb, 0, 255)
    return rgb.astype(np.uint8)


def lab_to_rgb(lab: np.ndarray) -> np.ndarray:
    xyz = _lab_to_xyz(lab)
    rgb = _xyz_to_rgb_linear(xyz)
    rgb = _linear_to_rgb(rgb)
    return rgb
