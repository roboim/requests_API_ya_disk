import requests
import os
from pprint import pprint


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_folders_name(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        params = {"path": "/" + disk_file_path}
        response = requests.get(upload_url, headers=headers, params=params)
        if response.status_code == 200:
            print(f'Папка {disk_file_path} существует на диске ')
            return response.json()
        else:
            return self._make_dir(disk_file_path)

    def _make_dir(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        # print(headers)
        params = {"path": "/" + disk_file_path, "overwrite": "true"}
        response = requests.put(upload_url, headers=headers, params=params)
        # pprint(response.json())
        return response.json()

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        # pprint(response.json())
        return response.json()

    def upload_file_to_disk(self, filename, disk_file_path):
        f = os.path.basename(filename)
        print(f)
        disk_file_path = "/" + disk_file_path + "/" + f
        print(disk_file_path)
        href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")

    def upload(self, file_path, disk_path: str):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        self._get_folders_name(disk_path)
        self.upload_file_to_disk(file_path, path_disk)


if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    path_to_file = r'Укажите_абсолютный_путь'
    token = "..."
    # Файл сохранится в папку NETOLOGY
    path_disk = "NETOLOGY"

    uploader = YaUploader(token)
    result = uploader.upload(path_to_file, path_disk)
