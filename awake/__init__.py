import argparse
import time
from datetime import datetime, timedelta
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version(__package__ or "awake")
except PackageNotFoundError:
    __version__ = "unknown"


import keyboard
import pyautogui
import pynput

pyautogui.FAILSAFE = False


class SessionLogger:
    """Handles session logging if enabled."""

    def __init__(self, enable_logging=True) -> None:
        """
        Initializes the SessionLogger.

        Parameters:
            enable_logging (bool): Enable session logging.
        """
        self.logging = enable_logging

        if self.logging:
            self.initialize_log()

    def initialize_log(self):
        """Creates and initializes the log file."""
        self.filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        with open(self.filename, "a") as file:
            file.write("datetime,is_stationary\n")

    def log(self, dt, is_stationary):
        """
        Logs the session details.

        Parameters:
            dt (datetime): Timestamp.
            is_stationary (bool): True if mouse is stationary, False otherwise.
        """
        if self.logging:
            with open(self.filename, "a") as file:
                file.write(f"{dt.isoformat()},{is_stationary}\n")

    def print(self, *args, **kwargs):
        """Prints the message if logging is enabled."""
        if self.logging or kwargs.get("_force", True):
            kwargs.pop("_force", None)
            print(*args, **kwargs)


class TimeKeeper:
    """Manages time and sleep-related operations."""

    def __init__(self, time_idle_to_wake, stop_time) -> None:
        """
        Initializes the TimeKeeper.

        Parameters:
            time_idle_to_wake (int): Time in seconds before mouse movement.
            stop_time (datetime): Stop time
        """
        self.time_idle_to_wake = time_idle_to_wake
        self.stop_time = self.parse_stop_time(stop_time)

        self.set_both()

    def is_sleep_in(self):
        """Check if it's time to wake up."""
        return self.now > self.awake

    def set_awake(self, *args):
        """Set the time to wake up."""
        self.awake = self.now + timedelta(seconds=self.time_idle_to_wake)

    def set_both(self):
        """Set both current time and wake-up time."""
        self.set_now()
        self.set_awake()

    def set_now(self):
        """Update the current time."""
        self.now = datetime.now()

    def set_last_idle(self):
        """Update the last idle time."""
        self.last_movement = datetime.now()

    def parse_stop_time(self, stop_time):
        """Parse stop time str and set stop_time."""
        if stop_time:
            date_format = "%y-%m-%d"
            now_date = datetime.now().strftime(date_format)

            try:
                stop_dt = datetime.strptime(
                    f"{now_date} {str(stop_time).zfill(4)}", f"{date_format} %H%M"
                )
            except ValueError as e:
                print(e)
                print("Invalid stop time format. Format hhmm/%h%m is required.")
                return None
            else:
                if stop_dt < datetime.now():
                    stop_dt += timedelta(days=1)
                return stop_dt
        else:
            return None

    def is_before_stop_time(self):
        if self.stop_time:
            return datetime.now() < self.stop_time
        else:
            return True


class Mouse:
    """Handles mouse-related operations."""

    def __init__(self, enable_multiscreen=True) -> None:
        """
        Initializes the Mouse.

        Parameters:
            enable_multiscreen (bool): Enable mouse movement to stay on current screen.
        """
        self.multiscreen = enable_multiscreen
        self.last_position = pyautogui.position()

    def is_stationary(self):
        """Check if the mouse is stationary."""
        result = self.last_position == pyautogui.position()
        self.last_position = pyautogui.position()
        return result

    def _get_start_position(self):
        """Calculate the starting position for mouse movement."""
        screen_size = pyautogui.size()
        return (
            (
                (self.last_position.x // screen_size[0]) * screen_size[1],
                (self.last_position.y // screen_size[0]) * screen_size[1],
            )
            if self.multiscreen
            else (0, 0)
        )

    def move_mouse(self):
        """Move the mouse required amount and press shift key."""
        start_position = self._get_start_position()
        for i in range(200):
            pyautogui.moveTo(start_position[0], start_position[1] + i * 4)
            if keyboard.is_pressed("esc"):
                break
        pyautogui.moveTo(*self.last_position)

        for i in range(3):
            pyautogui.press("shift")


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Prevents screen from sleeping by moving the mouse, pressing some keys following predefined idle period",
        epilog="See https://github.com/timothy-holmes/awake for docs and more info. Keeping the green dot alive!",
    )
    parser.add_argument(
        "-i",
        "--idle",
        default=60,
        type=int,
        help="time in seconds before mouse movement",
    )
    parser.add_argument(
        "-j",
        "--idle-res",
        default=10,
        type=int,
        help="time in seconds to pause during each loop",
    )
    parser.add_argument(
        "-l",
        "--log",
        default=False,
        action="store_true",
        help="enable session logging in ./YYYYmmddHHMMSS.csv",
    )
    parser.add_argument(
        "-m",
        "--multiscreen",
        default=True,
        action="store_true",
        help="enable mouse movement to stay on current screen",
    )
    parser.add_argument(
        "-s",
        "--stop-time",
        default=None,
        action="store",
        help="run awake until it's time to Pack 'Er Up Booiiizzzz! (format HHMM)",
    )
    parser.add_argument(
        "--version", action="version", version=f"{__package__} {__version__}"
    )
    return parser.parse_args()


def main():
    """Main execution function."""
    args = parse_arguments()

    logger = SessionLogger(args.log)
    times = TimeKeeper(args.idle, args.stop_time)
    mouse = Mouse(args.multiscreen)

    # Keyboard+mouse listeners
    keyboard.on_press(times.set_awake)
    mouse_listener = pynput.mouse.Listener(
        on_move=times.set_awake, on_click=times.set_awake, on_scroll=times.set_awake
    )
    mouse_listener.start()

    keyboard_listener = pynput.keyboard.Listener(on_press=times.set_awake)
    keyboard_listener.start()

    # Setup messages
    logger.print(
        f"{times.now.strftime('%H:%M:%S')}: Awake.py (version {__version__}). App started",
        _force=True,
    )

    if times.stop_time:
        logger.print(f"Stop time set {times.stop_time}", _force=True)

    # Keep awake
    while True:
        times.set_now()
        mouse_is_stationary = mouse.is_stationary()
        logger.log(times.now, mouse_is_stationary)

        if mouse_is_stationary:
            if times.is_sleep_in():
                logger.print(
                    f"{times.now.strftime('%H:%M:%S')}: Sleeping longer than {args.idle} seconds"
                )
                mouse.move_mouse()
                times.set_both()
        else:
            times.set_awake()

        time.sleep(args.idle_res)

        if not times.is_before_stop_time():
            logger.print(
                "Pack er up boooyyyzzzZ! (https://www.youtube.com/watch?v=riSrZOd_XfE)",
                _force=True,
            )
            break


if __name__ == "__main__":
    main()
