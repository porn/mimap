# Minecraft Map

Create a simple Minecraft schematic map from your notes.

## Usage:

This is a sample game's coordinates notes:
```markdown
# home area
Spawn: 0 / 0 / 0
Village Home: -120 / 94 / -220
Portal: -124 / 85 / -178

# mines
Zombie spawner: -22  / 23 / -366

# my first sea trip
Underwater Village: -231 / 62 / 339
Underwater Village2: 90 / 62 / 712
Shipwreck: -632 / 62 / 476
Outpost: -882 / 62 / 272
Underwater sand Village: -549 / 62 / 83
Underwater Portal: -326 / 62 / 106
```

After running `./mimap.py` you get this:
<center><img src="minecraft_map.png"></center>

# TODO
Usage improvements:
- [ ] output filename based on input file name, or some sane default for stdin and sample data
- [ ] doc install & run using uv
- [ ] file watch? 🤔
- [ ] dynamic `LABEL_OFFSET`
