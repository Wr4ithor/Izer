import argparse
from pathlib import Path
from palettes import available_palettes
from converter import orchestrate


main_parser = argparse.ArgumentParser(description="A Color Mapping Engine")
main_menu = main_parser.add_subparsers(dest="command", required=True, help="Available commands")

# Main parsers
run_parser = main_menu.add_parser("run", help="Run the Mapper Engine")

# Main arguments
run_parser.add_argument("path", help="An image file to process")
run_parser.add_argument("palette", help="The Palette to map the image to")
run_parser.add_argument("-o", "--output", type=Path, default=Path("results/"), help="Output dir")
run_parser.add_argument("-e", "--extension", choices=['png', 'jpg', 'jpeg', 'webp'],help="Processed output extension")
run_parser.add_argument("-c", "--chunk", type=int, default=8192, help="The size of a chunk to process at once")
run_parser.add_argument("-w", "--workers", type=int, default=1, help="Number of workers") # For future
run_parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

# Palette parsers
palette_parser = main_menu.add_parser("palette", help="Manage palette actions")
palette_menu = palette_parser.add_subparsers(dest="palette_cmd", required=True, help="Palette commands")

list_parser = palette_menu.add_parser("list", help="List all available color palettes")
# List palettes arguments
list_parser.add_argument("-d", "--detailed", action="store_true", help="Show detailed report")
list_parser.add_argument("-c", "--count", type=int, default=0, help="Number of palettes to show (from the top)")

show_palette = palette_menu.add_parser("show", help="Show a specific palette if available")
# Show palette arguments
show_palette.add_argument("name", help="Name of the palette")
show_palette.add_argument("-d", "--detailed", action="store_true", help="Show detailed report")

create_parser = palette_menu.add_parser("create", help="Create a new palette") # For future
remove_parser = palette_menu.add_parser("remove", help="Remove a color Palette") # For future
# Remove palette arguments
remove_parser.add_argument("-f", "--force", action="store_true", help="Ignore confirmation")

# args = main_parser.parse_args()


def handle_run(
        image_path: Path,
        palette: str,
        output: Path,
        name: str,
        fmt: str,
        chunk_size: int = 8192,
        workers: int = 1
    ) -> None:
    orchestrate(
        image_path=image_path,
        palette_name=palette,
        dest_dir=output,
        name=name,
        fmt=fmt,
        # workers=workers
        chunk_size=chunk_size
    )


def handle_palette_list(detailed: bool = False) -> None:
    print()
    for obj in available_palettes.values():
        if not detailed:
            if obj.family:
                print(f"● {obj.family} {obj.name}")
            else:
                print(f"● {obj.name}")
        else:
            if obj.family:
                print(f"● {obj.family} {obj.name}")
            else:
                print(f"● {obj.name}")
            print(f"    Number of Colors: {obj.size}\n")


def handle_palette_show(palette_name: str, detailed: bool = False) -> None:
    print()
    for obj in available_palettes.values():
        if palette_name.lower().strip() in (
            obj.name.lower().strip(),
            f"{obj.family}-{obj.name}".lower(),
            f"{obj.family}.{obj.name}".lower()
        ):
            print(f"● Palette Name: {obj.name}")
            print(f"● Palette Family: {obj.family}")
            print(f"● Number of Colors: {obj.size}\n")
                
            if detailed:
                print("● Colors:")
                for i, color in enumerate(obj.colors, 1):
                    print(f"    ({i}) Color Name: {color.name}")
                    print(f"        Color HEX: {color.hex}")
                    print(f"        Color RGB: {color.rgb}")
                    print(f"        Color Lab: {color.lab}\n")

