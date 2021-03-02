import os
import random

import dotenv
import requests


def get_random_comic_number(last_comic_url):
    response = requests.get(last_comic_url)
    response.raise_for_status()
    last_comic_number = response.json()['num']
    random_comic_number = random.randint(1, last_comic_number)
    return random_comic_number


def get_comic_parameters(url):
    response = requests.get(url)
    response.raise_for_status()
    comic_response = response.json()
    comic_image_url = comic_response['img']
    comic_title = comic_response['title']
    return comic_image_url, comic_title


def download_image(image_url, filename):
    response = requests.get(image_url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def check_vk_response(response):
    if response.json().get("error"):
        raise requests.HTTPError(f"error_code - {response.json()['error']['error_code']} {response.json()['error']['error_msg']}")


def get_vk_upload_url(vk_url, method_name, vk_access_token, vk_api_version):
    payload = {
        'access_token': vk_access_token,
        'v': vk_api_version
    }
    response = requests.get(f'{vk_url}/{method_name}', payload)
    check_vk_response(response)
    vk_upload_url = response.json()['response']['upload_url']
    return vk_upload_url


def get_vk_uploading_photo_parameters(upload_url, filename):
    headers = {
        'cache-control': 'no-cache',
    }
    with open(filename, 'rb') as file:
        files = {
            'photo': file
        }
        response = requests.post(upload_url, headers=headers, files=files)
    check_vk_response(response)
    photo_parameters = response.json()
    server, photo, photo_hash = photo_parameters['server'], photo_parameters['photo'], photo_parameters['hash']
    return server, photo, photo_hash


def get_vk_saving_uploading_photo_parameters(
        vk_url, method_name, server, photo, photo_hash, vk_access_token, vk_api_version):
    payload = {
        'photo': photo,
        'server': server,
        'hash': photo_hash,
        'access_token': vk_access_token,
        'v': vk_api_version
    }
    response = requests.post(f'{vk_url}/{method_name}', payload)
    check_vk_response(response)
    photo_parameters = response.json()
    photo_owner_id = photo_parameters['response'][0]['owner_id']
    photo_id = photo_parameters['response'][0]['id']
    return photo_owner_id, photo_id


def post_vk_wall(vk_url, method_name, owner_id, from_group, attachments, message, vk_access_token, vk_api_version):
    payload = {
        'owner_id': owner_id,
        'from_group': from_group,
        'attachments': attachments,
        'message': message,
        'access_token': vk_access_token,
        'v': vk_api_version
    }
    response = requests.post(f'{vk_url}/{method_name}', payload)
    check_vk_response(response)
    return f'Your post_id - {response.json()["response"]["post_id"]}'


def main():
    dotenv.load_dotenv()
    last_comic_url = 'https://xkcd.com/info.0.json'
    random_comic_number = get_random_comic_number(last_comic_url)
    random_comic_url = f'https://xkcd.com/{random_comic_number}/info.0.json'
    comic_image_url, comic_title = get_comic_parameters(random_comic_url)
    comic_file_name = comic_image_url.split('/')[-1]
    download_image(comic_image_url, comic_file_name)
    vk_url = 'https://api.vk.com/method/'
    upload_method_name = 'photos.getWallUploadServer'
    save_method_name = 'photos.saveWallPhoto'
    wall_posting_method_name = 'wall.post'
    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    vk_group_id = os.getenv('VK_GROUP_ID')
    vk_api_version = '5.130'
    upload_url = get_vk_upload_url(vk_url, upload_method_name, vk_access_token, vk_api_version)
    server, photo, photo_hash = get_vk_uploading_photo_parameters(upload_url, comic_file_name)
    photo_owner_id, photo_id = get_vk_saving_uploading_photo_parameters(
        vk_url, save_method_name, server, photo, photo_hash, vk_access_token, vk_api_version)
    from_group = 1
    attachments = f'photo{photo_owner_id}_{photo_id}'
    print(post_vk_wall(
        vk_url, wall_posting_method_name, vk_group_id, from_group, attachments, comic_title, vk_access_token, vk_api_version))
    os.remove(comic_file_name)


if __name__ == '__main__':
    main()
