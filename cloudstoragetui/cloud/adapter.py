from typing import List
from abc import ABCMeta, abstractmethod

from cloudstoragetui.filesystem import Folder, File

class CloudAdapter(metaclass=ABCMeta):

    @abstractmethod
    def initiate_buckets()-> List[List[Folder]]:
        return
