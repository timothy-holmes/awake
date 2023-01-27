# awake

```
pip install pyautogui
python awake.py
```

Limitations:
- Relies on mouse movement only. App will wake after between `TIME_TO_WAKE` and `TIME_TO_WAKE + IDLE_RESOLUTION` seconds-ish of no mouse movement
- Manually moving mouse during 'wake' sequence has no effect. It will continue to move mouse down the side of the screen until it's finished. 

To reduce load (if that's a problem):
- reduce `IDLE_RESOLUTION` constant (eg. 30, 60)*
- comment out `logger.write(...)` statements
- comment out print statements

For bonus points, create a shortcut:
- set `Target` as `C:\Users\useruser1\AppData\Local\Programs\Python\Python310\python.exe C:\Code\awake\awake.py` (or whatever)
- set `Start In` as `C:\Code\awake\awake.py` (or whatever)
- set `Run` to `Minimized`
- optional (danger): place shortcut in Start Menu Startup folder to have script run on logon (eg. C:\Users\useruser1\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup) 
