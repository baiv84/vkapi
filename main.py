import requests
import tempfile
from environs import Env
from common import publish_to_wall
from common import get_random_comic
from common import upload_to_server
from common import get_upload_server
from common import download_comic_file
from common import save_photo_to_album


def main():
    """Program entry point"""
    env = Env()
    env.read_env()
    group_id = env('VK_COMIC_GROUP_ID')
    access_token = env('VK_ACCESS_TOKEN')
    folder = tempfile.TemporaryDirectory()
    folder_name = folder.name

    try:
        comic_url, comic_desc = get_random_comic()
        comic_file_path = download_comic_file(comic_url, folder_name)
        server_url = get_upload_server(access_token, group_id)
        server_id, photo, photo_hash = upload_to_server(server_url, comic_file_path)
        owner_id, photo_id = save_photo_to_album(access_token, group_id, server_id, photo, photo_hash)
        publish_to_wall(access_token, group_id, owner_id, photo_id, comic_desc)
        print(f'\nNew comic story was published successfully!')
    except requests.exceptions.HTTPError:
        print('\nHTTP requests error occurred!')
        raise SystemExit(1)
    except KeyError:
        print('\nOoops, check your API token value in .env file!')
        raise SystemExit(1)
    finally:
        folder.cleanup()


if __name__ == '__main__':
    main()
