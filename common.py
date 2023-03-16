import pathlib
import requests


def get_comics_file_name(url):
    """Determine comics file name from URL"""
    url_parts = url.split('/')
    comics_file_name = url_parts[-1]
    return comics_file_name


def download_comics_picture(url, folder=None, params={}):
    """Download comics picture via URL link to the folder"""
    response = requests.get(url, params=params)
    response.raise_for_status()

    comics_file_name = get_comics_file_name(url)
    if not folder:
        folder = '.'
    else:
        pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    full_path = f'{folder}/{comics_file_name}'
    with open(full_path, 'wb') as file:
        file.write(response.content)
    return full_path


def get_random_comics(comics_number):
    """Extract random comics parameters: URL, text description"""
    comics_url = f'https://xkcd.com/{comics_number}/info.0.json'
    response = requests.get(comics_url)
    response.raise_for_status()

    comics_json = response.json()
    img_url = comics_json['img']
    img_desc = comics_json['alt']
    return (img_url, img_desc,)


def get_upload_server(vk_access_token, comics_group_id):
    """Get VK server URL to upload comics picture file"""
    params = {
            'access_token': vk_access_token,
            'group_id': comics_group_id,
            'v': '5.131',
    }
    response = requests.get('https://api.vk.com/method/photos.getWallUploadServer/', params=params)
    response.raise_for_status()

    json = response.json()['response']
    return json['upload_url']


def upload_comics(server_url, vk_access_token, comics_group_id, comics_picture_pathname, comics_descr):
    """Upload comics picture to vk.com server"""
    with open(comics_picture_pathname, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(server_url, files=files)
        response.raise_for_status()

        json = response.json()
        server = json['server']
        photo = json['photo']
        hash = json['hash']

        params = {
            'server': server,
            'photo': photo,
            'hash': hash,
            'access_token': vk_access_token,
            'group_id': comics_group_id,
            'v': '5.131',
        }
        response = requests.post('https://api.vk.com/method/photos.saveWallPhoto/', data=params)
        response.raise_for_status()
        resp = response.json()

        owner_id = resp['response'][0]['owner_id']
        media_id = resp['response'][0]['id']
        attachments = f'photo{owner_id}_{media_id}'

        params = {
            'message': comics_descr,
            'owner_id': f'-{comics_group_id}',
            'attachments': attachments,
            'from_group': 1,
            'access_token': vk_access_token,
            'v': '5.131',
        }
        response = requests.post('https://api.vk.com/method/wall.post/', data=params)
        response.raise_for_status()
        print('\n********')
