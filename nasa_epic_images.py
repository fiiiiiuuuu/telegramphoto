import requests
import os
import datetime


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
    return f"https://api.nasa.gov/EPIC/archive/natural/{formatted_date}/png/{image_name}.png?api_key={api_key}"


def download_image(image_url, file_path):
    image_response = requests.get(image_url)
    image_response.raise_for_status()

    with open(file_path, 'wb') as file:
        file.write(image_response.content)


def download_nasa_epic(api_key, folder=None):
    data = fetch_nasa_epic(api_key)

    for index, image_data in enumerate(data, start=1):
        image_url = build_epic_image_url(image_data, api_key)
        filename = f"{image_data['image']}_{index}.png"
        file_path = os.path.join(folder, filename)

        download_image(image_url, file_path)
        print(f"Изображение {filename} сохранено")