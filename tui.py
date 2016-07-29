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
<<<<<<< HEAD
        self.scr_size = None

    def main(self, curse_main):
        self.scr_size = ((curse_main.getmaxyx()[0] // 2), 
                        (curse_main.getmaxyx()[1] // 2))
=======

    def main(self, curse_main):

>>>>>>> b17d1d5112ff06df84b7256e4d7352c523637ede
        curses.cbreak()
        self.login_screen(curse_main)
        curse_main.clear()
        self.auth_api(curse_main)

    def login_screen(self, login_scr):
        
<<<<<<< HEAD
        login_scr.addstr('-'*int(self.scr_size[1] - 11) + 
                        'Welcome to CodeWars!' + 
                        '-'*int(self.scr_size[1] - 10))
        login_scr.refresh()
        time.sleep(1)

        login_scr.addstr(int(self.scr_size[0] + 5), 
                        int(self.scr_size[1] - 14), 
                        'Please enter your API token:')
        login_scr.refresh()
        curses.echo()
        time.sleep(1)
        if self.scr_size[0] > 28:
            logo_thrd = Thread(self.logo_print(login_scr))
            logo_thrd.start()
        user_api = ''
        getch_position = [0, 0]
        input_scr = curses.newwin(1,21, int(self.scr_size[0] + 6), 
                                        int(self.scr_size[1] - 10))
=======
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
>>>>>>> b17d1d5112ff06df84b7256e4d7352c523637ede
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

<<<<<<< HEAD
        login_scr.addstr(int(self.scr_size[0] + 8), 
                        int(self.scr_size[1] -12), 
                        'Press enter to confirm.')
=======
        login_scr.addstr(56, 45, 'Press enter to confirm.')
>>>>>>> b17d1d5112ff06df84b7256e4d7352c523637ede
        login_scr.getch()

        login_scr.keypad(False)
        login_scr.clear()

    def logo_print(self, scr):
        with open(path.join('ascii_art', 'logo.txt')) as logo_file:
<<<<<<< HEAD
            logo_count = int(self.scr_size[0] - 27)
            for line in logo_file:
                scr.addstr(logo_count, int(self.scr_size[1] - 30), line)
=======
            logo_count = 7
            for line in logo_file:
                scr.addstr(logo_count, 12, line)
>>>>>>> b17d1d5112ff06df84b7256e4d7352c523637ede
                logo_count += 1
                scr.refresh()
                time.sleep(0.05)

    def auth_api(self, auth_scr):
<<<<<<< HEAD
        auth_scr.addstr(int(self.scr_size[0] - 8), 
                        int(self.scr_size[1] -15),
                        'Authenticating your API token.')
        try:
            a = self.code_wars.train_next_code_challenge('python', peek=True)
        except HTTPError:
            auth_scr.addstr(int(self.scr_size[0] - 7), 
                            int(self.scr_size[1] -14),
                            'Authentication failed. Gtfo.')
            auth_scr.addstr(int(self.scr_size[0] - 4), 
                            int(self.scr_size[1] -13),
                            'Press the Any key to exit.')
            auth_scr.refresh()
            auth_scr.getkey()
        else:
            auth_scr.addstr(int(self.scr_size[0] - 7), 
                            int(self.scr_size[1] -7),
                            'Authenticated.')
=======
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
>>>>>>> b17d1d5112ff06df84b7256e4d7352c523637ede
            auth_scr.refresh()
            time.sleep(3)


tui = Tui()
curses.wrapper(tui.main)
