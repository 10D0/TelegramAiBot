import asyncio
from logging import exception
from os import getenv, getcwd
from dotenv import load_dotenv
# импорт классов из библиотеки Aiogram для работы с ботом
from aiogram import Bot, Dispatcher
# импорт роутеров из других модулей проекта
from Handlers import router


# Получаем путь к каталогу с файлом .env
dotenv_path = getcwd()+'\.env'
load_dotenv(dotenv_path,encoding='latin-1')


# main проекта
async def main():
    bot = Bot(token=str(getenv('TG_TOKEN')))
    dp = Dispatcher()
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(router)
    await dp.start_polling(bot, skip_updates=True)


# точка входа
if __name__ == '__main__':
    try:
        try:
            # Настраиваем логгер для записи сообщений об ошибках в файл error.log
            asyncio.run(main())
        except Exception as e:
            # Записываем сообщение об ошибке в логгер
            exception(f'Произошла ошибка: {e}')
    except KeyboardInterrupt:
        print('Бот выключен')
