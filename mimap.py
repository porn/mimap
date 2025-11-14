#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#     "matplotlib",
#     "matplotlib-map-utils",
#     "PyQt5",
# ]
# ///
import sys
import re

import matplotlib.pyplot as plt
from matplotlib_map_utils.core.north_arrow import north_arrow

LABEL_OFFSET=15
FIG_SIZE=10

sample_input_data = """
Spawn: 0 / 0 / 0
Village Home: -120 / 94 / -220
Portal: -124 / 85 / -178
Zombie spawner: -22  / 23 / -366
Underwater Village: -231 / 62 / 339
Underwater Village2: 90 / 62 / 712
Shipwreck: -632 / 62 / 476
Outpost: -882 / 62 / 272
Underwater sand Village: -549 / 62 / 83
Underwater Portal: -326 / 62 / 106
"""


def main():
    input_filename, output_file = _parse_args(sys.argv)
    input_data = _load_input(input_filename)
    locations = _extract_locations(input_data)
    _draw_figure(locations, output_file)


def _parse_args(argv: list[str]) -> tuple[str, str]:
    # defaults
    input_filename = '*'  # use sample data
    output_filename = '-'  # draw using matplotlib

    program_name = argv[0]

    # no arguments given
    if len(argv) < 2:
        _print_usage(program_name)
        return input_filename, output_filename

    input_filename = argv[1]
    if input_filename in ['-h', '--help']:
        _print_usage(program_name)
        sys.exit(0)

    # only INPUT_FILE given
    if len(argv) == 2:
        return input_filename, output_filename

    # INPUT_FILE and OUTPUT_FILE given
    output_filename = argv[2]
    if len(argv) == 3:
        return input_filename, output_filename

    # more arguments given
    _print_usage(program_name)
    sys.exit(1)


def _print_usage(program_name):
    print(f"""
Minecraft Map builder.

Usage: {program_name} [INPUT_FILE] [OUTPUT_FILE]

Compile INPUT_FILE with coordinates into image. If INPUT_FILE is -, read from standard input. If no INPUT_FILE is given, then sample hard-coded data is used.

Optionally, you can provide OUTPUT_FILE as the name of the file to store image to (png format hardcoded). If no OUTPUT_FILE is given, then try to draw using matplotlib.
    """.strip())


def _load_input(input_filename: str) -> str:
    match input_filename:
        case "*":
            return sample_input_data

        case "-":
            return sys.stdin.read()

        case _:
            try:
                with open(input_filename) as f:
                    return f.read()
            except FileNotFoundError:
                print(f"Input file '{input_filename}' not found 😵")
                sys.exit(1)


def _draw_figure(locations, output_file):
    # Extract X/Z for plotting
    x = [coord[0] for coord in locations.values()]
    z = [coord[1] for coord in locations.values()]

    # Create plot
    fig, ax = plt.subplots(figsize=(FIG_SIZE, FIG_SIZE))
    ax.scatter(x, z, c="blue", marker="x")
    ax.yaxis.set_inverted(True)

    # Add labels
    for name, (x_coord, z_coord) in locations.items():
        ax.text(x_coord + LABEL_OFFSET, z_coord - LABEL_OFFSET, name, fontsize=8)

    # Titles & labels
    ax.set_title("Minecraft World Map")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Z Coordinate")
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True)

    # Add north arrow (Minecraft north = decreasing Z, so arrow points up)
    north_arrow(ax=ax, location="upper right", rotation={"degrees": 0})

    # Show or save image
    if output_file == '-':
        plt.show()
    else:
        plt.savefig(output_file, dpi=300, bbox_inches="tight")
        print(f"Map saved to: {output_file} 🌍")

def _extract_locations(input_data):
    nonempty_lines = []
    for line in input_data.strip().splitlines():
        if line.strip() == "":
            continue
        if line.startswith('#'):
            continue
        nonempty_lines.append(line)

    print(f"Found {len(nonempty_lines):,} lines, parsing... 🔍")

    # Regex to match "Name: X / Y / Z"
    pattern = re.compile(r"^(.*?):\s*(-?\d+)\s*/\s*(-?\d+)\s*/\s*(-?\d+)$")

    locations = {}
    for line in nonempty_lines:
        match = pattern.match(line.strip())
        if match:
            name, x, y, z = match.groups()
            locations[name.strip()] = (int(x), int(z))  # keep only X and Z

    if not locations:
        print("❌ No valid coordinates found. Make sure input format is: Name: X / Y / Z")
        sys.exit(1)

    print(f"Found {len(locations):,} locations ✅")

    if len(locations) != len(nonempty_lines):
        print(f"{len(nonempty_lines) - len(locations):,} row(s) weren't parsed 🔥")

    return locations


if __name__ == '__main__':
    main()
