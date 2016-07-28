from os import path
import time
from threading import Thread

import curses
from curses import ERR
from requests.exceptions import HTTPError

from pythonwars.pythonwars import CodeWars


class Tui:
    def __init__(self):
        self.code_wars = None

    def main(self, curse_main):

        curses.cbreak()
        self.login_screen(curse_main)
        curse_main.clear()
        self.auth_api(curse_main)

    def login_screen(self, login_scr):
        
        login_scr.addstr('-'*47 + 'Welcome to Codewars!' + '-'*47)
        login_scr.refresh()
        time.sleep(1)

        login_scr.addstr(54, 43, 'Please enter your API token:')
        login_scr.refresh()
        curses.echo()
        time.sleep(1)

        logo_thrd = Thread(self.logo_print(login_scr))
        logo_thrd.start()
        
        user_api = ''
        
        getch_position = [0, 0]
        input_scr = curses.newwin(1,20, 55,47)
        input_scr.keypad(True)
        input_scr.nodelay(True)

        while True:
            in_char = input_scr.getch(*getch_position)
            try:
                if int(in_char) == -1:
                    continue
            except TypeError:
                pass
            else:
                if in_char == curses.KEY_BACKSPACE:
                    user_api = user_api[:-1]
                    getch_position[1] -= 1
                    input_scr.delch(*getch_position)
                else:
                    user_api += chr(in_char)
                    getch_position[1] += 1
            if len(user_api) == 20:
                   break

        input_scr.nodelay(False)
        self.code_wars = CodeWars(user_api)

        login_scr.addstr(56, 45, 'Press enter to confirm.')
        login_scr.getch()

        login_scr.keypad(False)
        login_scr.clear()

    def logo_print(self, scr):
        with open(path.join('ascii_art', 'logo.txt')) as logo_file:
            logo_count = 7
            for line in logo_file:
                scr.addstr(logo_count, 12, line)
                logo_count += 1
                scr.refresh()
                time.sleep(0.05)

    def auth_api(self, auth_scr):
        auth_scr.addstr(10, 40, 'Authenticating your API token.')
        try:
            a = self.code_wars.train_next_code_challenge('python', peek=True)
        except HTTPError:
            auth_scr.addstr(11,41, 'Authentication failed. Gtfo.')
            auth_scr.addstr(18,42, 'Press the Any key to exit.')
            auth_scr.refresh()
            auth_scr.getkey()
        else:
            auth_scr.addstr(11,47, 'Authenticated.')
            auth_scr.refresh()
            time.sleep(3)


tui = Tui()
curses.wrapper(tui.main)
