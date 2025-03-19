import requests
import os


def fetch_spacex_launch(launch_id=None, folder=None):
    if launch_id:
        url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    else:
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