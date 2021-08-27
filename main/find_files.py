import os

from typing import List


def find_files_in_directory(path: str) -> List[str]:
    """
    Returned rekursiv alle in dem Direktory gefundenen Bilder
    :param path: Directory das rekursiv nach bildern durchsucht werden soll
    :return: alle Bilder die in dem Directory geunden wurden
    """
    all_image_paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            all_image_paths.append(f"{root}/{file}")
    return all_image_paths

