import os
import requests
from urllib.parse import urljoin

class YaUploader:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"

    def _get_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"OAuth {self.token}"
        }

    def upload(self, file_path: str):
        """Метод загружает файл file_path на Яндекс.Диск с таким же именем."""
        # Проверяем, существует ли локальный файл
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден.")

        file_name = os.path.basename(file_path)
        disk_path = f"/{file_name}"  # Путь на Диске (в корне)

        params = {"path": disk_path, "overwrite": "true"}
        response = requests.get(self.base_url, headers=self._get_headers(), params=params)
        response.raise_for_status()  # Если статус не 200, вызовет исключение

        upload_data = response.json()
        href = upload_data.get("href")
        if not href:
            raise RuntimeError("Не удалось получить ссылку для загрузки.")


        with open(file_path, "rb") as f:
            upload_response = requests.put(href, data=f)
        upload_response.raise_for_status()

        return f"Файл '{file_name}' успешно загружен на Яндекс.Диск."

if __name__ == '__main__':
    # Вставьте ваш токен сюда (не публикуйте его в открытых источниках)
    token = " "  # Вставьте ваш токен сюда (не публикуйте его в открытых источниках)
    if not token:
        print("Ошибка: токен не указан. Получите токен на https://yandex.ru/dev/disk/poligon/")
    else:
        uploader = YaUploader(token)
        # Пример пути к файлу – измените на актуальный
        file_path = r"c:\my_folder\file.txt"
        try:
            result = uploader.upload(file_path)
            print(result)
        except Exception as e:
            print(f"Произошла ошибка: {e}")