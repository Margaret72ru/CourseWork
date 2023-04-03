import time
from pbar import ProgressBar
from vk import VK
from yadisk import YaUploader


def get_vk_token():
    with open("..\\VK_token.txt") as f:
        return f.readline()


def get_ya_token():
    with open("..\\token.txt") as f:
        return f.readline()


if __name__ == '__main__':
    progress = ProgressBar()
    print("Загрузка фоток из профиля VK на Яндекс диск.")
    print("Инициализация VK token...")
    vkToken = get_vk_token()
    print("Инициализация Яндекс token...")
    yaToken = get_ya_token()
    print("Токены инициализированы.")
    vkId = input("Введите ID пользователя VK:")
    vk = VK(vkToken, vkId, progress)
    vkPhotos = vk.get_five_best_photos()
    print("Фотографии определены.")
    print("Введите название директории на Яндекс диске для загрузки фотографий:")
    yaDir = input("Директория (по умолчанию VK-Photos):")
    if len(yaDir) == 0:
        yaDir = "VK-Photos"
    yaDisk = YaUploader(yaToken)
    print("Яндекс диск инициализирован.")
    print("Создание директории " + yaDir)
    res = yaDisk.create_dir(yaDir)
    if res.status_code == 201:
        print("Директория " + yaDir + " создана.")
    elif res.status_code == 409:
        print("Директория " + yaDir + " уже существует, работа продолжается...")
    else:
        print(res.text)
        exit(-1)
    progress.setup("Загрузка фотографий на Яндекс диск...", len(vkPhotos))
    with open("result.txt", "w") as f:
        f.write('{\n')
        try:
            js_lines = []
            for item in vkPhotos:
                res = yaDisk.upload(yaDir + "/" + item, vkPhotos[item][1])
                progress.next()
                time.sleep(0.1)
                print(flush=True)
                js_lines.append(f'"{item}": "{vkPhotos[item][1]}"')
        finally:
            f.write(',\n'.join(js_lines))
            f.write('\n}')
    print("Загрузка фотографий успешно завершена!")
