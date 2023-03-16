import os
import requests
from environs import Env
from common import get_random_comics
from common import download_comics_picture
from common import get_upload_server
from common import upload_comics_photo
from common import save_photo_group_album
from common import publish_comics


def main():
    """Program entry point"""
    env = Env()
    env.read_env()
    group_id = env('VK_COMICS_GROUP_ID')
    access_token = env('VK_ACCESS_TOKEN')

    try:
        comics_url, comics_desc = get_random_comics()
        comics_photo_path = download_comics_picture(comics_url)
        server_url = get_upload_server(access_token, group_id)
        photo_json = upload_comics_photo(server_url, comics_photo_path)
        album_json = save_photo_group_album(access_token, group_id, photo_json)
        publish_comics(access_token, group_id, album_json, comics_desc)
    except requests.exceptions.HTTPError:
        print('HTTP requests error occurred. Exit from runtime...')
        raise SystemExit(1)

    os.remove(comics_photo_path)
    print(f'\nComics was published successfully!\n')


if __name__ == '__main__':
    main()
