import requests
import os
import dotenv
import datetime
from urllib.parse import urlsplit, unquote
from os.path import splitext, split

dotenv.load_dotenv('.env')
NASA_API = os.getenv("NASA_API")

folder = "photos"
if not os.path.exists(folder):
    os.mkdir(folder)


def download_photo():
    url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"
    filename = "hubble.jpeg"
    filepath = os.path.join(folder, filename)

    response = requests.get(url)
    response.raise_for_status()

    with open(filepath, 'wb') as file:
        file.write(response.content)
    print(f"Фото {filename} сохранено.")


def fetch_spacex_last_launch():
    url = "https://api.spacexdata.com/v5/launches/5eb87d47ffd86e000604b38a"
    response = requests.get(url)
    response.raise_for_status()

    api_response = response.json()

    launch_links = api_response.get('links', {}).get('flickr', {}).get('original', {})

    for index, link in enumerate(launch_links, start=1):
        response = requests.get(link)
        response.raise_for_status()

        filename = f"spacex_{index}.jpg"
        file_path = os.path.join(folder, filename)

        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Фото {filename} сохранено.")


def get_file_extension(url: str):
    path = unquote(urlsplit(url).path)
    filename = split(path)[1]
    _, ext = splitext(filename)
    return ext.lower()


def nasa_apod(api_key, count=30):
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


def nasa_epic(api_key):
    url = "https://api.nasa.gov/EPIC/api/natural/images"
    payload = {"api_key": api_key}
    response = requests.get(url, params=payload)
    response.raise_for_status()

    data = response.json()

    for index, image in enumerate(data, start=1):
        date = image['date']
        image_name = image['image']

        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        formatted_date = date_obj.strftime('%Y/%m/%d')

        image_url = f"https://api.nasa.gov/EPIC/archive/natural/{formatted_date}/png/{image_name}.png"

        filename = f"{index}_{image_name}.png"
        file_path = os.path.join(folder, filename)

        image_response = requests.get(image_url, params={'api_key': api_key})

        with open(file_path, 'wb') as file:
            file.write(image_response.content)
        print(f"Изображение {filename} сохранено")


download_photo()
fetch_spacex_last_launch()
nasa_apod(NASA_API)
nasa_epic(NASA_API)