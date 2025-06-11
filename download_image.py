import requests


def download_image(url, path):
    photo_response = requests.get(url)
    photo_response.raise_for_status()

    with open(path, 'wb') as file:
        file.write(photo_response.content)
