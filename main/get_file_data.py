import logging
import os
import requests
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS


def get_labeled_exif(exif):
    """
    labels the exif dictionary with human readable tags
    :param exif:
    :return: labeled dictionary
    """
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val
    return labeled


def get_exif(filename):
    """
    returns meta data from an image file via path variable
    :param filename: path and filename
    :return: exif dictionary
    """
    image = Image.open(filename)
    image.verify()
    return image._getexif()


def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging


def get_geo_data(filename):
    exif = get_exif(filename)
    geotagging = get_geotagging(exif)
    return geotagging


def get_decimal_from_dms(dms, ref):

    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon)

def get_location(geotags):
    coords = get_coordinates(geotags)

    uri = 'https://revgeocode.search.hereapi.com/v1/revgeocode'
    headers = {}
    params = {
        'apiKey': os.environ['API_KEY'],
        'at': "%s,%s" % coords,
        'lang': 'en-US',
        'limit': 1,
    }

    response = requests.get(uri, headers=headers, params=params)
    try:
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        print(str(e))
        return {}

#exif = get_exif('image.jpg')
#geotags = get_geotagging(exif)
#location = get_location(geotags)

#print(location['items'][0]['address']['label'])


def get_file_creation_date(filename: str):
    labeled_exif = get_labeled_exif(get_exif(filename))
    test = labeled_exif["DateTime"]
    logging.info(f"File datetime: '{test}'")
    datetime.strptime