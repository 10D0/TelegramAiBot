import asyncio
from logging import exception
from io import BytesIO
from re import compile
# импорт классов из библиотеки Aiogram для работы с ботом
from aiogram import Router, F, types, Bot
from aiogram.exceptions import TelegramRetryAfter
from aiogram.filters import Command, CommandObject, BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.methods.close import Close
from aiogram.types import Message, FSInputFile, BufferedInputFile
# импорт методов из других модулей проекта
from Generators import LanguageModel, ImageModel


# Создание Роутера
# нужен Роутер для обработки запросов от пользователя
router = Router()
# переменная отвечающая за то является ли бот запущенным
IsOn = False


# Состояние бота
class Generate(StatesGroup):
    text = State()

# фильтр для проверки того включен бот или нет(булевая переменная)
class MyFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return IsOn


# проверка состояния бота при получении запрос от пользователя
@router.message(Generate.text)
async def generate_error(message: Message):
    await message.answer("""Происходит генерация ответа, 
    подождите""")


# обработка команды /start и приветственное сообщение
@router.message(Command('start'), ~MyFilter())
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    print('Начало работы бота')
    global IsOn
    IsOn = True
    await message.answer("""Привет!

    Меня зовут Estafano. Я бот ассисент, наделенный искусственным интеллектом, созданный, чтобы помогать вам в поиске полезной информации и других возможностях.

    Если у вас есть вопросы или вы хотите, чтобы я что-то сделал, пожалуйста, введите команду /start, и я начну работу.

    Вы также можете использовать другие команды, чтобы управлять мной:

    /start — прекратить работу бота;
    /help — получить список команд и информацию о них;
    /GenerateImage {запрос на генерацию изображения} — Создание изображения по запросу;
    /stop — прекратить работу бота;

    Если вы столкнулись с проблемой, не стесняйтесь обращаться. Я готов помочь! 😊""")
    await state.clear()


# обработчик команды /stop
@router.message(Command('stop'), MyFilter())
async def stop_bot(message, bot: Bot):
    print('Прекращение работы бота')
    await message.reply("Прекращение работы бота.")
    global IsOn
    IsOn = False
    while True:
        try:
            await bot(Close())
            break
        except TelegramRetryAfter as e:
            exception(f'Произошла ошибка: {e}')
            print(f"Сервера Telegram'а: {e.message}. Попробуйте выключение бота через {e.retry_after} секунд.")
            await asyncio.sleep(e.retry_after + 1)


# обработка команд /help
@router.message(Command(compile(r'(H|h)elp(@(E|e)fano(B|b)ot)?')))
async def help(message: Message, state: FSMContext):
    print('Вызов команды /help')
    await state.set_state(Generate.text)
    response = '''Команды бота:
    /start — начать работу бота;
    
    /help — получить список команд и информацию о них;
    
    /GenerateImage {запрос на генерацию изображения} — Создание изображения по запросу;
    
    /stop — прекратить работу бота;
    
    Для получение ответа просто напиши сообщение'''
    await message.answer(response)
    await state.clear()


# обработка запроса на генерацию изображения
@router.message(Command(compile(r'(G|g)enerate(I|i)mage(@(E|e)fano(B|b)ot)?')), MyFilter())
async def GenerateImageAnswer(message: Message, command: CommandObject):
    args = command.args
    print('args:   ', args)
    try:
        image = await ImageModel(args)
        image_data = BytesIO()
        image.image.save(image_data, format="PNG")
        image_data.seek(0)
        image_bytes = image_data.getvalue()
        await message.reply_photo(photo=BufferedInputFile(image_bytes, filename="photo.png"), caption="Вот ваше изображение")
    except Exception as e:
        await message.answer(f'Произошла ошибка при генерации изображения')
        exception(f'Произошла ошибка: {e}')
        print(f'Произошла ошибка: {e}')


# обработка запроса на генерацию текста
@router.message(F.text, MyFilter())
async def GenerateTextAnswer(message: Message, state: FSMContext) -> None:
    msg = message.text.lower()
    print(f'Запрос с текстом:   {msg}')
    await state.set_state(msg)
    try:
        task = asyncio.create_task(LanguageModel(message.text))
        response = await task
        await message.answer(response, parse_mode="html")
    except Exception as e:
        await message.answer(f'Произошла ошибка при генерации ответа')
        exception(f'Произошла ошибка: {e}')
        print(f'Произошла ошибка: {e}')
    finally:
        await state.clear()
