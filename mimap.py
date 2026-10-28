#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#     "matplotlib",
#     "matplotlib-map-utils",
#     "PyQt5",
# ]
# ///
import os
import sys
import tempfile
from pathlib import Path

from matplotlib import pyplot
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib_map_utils.core.north_arrow import north_arrow

LABEL_OFFSET = 15
FIG_SIZE = 10
RELOAD_INTERVAL_MS = 500

type Location = tuple[str, tuple[int, int]]
type Locations = list[Location]
type ViewLimits = tuple[tuple[float, float], tuple[float, float]]

sample_input_data = """
Spawn: 0 / 0 / 0
Village Home: -120 / 94 / -220
Portal: -124 / 85 / -178
Zombie spawner: -22  / 23 / -366
Underwater Village: -231 / 62 / 339
Underwater Village: 90 / 62 / 712
Shipwreck: -632 / 62 / 476
Outpost: -882 / 62 / 272
Underwater sand Village: -549 / 62 / 83
Underwater Portal: -326 / 62 / 106
"""


def main() -> None:
    input_filename, output_file = _parse_args(sys.argv)
    fig: Figure | None = None
    try:
        input_data = _read_input_text(input_filename)
        locations = _parse_locations(input_data)
        fig, ax = pyplot.subplots(figsize=(FIG_SIZE, FIG_SIZE))
        _render_map(ax, locations)
        if output_file == '-':
            _show_live_map(fig, ax, input_filename, input_data)
        else:
            _save_map_png(fig, output_file)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"❌ {error}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        pass
    finally:
        if fig is not None:
            pyplot.close(fig)


def _parse_args(argv: list[str]) -> tuple[str, str]:
    """
    >>> _parse_args(['mimap.py'])  # doctest: +ELLIPSIS
    Minecraft Map builder.
    ...
    ('*', '-')
    >>> _parse_args(['mimap.py', 'notes.md'])
    ('notes.md', '-')
    >>> _parse_args(['mimap.py', 'notes.md', 'output.png'])
    ('notes.md', 'output.png')
    >>> _parse_args(['mimap.py', '*', 'output.png'])
    ('*', 'output.png')
    """
    program_name = argv[0]
    arguments = argv[1:]

    if not arguments:
        _print_usage(program_name)
        return '*', '-'

    if arguments[0] in ('-h', '--help'):
        _print_usage(program_name)
        sys.exit(0)

    if len(arguments) > 2:
        _print_usage(program_name)
        sys.exit(1)

    input_filename = arguments[0]
    output_filename = arguments[1] if len(arguments) == 2 else '-'
    return input_filename, output_filename


def _print_usage(program_name: str) -> None:
    print(f"""
Minecraft Map builder.

Usage: {program_name} [INPUT_FILE] [OUTPUT_FILE]

Compile INPUT_FILE with coordinates into image. If no INPUT_FILE is given, then
sample hard-coded data is used.

Optionally, you can provide OUTPUT_FILE as the name of the file to store image
to (png format hardcoded). The image is saved once and the program exits.
If OUTPUT_FILE is omitted or '-', display an interactive matplotlib map.

Only interactive maps watch input files, checking every 500 ms.
Close the plot or press Ctrl+C to stop. Sample data is rendered once.
    """.strip())


def _read_input_text(input_filename: str) -> str:
    if input_filename == "*":
        return sample_input_data

    return Path(input_filename).read_text()


def _render_map(ax: Axes, locations: Locations) -> None:
    # Extract X/Z for plotting
    x = [coord[0] for _, coord in locations]
    z = [coord[1] for _, coord in locations]

    ax.clear()
    ax.scatter(x, z, c="blue", marker="x")
    ax.yaxis.set_inverted(True)

    # Add labels
    for name, (x_coord, z_coord) in locations:
        ax.text(x_coord + LABEL_OFFSET, z_coord - LABEL_OFFSET, name, fontsize=8)

    # Include label anchors in the map extent, even for a single point at zero.
    label_positions = [(x_coord + LABEL_OFFSET, z_coord - LABEL_OFFSET)
                       for x_coord, z_coord in zip(x, z)]
    ax.update_datalim(label_positions)
    ax.autoscale_view()

    # Titles & labels
    ax.set_title("Minecraft World Map")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Z Coordinate")
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True)

    # Add north arrow (Minecraft north = decreasing Z, so arrow points up)
    north_arrow(ax=ax, location="upper right", rotation={"degrees": 0})


def _save_map_png(fig: Figure, output_file: str) -> None:
    destination = Path(output_file)
    # Keep readers from seeing an incomplete PNG. Use the same filesystem so
    # replacement is atomic, and clean up even when rendering fails.
    descriptor, temporary = tempfile.mkstemp(
        dir=destination.absolute().parent,
        suffix=".png",
    )
    os.close(descriptor)
    try:
        fig.savefig(temporary, format="png", dpi=300, bbox_inches="tight")
        os.replace(temporary, destination)
    finally:
        Path(temporary).unlink(missing_ok=True)
    print(f"Map saved to: {output_file} 🌍")


def _update_map_view(
    ax: Axes, locations: Locations, home_limits: ViewLimits,
) -> ViewLimits:
    """Redraw the map, preserving a custom view and updating toolbar Home."""
    current_limits = (ax.get_xlim(), ax.get_ylim())
    zoomed = current_limits != home_limits
    _render_map(ax, locations)
    home_limits = (ax.get_xlim(), ax.get_ylim())

    toolbar = ax.figure.canvas.toolbar
    if toolbar is not None:
        toolbar.update()
        toolbar.push_current()

    if zoomed:
        ax.set_xlim(current_limits[0])
        ax.set_ylim(current_limits[1])
        if toolbar is not None:
            toolbar.push_current()

    ax.figure.canvas.draw_idle()
    return home_limits


def _show_live_map(
    fig: Figure, ax: Axes, input_filename: str, input_data: str,
) -> None:
    """Watch input and update the map on the GUI thread until the window closes."""
    if input_filename == '*':
        pyplot.show()
        return

    processed_data = input_data
    pending_data: str | None = None
    last_error: str | None = None
    home_limits = (ax.get_xlim(), ax.get_ylim())

    def check_for_changes() -> None:
        nonlocal processed_data, pending_data, last_error, home_limits
        try:
            data = _read_input_text(input_filename)
            if data == processed_data:
                pending_data = None
                last_error = None
                return
            # Require two consecutive identical reads before processing a save.
            if data != pending_data:
                pending_data = data
                return

            # Remember invalid input too, so it is parsed only once per change.
            processed_data = data
            pending_data = None
            locations = _parse_locations(data)
            home_limits = _update_map_view(ax, locations, home_limits)
            last_error = None
        except (OSError, UnicodeError, ValueError) as error:
            pending_data = None
            message = str(error)
            if message != last_error:
                print(f"Reload failed: {message}. Keeping the last map.", file=sys.stderr)
                last_error = message

    timer = fig.canvas.new_timer(interval=RELOAD_INTERVAL_MS)
    timer.add_callback(check_for_changes)
    fig.canvas.mpl_connect('close_event', lambda event: timer.stop())
    print(f"Watching {input_filename} (every {RELOAD_INTERVAL_MS} ms).")
    timer.start()
    try:
        pyplot.show()
    finally:
        timer.stop()


def _parse_locations(input_data: str) -> Locations:
    nonempty_lines = []
    for line in input_data.strip().splitlines():
        if line.strip() == "":
            continue
        if line.startswith('#'):
            continue
        nonempty_lines.append(line)

    print(f"Found {len(nonempty_lines):,} lines, parsing... 🔍")

    unparsed_lines = []
    locations = []
    for line in nonempty_lines:
        try:
            name, x, _, z = _parse_location_line(line)
            locations.append((name, (x, z)))  # keep only X and Z
        except ValueError:
            unparsed_lines.append(line)

    if not locations:
        raise ValueError("No valid coordinates found. Make sure input format is: Name: X / Y / Z")

    print(f"Found {len(locations):,} locations ✅")

    if unparsed_lines:
        print(f"🔥 {len(unparsed_lines):,} unparsed line(s) found:")
        for line in unparsed_lines:
            print(line)
        print("\nNOTE: you can prefix comments with # symbol to get rid of this warning ✏️️")

    return locations


def _parse_location_line(line: str) -> tuple[str, int, int, int]:
    name, coords = line.split(":")
    x, y, z = map(int, coords.split("/"))

    return name.strip(), x, y, z


if __name__ == '__main__':
    main()
