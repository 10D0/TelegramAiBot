from logging import basicConfig, ERROR
from os.path import exists

basicConfig(filename='error.log', level=ERROR)


# Проверяем наличие файла .env
if not exists('.env'):
    # Создаем файл .env с пустыми полями
    with open('.env', 'w') as f:
        f.write('''#токен телеграмм бота
#тут должен быть токен бота из BotFather
TG_TOKEN=\n

# данные для подключения апи YandexGPT
#тут индефикатор из консоли Yandex.cloud
LIB=\n
#тут апи токен
API_TOKEN=\n

# данные для подключения к Stable Diffusion
# на локальном сервере в моем случае
HOST=127.0.0.1
PORT=7860''')

# Проверяем наличие файла README.txt
if not exists('README.txt'):
    # Создаем текстовый файл README с инструкциями
    with open('README.txt', 'w') as f:
        f.write('''
Прежде всего проверьте заполненость файла .env

.env содержит данные необходимые для работы телеграмм бота.

Бот использует YandexGPT(данные для его работы можно найти на Yandex.Cloud): https://yandex.cloud/ru/services/yandexgpt

После заполения файла .env сохраните его и запустите приложение с помощью исполнительного файла run.exe.
''')
