from abc import ABCMeta, abstractmethod
import os
from typing import List
from cloudstoragetui.utils import pathstring

class FileType:
    FILE = "file"
    FOLDER = "folder"


class FileSystem(metaclass=ABCMeta):

    def __init__(self, path: str, parent, provider=None):
        self.path = path
        self.parent = parent
        self._provider = provider

    def __repr__(self):
        return f"""{self._type}: {self.path}"""

    @property
    def provider(self) -> str:
        return self._provider or (self.parent.provider if self.parent else None)

    @property
    @abstractmethod
    def name(self) -> str:
        return

    def is_file(self):
        return self._type == FileType.FILE

    def is_folder(self):
        return self._type == FileType.FOLDER


class File(FileSystem):
    _type = FileType.FILE

    @property
    def name(self):
        return os.path.basename(self.path)


class Folder(FileSystem):
    _type = FileType.FOLDER

    def __init__(self, path: str, parent: FileSystem, provider=None):
        super().__init__(path, parent, provider)
        self.children = []

    def get_children(self) -> List[str]:
        if self.children:
            return self.children

        from cloudstoragetui.cloud.cloudclient import CloudClient
        self.children = CloudClient.list_filenames_by_fullpath(self.path, self.provider)
        return self.children

    def generate_children_filesystem(self) -> List[FileSystem]:
        results: List[FileSystem] = []
        for child in self.get_children():
            if child.endswith("/"):
                results.append(Folder(self.path + child, self, self.provider))
            else:
                results.append(File(self.path + child, self, self.provider))
        return results


    @property
    def name(self):
        return pathstring.get_foldername_from_folderstring(self.path)

    def select_child(self, name):
        if name[-1] == "/":
            return Folder(f"{self.path}{name}", self)
        else:
            return File(f"{self.path}{name}", self)


def generate_filesystem_from_path(path: str) -> List[File]:
    path = f"/{path.split('//')}"
    path_split = path.split("/")
    results = []
    for i, path_section in enumerate(path_split):
        if i == len(path_split) - 1:
            results.append(File("/".join(path_split[:i+1])))
        else:
            results.append(Folder("/".join(path_split[:i+1]) + "/"))
    return results
