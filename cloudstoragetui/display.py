from typing import List
import curses
from cloudstoragetui.constants import ESC, NO_OF_COLUMNS
from cloudstoragetui.draw import DrawnBox
from cloudstoragetui.wrapper import screen_wrapper
from cloudstoragetui.cursor_state import CursorState
from cloudstoragetui.keypress import eval_keypress
from cloudstoragetui.debug import log
from cloudstoragetui.filesystem import FileSystem 
from cloudstoragetui.cloud.adapter import CloudAdapter
from cloudstoragetui.actions import evaluate_action

def _get_screen_max(screen):
    height, width = screen.getmaxyx()
    return height - 1, width - 1

def create_column_boxes(screen, data: List[List[FileSystem]]) -> List[DrawnBox]:
    height, width = _get_screen_max(screen)
    column_width = int(width/NO_OF_COLUMNS)
    results: List[DrawnBox] = []
    for i, _ in enumerate(data):
        box = DrawnBox(
                index=i,
                length_y=height - CursorState._MIN_ROW + 1,
                length_x=column_width,
                top_left_y=CursorState._MIN_ROW - 1,
                top_left_x=(i*column_width) + 1
            )
        results.append(box)
    return results

def draw_columns(screen, data: List[List[FileSystem]], cursor_state: CursorState, boxes: List[DrawnBox]=[]) -> List[DrawnBox]:
    height, width = _get_screen_max(screen)
    column_width = int(width/NO_OF_COLUMNS)
    boxes: List[DrawnBox] = boxes or create_column_boxes(screen, data)
    for col_data, box in zip(data, boxes):
        box.draw_column_with_text(screen, col_data, cursor_state)
    return boxes

def _loading(screen, x=None, y=None):
    curs_y, curs_x = curses.getsyx()
    screen.addstr(y or curs_y, x or curs_x, "Loading")
    screen.refresh()
    screen.move(curs_y, curs_x)

def screen_init(screen, cloud_adapter: CloudAdapter):
    screen.addstr(0, 0, "⌛")
    screen.refresh()
    column_data = cloud_adapter.initiate_buckets()
    screen.clear()
    screen.refresh()
    screen.scrollok(1)

    height, width = screen.getmaxyx()

    SCREEN_MAX_Y = height - 1
    SCREEN_MAX_X = width - 1

    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) # selected file
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK) # unselected folder
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN) # selected folder

    cursor_state = CursorState()
    boxes = screen_wrapper(screen, draw_columns)(data=column_data, cursor_state=cursor_state)
    screen.move(CursorState._MIN_ROW, 2)

    while True:
        key = screen.getch()
        screen.clear()
        previous_state = cursor_state.copy()
        action = eval_keypress(screen, key, boxes, cursor_state)
        if action == ESC:
            break
        column_data = evaluate_action(screen, action, cloud_adapter, previous_state, cursor_state, column_data)
        boxes = screen_wrapper(screen, draw_columns)(data=column_data[-3:], cursor_state=cursor_state, boxes=boxes)
    

def main():
    column_data = [["hi/", "there/"], ["how/", "are"], ["you"]]
    curses.wrapper(screen_init, column_data=column_data)

if __name__ == "__main__":
    main()
