import requests
import os

def build_spacex_url(launch_id):
    if launch_id:
        return f"https://api.spacexdata.com/v5/launches/{launch_id}"
    return "https://api.spacexdata.com/v5/launches/5eb87d47ffd86e000604b38a"

def fetch_spacex_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def extract_image_links(api_response):
    return api_response.get('links', {}).get('flickr', {}).get('original', {})

def dowload_images(links, folder):
    for index, link in enumerate(links, start=1):
        response = requests.get(link)
        response.raise_for_status()

        filename = f"spacex_{index}.jpg"
        file_path = os.path.join(folder, filename)

        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Фото {filename} сохранено.")
        

def fetch_spacex_launch(launch_id=None, folder=None):
    url = build_spacex_url(launch_id)
    data = fetch_spacex_data(url)
    links = extract_image_links(data)

    if links:
        dowload_images(links, folder)
    else:
        print('No images!')