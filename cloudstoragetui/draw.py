from typing import List
import curses

from cloudstoragetui.cursor_state import CursorState
from cloudstoragetui.filesystem import FileSystem, Folder

class DrawnBox:

    def __init__(self, index, length_y, length_x, top_left_y, top_left_x):
        self.index = index
        self.length_y = length_y
        self.length_x = length_x
        self.top_left_y = top_left_y
        self.top_left_x = top_left_x
        self.box = None

    def draw_column_with_text(self, screen, col_data: List[FileSystem], cursor_state: CursorState):
        if self.box is None:
            self.box = self.create_box(
                length_y=self.length_y,
                length_x=self.length_x,
                top_left_y=self.top_left_y,
                top_left_x=self.top_left_x)

        return self._draw_column(
            screen=screen,
            box=self.box,
            length_y=self.length_y,
            length_x=self.length_x,
            top_left_y=self.top_left_y,
            top_left_x=self.top_left_x,
            data=col_data,
            column=self.index,
            cursor_state=cursor_state)

    def create_box(self, length_y: int, length_x: int, top_left_y: int, top_left_x: int):
        box = curses.newwin(length_y, length_x, top_left_y, top_left_x)
        box.box()
        return box

    def _draw_column(self, screen, box, length_y: int, length_x: int, top_left_y: int, top_left_x: int, data: List[FileSystem], column: int, cursor_state: CursorState):
        self.write_texts(box, length_y, length_x, top_left_y - 1, top_left_x - 1, data, column, cursor_state)
        box.refresh()
        screen.refresh()

    @classmethod
    def _set_background_colour(cls, i, is_folder, column, cursor_state):
        if is_folder:
            if i + CursorState._MIN_ROW == cursor_state.row and column == cursor_state.column:
                return curses.color_pair(3)
            else:
                return curses.color_pair(2)
        if i + CursorState._MIN_ROW == cursor_state.row and column == cursor_state.column:
            return curses.color_pair(1)
        return 0

    def write_texts(self, screen, length_y, length_x, top_left_y, top_left_x, data: List[FileSystem], column, cursor_state):
        curs_y, curs_x = curses.getsyx()
        for i, filesystem in enumerate(data):
            screen.addstr(i+1, 1, filesystem.name, self._set_background_colour(i, isinstance(filesystem, Folder), column, cursor_state))

