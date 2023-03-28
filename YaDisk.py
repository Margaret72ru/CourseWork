import requests


class YaUploader:
    def __init__(self, token: str):
        self.Token = token
        self.Url = "https://cloud-api.yandex.net/v1/disk/resources"
        self.Headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {self.Token}'}

    def create_dir(self, disk_dir: str):
        res = requests.get(self.Url, headers=self.Headers)
        if res.status_code != 400:
            return f"Error: {res.text}"
        res = requests.put(f'{self.Url}?path={disk_dir}', headers=self.Headers)
        return res

    def upload(self, file_name: str, file_url: str):
        res = requests.get(self.Url, headers=self.Headers)
        if res.status_code != 400:
            return f"Error: {res.text}"

        res = requests.post(f'{self.Url}/upload?path={file_name}&url={file_url}', headers=self.Headers)
        return res
