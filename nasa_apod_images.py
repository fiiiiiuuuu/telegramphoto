import requests
import os
from urllib.parse import urlsplit, unquote
from os.path import splitext, split


def get_file_extension(url: str):
    path = unquote(urlsplit(url).path)
    filename = split(path)[1]
    _, ext = splitext(filename)
    return ext.lower()


def download_nasa_apod(api_key, folder=None, count=30):
    url = f'https://api.nasa.gov/planetary/apod'
    payload = {'api_key': api_key,
               'count': count}
    response = requests.get(url, params=payload)
    response.raise_for_status()

    data = response.json()
    for index, item in enumerate(data, start=1):
        if 'url' not in item:
            print('no url. skip')
            continue

        if item['media_type'] != 'image':
            print('this is video. skip')
            continue
        
        image_link = item['hdurl'] if 'hdurl' in item else item['url']
        extension = get_file_extension(image_link)
        filename = f"{index}_apod_{item['date']}{extension}"
        file_path = os.path.join(folder, filename)

        photo_response = requests.get(image_link)
        photo_response.raise_for_status()

        with open(file_path, 'wb') as file:
            file.write(photo_response.content)
        
        print(f'Фото сохранено как: {filename}')