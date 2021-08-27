import logging

from get_file_data import *
from find_files import find_files_in_directory

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    for file in find_files_in_directory("../images"):
        logging.info(f"Scanning file: '{file}'")
        logging.info(get_geotagging(get_exif(file)))
        logging.info(get_file_creation_date(file))