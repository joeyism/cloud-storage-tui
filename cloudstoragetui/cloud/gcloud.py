from typing import List
import os
import subprocess

from cloudstoragetui.utils import pathstring

def list_files(remote_path) -> subprocess.CompletedProcess:
    results = subprocess.run(
        ("gsutil", "ls", remote_path), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if results.returncode:
        raise Exception("Downloading model failed")
    return results

def list_files_by_fullpath(path):
    completed_process = list_files(path)
    paths = [path for path in completed_process.stdout.decode("utf8").split("\n") if path]
    return paths

def list_filenames_by_fullpath(path) -> List[str]:
    paths = list_files_by_fullpath(path)
    paths = [f"{pathstring.get_foldername_from_folderstring(this_path)}/" if this_path[-1] == "/" else os.path.basename(this_path) for this_path in paths if this_path != path]
    return paths

def list_buckets():
    return list_files_by_fullpath("gs://")
