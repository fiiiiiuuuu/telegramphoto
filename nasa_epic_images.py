import requests
import os
import datetime
from download_image import download_image
from urllib.parse import urlencode


def fetch_nasa_epic(api_key):
    url = "https://api.nasa.gov/EPIC/api/natural/images"
    payload = {"api_key": api_key}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def format_epic_date(date):
    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return date_obj.strftime('%Y/%m/%d')


def build_epic_image_url(image_data, api_key):
    formatted_date = format_epic_date(image_data['date'])
    image_name = image_data['image']

    epic_url = f"https://api.nasa.gov/EPIC/archive/natural/"
    params = {"api_key": api_key}

    encoded_params = urlencode(params)
    return f"{epic_url}{formatted_date}/png/{image_name}.png?{encoded_params}"


def download_nasa_epic(api_key, folder=None):
    data = fetch_nasa_epic(api_key)

    for index, image_data in enumerate(data, start=1):
        image_url = build_epic_image_url(image_data, api_key)
        filename = f"{image_data['image']}_{index}.png"
        file_path = os.path.join(folder, filename)

        download_image(image_url, file_path)
        print(f"Изображение {filename} сохранено")