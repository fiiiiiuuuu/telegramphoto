import requests
import os
import dotenv
import argparse
from fetch_spacex_images import fetch_spacex_launch
from nasa_apod_images import nasa_apod
from nasa_epic_images import nasa_epic

def download_photo():
    url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"
    filename = "hubble.jpeg"
    filepath = os.path.join(folder, filename)

    response = requests.get(url)
    response.raise_for_status()

    with open(filepath, 'wb') as file:
        file.write(response.content)
    print(f"Фото {filename} сохранено.")

if __name__ == "__main__":
    dotenv.load_dotenv('.env')
    NASA_API = os.getenv("NASA_API")

    folder = "photos"
    if not os.path.exists(folder):
        os.mkdir(folder)

    parser = argparse.ArgumentParser() 
    parser.add_argument('--launch_id')
    args = parser.parse_args()

    download_photo()
    fetch_spacex_launch(args.launch_id, folder)
    nasa_apod(NASA_API, folder)
    nasa_epic(NASA_API, folder)