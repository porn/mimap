#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#     "matplotlib",
#     "matplotlib-map-utils",
# ]
# ///

import sys
import re
import matplotlib.pyplot as plt
from matplotlib_map_utils.core.north_arrow import north_arrow
import matplotlib.font_manager as fm

# sample input for syncyng X & Z
input_data = """
Spawn: 0 / 0 / 0
Village Home: -120 / 94 / -220
Portal: -124 / 85 / -178

Underwater Vilage: -231 / 62 / 339

Underwater Vilage2: 90 / 62 / 712
South Treasure: -295 / 62 / 1447

Shipwreck2: -632 / 62 / 476
Outpost: -882 / 62 / 272

Underwater sand Village: -549 / 62 / 83
Underwater Portal: -326 / 62 / 106

Broken Portal: 337 / 97 / -333
Zombie spawner: -22  / 23 / -366

Jungle pyramid: -630 / 64 / -857

Village2: -669 / 64 / -468

Small Hill Village: 606 / 109 / -216

Great Double Village3: 1487 / 76 / 300
East Village: 1434 / 64 / -225
East Dry Shipwreck: 1034 / 67 / -608

Village4: 130 /79 /868
Ocean Monument: -200 / 62 / 745
Shipwreck: -107 / 62 / 691

South Underwater Village (2 sea lanterns): 1370 / 62 / 1127
Savana Village: 189 / 94 / -915

West Underwater village: -1155 / 62 / -500
West Beautiful Shipwreck: -1290 / 62 / -720
West Ocean Monument: -1290 / 62 / -187
West deep trasure: -1278 / 62 / 451
*Southwest shipwreck: -1403 / 63 / 1855
"""

LABEL_OFFSET=15
FIG_SIZE=10

# Read from stdin
# input_data = sys.stdin.read()

def main():
    locations = _extract_locations(input_data)

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

    # Save instead of show
    output_file = "minecraft_map.png"
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
