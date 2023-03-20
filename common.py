import os
import random
import requests
from urllib.parse import unquote
from urllib.parse import urlsplit


def get_file_name(url):
    """Extract file name from URL"""
    file_path = urlsplit(url).path
    file_path = unquote(file_path)
    _, file_name = os.path.split(file_path)
    return file_name


def download_comic_file(url, folder, params={}):
    """Download comic file via URL link to the folder"""
    response = requests.get(url, params=params)
    response.raise_for_status()

    comic_file_name = get_file_name(url)
    comic_file_path = os.path.join(folder, comic_file_name)
    with open(comic_file_path, 'wb') as file:
        file.write(response.content)
    return comic_file_path


def get_total_comic_number():
    """Determine total comic number on the xkcd.com"""
    api_url = 'https://xkcd.com/info.0.json'
    response = requests.get(api_url)
    response.raise_for_status()
    resp_object = response.json()
    return resp_object['num']


def get_random_comic():
    """Get random comic as extracted parameters: image URL, description"""
    total_comic_number = get_total_comic_number()
    random_comic = random.randrange(1, total_comic_number)
    api_url = f'https://xkcd.com/{random_comic}/info.0.json'
    response = requests.get(api_url)
    response.raise_for_status()

    resp_object = response.json()
    comic_img_url = resp_object['img']
    comic_text_desc = resp_object['alt']
    return comic_img_url, comic_text_desc


def get_upload_server(access_token, group_id):
    """Get VK server URL to upload comic file"""
    params = {
            'access_token': access_token,
            'group_id': group_id,
            'v': '5.131',
    }
    api_url = 'https://api.vk.com/method/photos.getWallUploadServer/'
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    resp_object = response.json()['response']
    return resp_object['upload_url']


def upload_to_server(server_url, comic_photo):
    """Upload comic photo to server"""
    with open(comic_photo, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(server_url, files=files)
    response.raise_for_status()
    resp_object = response.json()
    server_id = resp_object['server']
    photo = resp_object['photo']
    photo_hash = resp_object['hash']
    return server_id, photo, photo_hash


def save_photo_to_album(access_token, group_id, server_id,
                        photo, photo_hash):
    """Save photo to a group album"""
    params = {
            'server': server_id,
            'photo': photo,
            'hash': photo_hash,
            'access_token': access_token,
            'group_id': group_id,
            'v': '5.131',
    }
    api_url = 'https://api.vk.com/method/photos.saveWallPhoto/'
    response = requests.post(api_url, data=params)
    response.raise_for_status()

    resp_object = response.json()
    owner_id = resp_object['response'][0]['owner_id']
    photo_id = resp_object['response'][0]['id']
    return owner_id, photo_id


def publish_to_wall(access_token, group_id, owner_id, photo_id, comic_desc):
    """Publish comic picture + funny text to the user's wall"""
    params = {
        'message': comic_desc,
        'owner_id': f'-{group_id}',
        'attachments': f'photo{owner_id}_{photo_id}',
        'from_group': 1,
        'access_token': access_token,
        'v': '5.131',
    }
    api_url = 'https://api.vk.com/method/wall.post/'
    response = requests.post(api_url, data=params)
    response.raise_for_status()
    resp_object = response.json()['response']
    return resp_object['post_id']
