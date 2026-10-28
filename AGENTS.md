# AGENTS.md

This file provides guidance to coding agents working in this repository.

## Project Overview

mimap is a Minecraft map visualization tool that parses coordinates from markdown notes and generates a 2D map using matplotlib. It's a single-file Python script using uv's inline script dependencies feature.

## Architecture

**Single Script Design**: The entire application is contained in `mimap.py`. Its inline script metadata declares matplotlib, matplotlib-map-utils, and PyQt5 as dependencies.

**Core Flow**:
1. `_parse_args`: Determine input source and output destination.
2. `_read_input_text`: Load input data from a file or use sample data.
3. `_parse_locations` and `_parse_location_line`: Split text into names and integer coordinates.
4. `main` creates the figure and calls `_render_map` to draw markers, labels, and a north arrow.
5. `main` calls `_save_map_png` for a one-time export or `_show_live_map` for an interactive map with input watching, then closes the figure on exit.

**Coordinate System**: Uses Minecraft's coordinate system (X, Y, Z) but only plots X and Z for 2D visualization. `_parse_locations` discards Y, and `_render_map` inverts the vertical plot axis to match Minecraft's convention where north = decreasing Z.

**Input Format**: `_parse_location_line` expects `Name: X / Y / Z`, with integer coordinates, exactly one colon, and exactly three slash-separated coordinate values. `_parse_locations` skips blank lines and lines starting with `#`.

## Running the Application

Using uv (recommended):
```bash
./mimap.py                              # Run with sample data, display interactive plot
./mimap.py notes.md                     # Parse notes.md, display plot
./mimap.py notes.md output.png          # Parse notes.md, save to output.png
./mimap.py "*" minecraft_map_new.png    # Use sample data, save to file
```

The executable script's shebang invokes `uv run`. The equivalent explicit command is:
```bash
uv run mimap.py [INPUT_FILE] [OUTPUT_FILE]
```

The bracketed arguments above are optional placeholders. Both forms use an isolated environment populated from the script's inline dependencies; no prior `uv sync` is required.

## Development Commands

**Install project dependencies**:
```bash
uv sync
```

This installs dependencies from `pyproject.toml` into the project environment. That manifest declares Python >=3.14, matplotlib, and matplotlib-map-utils; it does not declare PyQt5. The script's inline dependencies are managed separately when running `mimap.py` through uv.

**Run with specific input/output**:
```bash
# Test with sample data
./mimap.py "*" test_output.png
```

**Check the project environment**:
```bash
uv pip list  # Show packages in the project environment, not the script's isolated environment
```

## Key Configuration

- `LABEL_OFFSET`: Label offset in map coordinate units; `_render_map` adds it to X and subtracts it from Z.
- `FIG_SIZE`: Width and height of the square figure in inches.
- `sample_input_data`: Hardcoded sample coordinates used by `_read_input_text` when the input filename is `*`.

## Special Behaviors

- `_parse_args`: With no arguments, prints usage information and continues with sample data and an interactive plot. `-h` or `--help` prints usage and exits with code 0; excess arguments cause exit code 1.
- `_read_input_text`: Reads a file or returns sample data. Read errors propagate to the caller.
- `_parse_locations`: Raises `ValueError` if no valid coordinates are parsed. Otherwise, unparsed lines generate a warning suggesting the `#` prefix for comments.
- `main`: Initial input errors exit with code 1. Reload errors keep the last valid map.
- `main`: A file output saves PNG once and exits without watching. An omitted output or `-` opens an interactive map.
- `_save_map_png`: Saves PNG using an atomic file replacement.
- `_show_live_map`: Displays an interactive plot and checks for input changes every 500 ms using a GUI timer with a local callback. Changed input is processed after two consecutive identical reads, including invalid input only once per change. Sample data is not watched.
- `_update_map_view`: Redraws the map while preserving zoom and position and updating toolbar Home to fit current locations.
