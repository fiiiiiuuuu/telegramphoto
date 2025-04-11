import requests
import os
import datetime


def download_nasa_epic(api_key, folder=None):
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

        filename = f"{image_name}_{index}.png"
        file_path = os.path.join(folder, filename)

        image_response = requests.get(image_url, params={'api_key': api_key})
        image_response.raise_for_status()

        with open(file_path, 'wb') as file:
            file.write(image_response.content)
        print(f"Изображение {filename} сохранено")