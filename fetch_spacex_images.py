import requests
import os
from download_image import download_image

def fetch_spacex_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def extract_image_links(api_response):
    return api_response.get('links', {}).get('flickr', {}).get('original', {})
        

def fetch_spacex_launch(launch_id=None, folder=None):
    url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    data = fetch_spacex_data(url)
    links = extract_image_links(data)
    if links:
        for index, link in enumerate(links, start=1):
            filename = f"spacex_{index}.jpg"
            file_path = os.path.join(folder, filename)

            download_image(link, file_path)
            print(f"Фото {filename} сохранено.")
    else:
        print('No images!')