import os
import random
from environs import Env
from common import upload_comics
from common import get_upload_server
from common import get_random_comics
from common import download_comics_picture


def main():
    """Program entry point"""
    env = Env()
    env.read_env()

    last_published_comics_number = env.int('LAST_PUBLISHED_COMICS_NUMBER')
    comics_group_id = env('COMICS_GROUP_ID')
    vk_access_token = env('VK_ACCESS_TOKEN')

    random_comics_num = random.randrange(1, last_published_comics_number)
    comics_url, comics_description = get_random_comics(random_comics_num)
    comics_picture_pathname = download_comics_picture(comics_url)

    server_url = get_upload_server(vk_access_token, comics_group_id)
    upload_comics(server_url, vk_access_token, comics_group_id,
                  comics_picture_pathname, comics_description)
    os.remove(comics_picture_pathname)


if __name__ == '__main__':
    main()
