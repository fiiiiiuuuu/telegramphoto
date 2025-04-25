import requests
import os
from urllib.parse import urlsplit, unquote
from os.path import splitext, split


def get_file_extension(url: str):
    path = unquote(urlsplit(url).path)
    filename = split(path)[1]
    _, ext = splitext(filename)
    return ext.lower()


def fetch_apod_data(api_key, count=30):
    url = f'https://api.nasa.gov/planetary/apod'
    payload = {'api_key': api_key,
               'count': count}
    response = requests.get(url, params=payload)
    response.raise_for_status()

    return response.json()


def should_skip_item(item):
    if 'url' not in item:
            print('no url. skip')
            return False

    if item['media_type'] != 'image':
        print('this is video. skip')
        return False
    return True
    

def get_image_url(item):
    return item['hdurl'] if 'hdurl' in item else item['url']


def generate_filename(item, index):
    extension = get_file_extension(get_image_url(item))
    return f"{index}_apod_{item['date']}{extension}"


def download_image(url, path):
    photo_response = requests.get(url)
    photo_response.raise_for_status()

    with open(path, 'wb') as file:
        file.write(photo_response.content)

def download_nasa_apod(api_key, folder=None, count=30):
    data = fetch_apod_data(api_key)
    for index, item in enumerate(data, start=1):
        if not should_skip_item(item):
            continue

        image_url = get_image_url(item)
        filename = generate_filename(item, index)
        file_path = os.path.join(folder, filename)

        
        download_image(image_url, file_path)
        print(f'Фото сохранено как: {filename}')