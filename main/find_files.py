import os

from typing import List


def find_files_in_directory(path: str) -> List[str]:
    """
    Returns recursively all images found in the directory
    :param path: path to directory
    :return: list of all paths to the images found in the directory
    """
    all_image_paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            all_image_paths.append(f"{root}/{file}")
    return all_image_paths

