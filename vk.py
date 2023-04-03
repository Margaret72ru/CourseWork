import os
import time
from pbar import ProgressBar
import requests


class VK:
    def __init__(self, token, uid, progress: ProgressBar, version='5.131'):
        self._progress = progress
        self._token = token
        self._id = uid
        self._version = version
        self._params = {'access_token': self._token, 'v': self._version}

    def get_photos_data(self, offset=0, count=250):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': self._id,
            'album_id': 'profile',  # получение фотографий профиля
            'extended': '1',  # доп.параметры (лайки)
            'access_token': self._token,
            'v': '5.131',
            'count': count,
            'offset': offset
        }
        res = requests.get(url, params=params)  # запрос получения фотографий
        return res.json()

    def get_five_best_photos(self):
        part_size = 250
        current_part = self.get_photos_data(count=part_size)
        all_photos_count = current_part['response']['count']
        self._progress.setup("Запрос фотографий VK профиля...", all_photos_count)
        index = 0
        result = {}
        while all_photos_count > index:
            for files in current_part['response']['items']:
                index += 1
                file_name = str(files['likes']['count'])
                f = sorted(files['sizes'], key=lambda item: item['type'], reverse=True)[0]
                f_type = f['type'][-1]
                f_ext = str.split(os.path.splitext(f['url'])[1], sep='?')[0]
                file_name_full = file_name + f_ext
                while result.__contains__(file_name_full):
                    file_name_full = file_name + '-' + str(files['date']) + f_ext
                result[file_name_full] = (f_type, f['url'])
                time.sleep(0.3)  # имитация долгой работы )))))
                self._progress.next()
                print(flush=True)  # чтобы прогресс выводился
            if all_photos_count > index:
                current_part = self.get_photos_data(offset=index, count=part_size)

        all_photos = sorted(result.items(), key=lambda item: item[1][0])
        if len(all_photos) > 5:
            res = all_photos[:5]
        else:
            res = all_photos
        return dict(res)
