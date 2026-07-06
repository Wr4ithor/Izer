from pathlib import Path
from mapper import map_image
from imageio import open_image, save_image
from lab import rgb_to_lab, lab_to_rgb
from palettes import available_palettes


def orchestrate(image_path: Path, palette_name: str) -> None:
    if not palette_name.lower() in available_palettes.keys():
        raise ValueError(f"Palette {palette_name} not supported")
    else:
        palette = available_palettes[palette_name]

    rgb = open_image(image_path)
    lab = rgb_to_lab(rgb)

    mapped_lab = map_image(lab, palette)
    mapped_rgb = lab_to_rgb(mapped_lab)
    
    save_image(mapped_rgb)
