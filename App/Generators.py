from os import getenv, path, getcwd
from typing import Any
from dotenv import load_dotenv
from logging import exception
# импорт апи Google translator
from googletrans import Translator
# импорт апи YandexGPT
from yandexgptlite import YandexGPTLite
# импорт интерфеса stable-diffusion-webui для работы взаимодействия с вебинтерфейсом Stable Diffusion
from webuiapi import WebUIApi


# импорт из файла данных

# Получаем путь к каталогу с файлом .env
dotenv_path = getcwd()+'\.env'
exception(f'\n\n\ndotenv_path = {dotenv_path}\n\n\n{getcwd()}\n\n\n')
load_dotenv(dotenv_path,encoding='latin-1')
# импорт хоста и порта
host = str(getenv('HOST'))
port = str(getenv('PORT'))


# подключение к апи YandexGPT
try:
    account = YandexGPTLite(folder=str(getenv('LIB')),token=str(getenv('API_TOKEN')))
except Exception as e:
    # Записываем сообщение об ошибке в логгер
    a = str(getenv('API_TOKEN'))
    b = str(getenv('LIB'))
    exception(f'\n\nAPI_TOKEN\nlib = {b}\napitoken = {a}\nПроизошла ошибка: {e}')

# Генерация текстового ответа
async def LanguageModel(question: str) -> str:
    text = account.create_completion(question, '0.9')
    print(text)
    # возврат сгенерированного текста
    return str(text)


# Генерация изображения по запросу
async def ImageModel(question: str) -> Any:
    # перевод запроса на английский язык
    translator = Translator()
    question = translator.translate(question, dest='en').text
    print('Запрос:  ' + question)
    # создание апи клиента
    api = WebUIApi(host=host, port=port)
    # запрос на генерацию изображения с клиента
    result1 = api.txt2img(prompt=question,
                          negative_prompt="ugly, out of frame",
                          seed=-1,
                          #styles=["anime"],
                          cfg_scale=7,
                          steps=15,
                          save_images=True
                          )
    # вывод информации о сгенерированном изображении
    print(result1.info)
    # возврат сгенерированного изображения
    return result1
