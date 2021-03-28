import curses
from cloudstoragetui.wrapper import screen_wrapper

def log(screen, sentence):
    curs_y, curs_x = curses.getsyx()
    screen.addstr(0, 0, f"{sentence}", curses.color_pair(1))
    screen.move(curs_y, curs_x)
