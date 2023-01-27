import time
from datetime import datetime, timedelta

import pyautogui
pyautogui.FAILSAFE = False


class Logger:
    def __init__(self):
        self.filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        with open(self.filename,'a') as file:
            file.write('datetime,is_stationary\n')

    def write(self,dt,is_stationary):
        with open(self.filename,'a') as file:
            file.write(f'{dt.isoformat()},{is_stationary}\n')


class TimeKeeper:
    def __init__(self, TIME_IDLE_TO_WAKE) -> None:
        self.TIME_IDLE_TO_WAKE = TIME_IDLE_TO_WAKE
        self.set_both()

    def is_sleep_in(self):
        return self.now > self.awake
    
    def set_awake(self):
        self.awake = self.now + timedelta(seconds=self.TIME_IDLE_TO_WAKE)

    def set_both(self):
        self.set_now()
        self.set_awake()

    def set_now(self):
        self.now =  datetime.now()

    def set_last_idle(self):
        self.last_movement = datetime.now()


class Mouse:
    def __init__(self):
        self._last_position = self.get_snapshot()

    def is_stationary(self, last_position=None, current_position=None):
        cp = current_position or self.get_snapshot()
        lp = last_position or self._last_position
        result = (cp == lp)
        self._last_position = self.get_snapshot()
        return result

    @staticmethod
    def get_snapshot():
        return pyautogui.position()

    def move_mouse(self):
        """ Moves mouse required amount and presses shift key """
        for i in range(200):
            pyautogui.moveTo(0,i*4)
        pyautogui.moveTo(1,1)
        for i in range(3):
            pyautogui.press("shift")


def main():
    """ Keeps computer awake if at risk of sleeping (showing away status) """
    IDLE_RESOLUTION = 10 # not really seconds, but indicative of time passed
    TIME_IDLE_TO_WAKE = 18

    logger = Logger()
    times = TimeKeeper(TIME_IDLE_TO_WAKE)
    mouse = Mouse()

    print(f"{times.now.strftime('%H:%M:%S')}: App started...")

    while(True):
        times.set_now()
        mouse_is_stationary = mouse.is_stationary()
        logger.write(times.now,mouse_is_stationary)

        if mouse_is_stationary:
            if times.is_sleep_in():
                print(f"{times.now.strftime('%H:%M:%S')}: Sleeping longer than {TIME_IDLE_TO_WAKE} seconds")
                mouse.move_mouse()
                times.set_both()
        else:
            times.set_both()

        time.sleep(IDLE_RESOLUTION)


if __name__ == '__main__':
    main()
