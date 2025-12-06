# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

mimap is a Minecraft map visualization tool that parses coordinates from markdown notes and generates a 2D map using matplotlib. It's a single-file Python script using uv's inline script dependencies feature.

## Architecture

**Single Script Design**: The entire application is contained in `mimap.py` (mimap:1-178). The script uses uv's inline dependency specification (mimap.py:2-8) to manage matplotlib, matplotlib-map-utils, and PyQt5.

**Core Flow**:
1. Parse command-line arguments to determine input source and output destination (mimap.py:38-69)
2. Load input data from file, stdin, or use sample data (mimap.py:88-102)
3. Extract location coordinates from text using pattern matching (mimap.py:136-168)
4. Render matplotlib plot with markers, labels, and north arrow (mimap.py:105-134)

**Coordinate System**: Uses Minecraft's coordinate system (X, Y, Z) but only plots X and Z for 2D visualization (mimap.py:107-108, 152). Y-axis is inverted (mimap.py:113) to match Minecraft's convention where north = decreasing Z.

**Input Format**: Expects lines matching `Name: X / Y / Z` pattern (mimap.py:170-173). Lines starting with `#` are treated as comments and skipped (mimap.py:141-142).

## Running the Application

Using uv (recommended):
```bash
./mimap.py                              # Run with sample data, display interactive plot
./mimap.py notes.md                     # Parse notes.md, display plot
./mimap.py notes.md output.png          # Parse notes.md, save to output.png
./mimap.py - output.png                 # Read from stdin, save to output.png
./mimap.py "*" minecraft_map_new.png    # Use sample data, save to file
```

Traditional Python:
```bash
uv run mimap.py [INPUT_FILE] [OUTPUT_FILE]
```

## Development Commands

**Install dependencies**:
```bash
uv sync
```

**Run with specific input/output**:
```bash
# Test with sample data
./mimap.py "*" test_output.png

# Test with stdin
cat notes.md | ./mimap.py - output.png
```

**Check Python environment**:
```bash
uv pip list  # Show installed packages
```

## Key Configuration

- `LABEL_OFFSET`: Pixel offset for location labels (mimap.py:14)
- `FIG_SIZE`: Figure dimensions in inches (mimap.py:15)
- `sample_input_data`: Hardcoded test data (mimap.py:17-28)

## Special Behaviors

- If no arguments provided, displays usage information and shows interactive plot with sample data (mimap.py:49-51)
- If input file not found, exits with error code 1 (mimap.py:100-102)
- If no valid coordinates parsed, exits with error code 1 (mimap.py:156-158)
- Unparsed lines generate a warning suggesting to use `#` prefix for comments (mimap.py:162-166)
- When output file is `-` or not specified, shows interactive matplotlib window instead of saving (mimap.py:130-131)
