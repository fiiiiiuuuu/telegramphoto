import os
import dotenv
import argparse
from fetch_spacex_images import fetch_spacex_launch
from nasa_apod_images import download_nasa_apod
from nasa_epic_images import download_nasa_epic

if __name__ == "__main__":
    dotenv.load_dotenv('.env')
    NASA_APIKEY = os.getenv("NASA_APIKEY")

    folder = "photos"
    if not os.path.exists(folder):
        os.mkdir(folder)

    parser = argparse.ArgumentParser() 
    parser.add_argument('--launch_id')
    parser.add_argument('--apod', action='store_true')
    parser.add_argument('--epic', action='store_true')
    args = parser.parse_args()

    if args.launch_id:
        fetch_spacex_launch(args.launch_id, folder)
    if args.apod:
        download_nasa_apod(NASA_APIKEY, folder)
    if args.epic:
        download_nasa_epic(NASA_APIKEY, folder)