import os
import dotenv
import argparse
from fetch_spacex_images import fetch_spacex_launch
from nasa_apod_images import download_nasa_apod
from nasa_epic_images import download_nasa_epic

dotenv.load_dotenv('.env')
NASA_API_KEY = os.environ["NASA_API_KEY"]

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--fld', help='название папки') 
    parser.add_argument('--lid', help='айди для фото запусков spacex (необязательно)')
    parser.add_argument('--spacex', action='store_true', help='загрузка фоток SpaceX (если нету своего айди запуска)')    
    parser.add_argument('--apod', action='store_true', help='загрузка картинок дня')
    parser.add_argument('--epic', action='store_true', help='загрузка фотографий земли')
    args = parser.parse_args()

    folder = args.fld
    os.makedirs(folder, exist_ok=True)

    if args.lid or args.spacex:
        fetch_spacex_launch(args.lid, folder)
    if args.apod:
        download_nasa_apod(NASA_API_KEY, folder)
    if args.epic:
        download_nasa_epic(NASA_API_KEY, folder)