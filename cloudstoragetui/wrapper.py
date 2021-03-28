import curses

def cursor_wrapper(screen, f):
    def fn(*args, **kwargs):
        curs_y, curs_x = curses.getsyx()
        f(*args, **kwargs)
        screen.move(curs_y, curs_x)
    return fn

def screen_wrapper(screen, f):
    def fn(*args, **kwargs):
        curs_y, curs_x = curses.getsyx()
        results = f(screen, *args, **kwargs)
        screen.move(curs_y, curs_x)
        return results
    return fn

