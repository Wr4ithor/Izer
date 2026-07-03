import numpy as np
from lab import rgb_to_lab
from typing import Dict, Tuple
from dataclasses import dataclass


@dataclass(frozen=True)
class PaletteColor:
    name: str
    hex: str
    rgb: Tuple[int, int, int]
    lab: np.ndarray


@dataclass(frozen=True)
class Palette:
    name: str
    colors: list[PaletteColor]


def _hex_to_rgb(hex: str) -> Tuple[int, int, int]:
    clean_hex = hex.lstrip('#')
    return (
        int(clean_hex[0:2], 16),
        int(clean_hex[2:4], 16),
        int(clean_hex[4:6], 16)
    )


def _build_palette(theme_name: str, theme_colors: Dict[str, str]) -> Palette:
    colors = []
    for color_name, color_hex in theme_colors.items():
        rgb = _hex_to_rgb(color_hex)
        lab = rgb_to_lab(np.array(rgb))

        color = PaletteColor(
            name=color_name,
            hex=color_hex,
            rgb=rgb,
            lab=lab
        )

        colors.append(color)

    return Palette(name=them_name, colors=colors)


