import requests


class YaUploader:
    def __init__(self, token: str):
        self._token = token
        self._url = "https://cloud-api.yandex.net/v1/disk/resources"
        self._headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {self._token}'}

    def create_dir(self, disk_dir: str):
        res = requests.get(self._url, headers=self._headers)
        if res.status_code != 400:
            return f"Error: {res.text}"
        res = requests.put(self._url, params={'path': disk_dir}, headers=self._headers)
        return res

    def upload(self, file_name: str, file_url: str):
        res = requests.get(self._url, headers=self._headers)
        if res.status_code != 400:
            return f"Error: {res.text}"
        res = requests.post(f'{self._url}/upload', params={'path': file_name, 'url': file_url}, headers=self._headers)
        return res
