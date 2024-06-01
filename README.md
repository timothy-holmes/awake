# awake.py

```bash
python -m pip install pipx
pipx install https://github.com/timothy-holmes/awake.git
pipx ensurepath
# restart terminal to refresh env vars
awake --multiscreen --stop-time 1800
```

## What it does

- Moves mouse every 60 seconds to prevent screen saver from activating.
- Moves mouse along left edge of the screen, then back to original position.

## Command Line Options

All options are optional:

- `-i, --idle` - amou of idle time computer is idle before waking action (integer, default: 60)
- `-l, --log` - enable logging to file and stdout (default: disabled)
- `-m, --multiscreen` - move mouse on screen mouse is idle on (default: disabled)
- `-i, --interval` - time in seconds between mouse movements (integer, default: 60 seconds)
- `-s., --stop-time` - run awake until it's time to Pack 'Er Up Booooiiizzzz! (string with format HHMM, default: disabled)

## Limitations

- Multiscreen assumes screens are aligned horitontally and/or vertically.
- Multiscreen assumes screen sizes are the same.

## Minimum resoruce-consuming configuration

- Specify `--idle-res` constant (eg. 30, 60) in main function in script file (minimum of 25% of `IDLE_TIME` recommended).
- Ensure logging is disabled (default).

## Recommended usage

- Create a shortcut
- In Properties, set `Target` as `python "C:\Code\awake\awake.py"` (or whatever)
- Set `Start In` as `"C:\Code\awake\awake.py" --multiscreen` (or whatever)
- Set `Run` to `Minimized`
- Optional (danger): place shortcut in Start Menu Startup folder to have script run on logon (eg. C:\Users\useruser1\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup)
