import random
import pathlib
import requests


def get_file_name(url):
    """Determine file name from URL"""
    url_parts = url.split('/')
    file_name = url_parts[-1]
    return file_name


def download_comics_picture(url, folder=None, params={}):
    """Download comics picture via URL link to the folder"""
    response = requests.get(url, params=params)
    response.raise_for_status()

    comics_file_name = get_file_name(url)
    if not folder:
        folder = '.'
    else:
        pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    comics_full_path = f'{folder}/{comics_file_name}'
    with open(comics_full_path, 'wb') as file:
        file.write(response.content)
    return comics_full_path


def get_total_comics_number():
    """Determine total comics number on the xkcd.com"""
    api_url = 'https://xkcd.com/info.0.json'
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()['num']


def get_random_comics():
    """Get random comics as extracted parameters: image URL, description"""
    total_comics_num = get_total_comics_number()
    random_comics = random.randrange(1, total_comics_num)
    api_url = f'https://xkcd.com/{random_comics}/info.0.json'
    response = requests.get(api_url)
    response.raise_for_status()

    comics_json = response.json()
    img_url = comics_json['img']
    text_desc = comics_json['alt']
    return (img_url, text_desc,)


def get_upload_server(access_token, group_id):
    """Get VK server URL to upload comics picture"""
    params = {
            'access_token': access_token,
            'group_id': group_id,
            'v': '5.131',
    }
    api_url = 'https://api.vk.com/method/photos.getWallUploadServer/'
    response = requests.get(api_url, params=params)
    response.raise_for_status()

    json = response.json()['response']
    return json['upload_url']


def upload_comics_photo(server_url, comics_photo):
    """Upload comics photo to server"""
    with open(comics_photo, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(server_url, files=files)
        response.raise_for_status()
    return response.json()


def save_photo_group_album(access_token, group_id, photo_json):
    """Save photo to a group album"""
    server = photo_json['server']
    photo = photo_json['photo']
    hash = photo_json['hash']

    params = {
            'server': server,
            'photo': photo,
            'hash': hash,
            'access_token': access_token,
            'group_id': group_id,
            'v': '5.131',
        }
    api_url = 'https://api.vk.com/method/photos.saveWallPhoto/'
    response = requests.post(api_url, data=params)
    response.raise_for_status()
    return response.json()


def publish_comics(access_token, group_id, album_json, comics_desc):
    """Publish comics picture to group page on vk.com"""
    owner_id = album_json['response'][0]['owner_id']
    photo_id = album_json['response'][0]['id']
    attachments = f'photo{owner_id}_{photo_id}'

    params = {
        'message': comics_desc,
        'owner_id': f'-{group_id}',
        'attachments': attachments,
        'from_group': 1,
        'access_token': access_token,
        'v': '5.131',
    }
    api_url = 'https://api.vk.com/method/wall.post/'
    response = requests.post(api_url, data=params)
    response.raise_for_status()
    json = response.json()
    return json['response']['post_id']
