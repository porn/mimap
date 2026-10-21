# AGENTS.md

This file provides guidance to coding agents working in this repository.

## Project Overview

mimap is a Minecraft map visualization tool that parses coordinates from markdown notes and generates a 2D map using matplotlib. It's a single-file Python script using uv's inline script dependencies feature.

## Architecture

**Single Script Design**: The entire application is contained in `mimap.py`. Its inline script metadata declares matplotlib, matplotlib-map-utils, and PyQt5 as dependencies.

**Core Flow**:
1. `_parse_args`: Determine input source and output destination.
2. `_load_input`: Load input data from a file or use sample data.
3. `_extract_locations` and `_parse_line`: Split text into names and integer coordinates.
4. `_draw_figure`: Render a matplotlib plot with markers, labels, and a north arrow.

**Coordinate System**: Uses Minecraft's coordinate system (X, Y, Z) but only plots X and Z for 2D visualization. `_extract_locations` discards Y, and `_draw_figure` inverts the vertical plot axis to match Minecraft's convention where north = decreasing Z.

**Input Format**: `_parse_line` expects `Name: X / Y / Z`, with integer coordinates, exactly one colon, and exactly three slash-separated coordinate values. `_extract_locations` skips blank lines and lines starting with `#`.

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

- `LABEL_OFFSET`: Label offset in map coordinate units; `_draw_figure` adds it to X and subtracts it from Z.
- `FIG_SIZE`: Width and height of the square figure in inches.
- `sample_input_data`: Hardcoded sample coordinates used by `_load_input` when the input filename is `*`.

## Special Behaviors

- `_parse_args`: With no arguments, prints usage information and continues with sample data and an interactive plot. `-h` or `--help` prints usage and exits with code 0; excess arguments cause exit code 1.
- `_load_input`: If the input file is not found, exits with code 1.
- `_extract_locations`: If no valid coordinates are parsed, exits with code 1. Otherwise, unparsed lines generate a warning suggesting the `#` prefix for comments.
- `_draw_figure`: When the output file is `-` or omitted, calls `plt.show()` to display an interactive plot. Otherwise, saves the figure to the supplied filename.
