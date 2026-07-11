import numpy as np
from lab import rgb_to_lab
from dataclasses import dataclass


@dataclass(frozen=True)
class PaletteColor:
    name: str
    hex: str
    rgb: tuple[int, int, int]
    lab: np.ndarray


@dataclass(frozen=True)
class Palette:
    name: str
    family: str | None
    colors: list[PaletteColor]
    rgb: np.ndarray
    lab: np.ndarray

    def names(self) -> list[str]:
        return [c.name for c in self.colors]

    def get(self, name: str) -> PaletteColor:
        for color in self.colors:
            if color.name.lower() == name.lower():
                return color


    def __len__(self):
        return len(self.colors)

    @property
    def size(self) -> int:
        return len(self.colors)


def _hex_to_rgb(hex_val: str) -> tuple[int, int, int]:
    clean_hex = hex_val.lstrip('#')
    return (
        int(clean_hex[0:2], 16),
        int(clean_hex[2:4], 16),
        int(clean_hex[4:6], 16)
    )


def _build_palette(theme_name: str, theme_family: str, theme_colors: dict[str, str]) -> Palette:
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
    
    rgb = np.array([color.rgb for color in colors], dtype=np.uint8)
    lab = np.array([color.lab for color in colors], dtype=np.float64)

    return Palette(name=theme_name, family=theme_family, colors=colors, rgb=rgb, lab=lab)

# ---- PALETTES ----
# Catppuccin
MOCHA_RAW = {
    # Base colors (backgrounds)
    "base": "#1e1e2e",
    "mantle": "#181825",
    "crust": "#11111b",
    
    # Surface colors
    "surface0": "#313244",
    "surface1": "#45475a",
    "surface2": "#585b70",
    
    # Overlay colors
    "overlay0": "#6c7086",
    "overlay1": "#7f849c",
    "overlay2": "#9399b2",
    
    # Text colors
    "text": "#cdd6f4",
    "subtext0": "#a6adc8",
    "subtext1": "#bac2de",
    
    # Accent colors
    "rosewater": "#f5e0dc",
    "flamingo": "#f2cdcd",
    "pink": "#f5c2e7",
    "mauve": "#cba6f7",
    "red": "#f38ba8",
    "maroon": "#eba0ac",
    "peach": "#fab387",
    "yellow": "#f9e2af",
    "green": "#a6e3a1",
    "teal": "#94e2d5",
    "sky": "#89dceb",
    "sapphire": "#74c7ec",
    "blue": "#89b4fa",
    "lavender": "#b4befe",
}


LATTE_RAW = {
    # Base colors (backgrounds)
    "base": "#eff1f5",
    "mantle": "#e6e9ef",
    "crust": "#dce0e8",
    
    # Surface colors
    "surface0": "#ccd0da",
    "surface1": "#bcc0cc",
    "surface2": "#acb0be",
    
    # Overlay colors
    "overlay0": "#9ca0b0",
    "overlay1": "#8c8fa1",
    "overlay2": "#7c7f93",
    
    # Text colors
    "text": "#4c4f69",
    "subtext0": "#6c6f85",
    "subtext1": "#5c5f77",
    
    # Accent colors
    "rosewater": "#dc8a78",
    "flamingo": "#dd7878",
    "pink": "#ea76cb",
    "mauve": "#8839ef",
    "red": "#d20f39",
    "maroon": "#e64553",
    "peach": "#fe640b",
    "yellow": "#df8e1d",
    "green": "#40a02b",
    "teal": "#179299",
    "sky": "#04a5e5",
    "sapphire": "#209fb5",
    "blue": "#1e66f5",
    "lavender": "#7287fd",
}

MOCHA = _build_palette("Mocha", "Catppuccin", MOCHA_RAW)
LATTE = _build_palette("Latte", "Catppuccin", LATTE_RAW)

available_palettes = {
    "catppuccin-mocha": MOCHA,
    "catppuccin-latte": LATTE
}
