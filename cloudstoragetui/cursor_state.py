import copy
from cloudstoragetui.constants import HEIGHT_BUFFER

class CursorState:
    _MIN_ROW = 4
    _MAX_COLUMNS = 2

    def __init__(self):
        self.column = 0
        self.depth = 0
        self.row = self._MIN_ROW
    
    def move_column_right(self):
        self.column = min(self.column + 1, self._MAX_COLUMNS)
        self.depth += 1
        self.row = self._MIN_ROW

    def move_column_left(self):
        self.column = max(self.column - 1, 0)
        self.depth = max(self.depth - 1, 0)
        self.row = self._MIN_ROW

    def move_row_up(self, min_x):
        self.row = max(self.row - 1, min_x)

    def move_row_down(self, max_x):
        self.row = min(self.row + 1, max_x)

    def __str__(self):
        return f"({self.row}, {self.column})"

    def get_row_in_box(self):
        return self.row - HEIGHT_BUFFER

    def copy(self):
        return copy.deepcopy(self)
