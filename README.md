# Minecraft Map

Create a simple Minecraft schematic map from your notes.

## Usage:

This is my current game's coordinates notes:
```
Spawn: 0 / 0 / 0
Village Home: -120 / 94 / -220
Farm: -93 / 92 / -208
Portal: -124 / 85 / -178
Iron Farm: -162 / 83 / -186

Broken Portal: 337 / 97 / -333
Zombie spawner: -22  / 23 / -366

Jungle pyramid: -630 / 64 / -857

Village2: -669 / 64 / -468

Small Hill Village: 606 / 109 / -216

Great Double Village3: 1487 / 76 / 300

Village4: 130 /79 /868
Ocean Monument: -200 / 62 / 745
Shipwreck: -107 / 62 / 691
```

After running `./mimap.py` you get this:
<center><img src="minecraft_map.png"></center>

# TODO
Usage improvements:

- [ ] `xsel | mimap.py -`
- [ ] `mimap.py myworld.md`
- [ ] specify output file name
- [ ] doc install & run using uv
- [ ] allow duplicate labels
- [ ] Z is drawn reversed
