import os

def get_foldername_from_folderstring(path):
    return os.path.basename(os.path.dirname(path))
