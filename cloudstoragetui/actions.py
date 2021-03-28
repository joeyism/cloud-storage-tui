from typing import List
import curses

from cloudstoragetui.constants import UP, DOWN, LEFT, RIGHT, KEY_ENTER, NO_OF_COLUMNS
from cloudstoragetui.cloud.adapter import CloudAdapter
from cloudstoragetui.cursor_state import CursorState
from cloudstoragetui.filesystem import FileSystem, File, Folder, generate_filesystem_from_path


def evaluate_action(screen, action: int, cloud_adapter: CloudAdapter, previous_state: CursorState, cursor_state: CursorState, column_data: List[List[FileSystem]]):
    if action == RIGHT:
        row = previous_state.get_row_in_box()
        column = previous_state.column
        filesystem = column_data[column][row]
        if filesystem.is_folder():
            children = filesystem.generate_children_filesystem()
            if column + 1 >= NO_OF_COLUMNS:
                column_data.append(children)
            else:
                column_data[column + 1] = children
        else:
            "TODO: download file"
    return column_data
