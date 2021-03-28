import curses
from typing import List

from cloudstoragetui.constants import KEY_QUIT, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_ENTER, ESC, UP, DOWN, LEFT, RIGHT
from cloudstoragetui.draw import DrawnBox
from cloudstoragetui.cursor_state import CursorState
from cloudstoragetui.debug import log

def _extract_min_max(box):
    min_y = box.top_left_y + 1
    min_x = box.top_left_x + 1
    max_y = box.length_y + box.top_left_y - 2
    max_x = (box.index + 1) * box.length_x - 1
    return (min_y, min_x, max_y, max_x)

def _eval_keypress(screen, key, boxes, cursor_state):
    curs_y, curs_x = curses.getsyx()
    box = boxes[cursor_state.column]
    min_y, min_x, max_y, max_x = _extract_min_max(box)
    action = None

    if key in KEY_QUIT:
        action = ESC
    elif key in KEY_UP:
        cursor_state.move_row_up(min_y)
        screen.move(max(curs_y - 1, min_y), curs_x)
        action = UP
    elif key in KEY_DOWN:
        cursor_state.move_row_down(max_y)
        screen.move(min(curs_y + 1, max_y), curs_x)
        action = DOWN
    elif key in KEY_LEFT:
        if curs_x == min_x:
            cursor_state.move_column_left()
            box = boxes[cursor_state.column]
            min_y, min_x, max_y, max_x = _extract_min_max(box)
            screen.move(min_y, min_x)
        else:
            screen.move(curs_y, max(curs_x - 1, min_x))
        action = LEFT
    elif key in KEY_RIGHT + KEY_ENTER:
        cursor_state.move_column_right()
        box = boxes[cursor_state.column]
        screen.move(box.top_left_y + 1, box.top_left_x + 1)
        action = RIGHT
    screen.refresh()
    return action

def eval_keypress(screen, key: int, boxes: List[DrawnBox], cursor_state: CursorState):
    return _eval_keypress(screen, key, boxes, cursor_state)
