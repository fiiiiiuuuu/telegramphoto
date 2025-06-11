import os
import dotenv
import argparse
from fetch_spacex_images import fetch_spacex_launch
from nasa_apod_images import download_nasa_apod
from nasa_epic_images import download_nasa_epic


def main():
    dotenv.load_dotenv('.env')
    nasa_api_key = os.environ["NASA_API_KEY"]
    parser = argparse.ArgumentParser()
    parser.add_argument('--fld', default='photos', help='название папки (необязательно)') 
    parser.add_argument('--lid', nargs='?', const='5eb87d47ffd86e000604b38a', default=None, help='айди для фото запусков spacex (необязательно)')    
    parser.add_argument('--apod', action='store_true', help='загрузка картинок дня')
    parser.add_argument('--epic', action='store_true', help='загрузка фотографий земли')
    args = parser.parse_args()

    folder = args.fld
    os.makedirs(folder, exist_ok=True)

    if args.lid:
        fetch_spacex_launch(args.lid, folder)
    if args.apod:
        download_nasa_apod(nasa_api_key, folder)
    if args.epic:
        download_nasa_epic(nasa_api_key, folder)

if __name__ == "__main__":
    main() 