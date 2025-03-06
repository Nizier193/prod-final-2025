from pathlib import Path
from redis import Redis
from telebot import TeleBot
from telebot.types import Message
from telebot import types
from telebot.apihelper import ApiException

import sys
import signal
import time

from core.cache import get_cache
from core.config import config

from src.api.client_service import ClientAPIService
from src.utils.support import check_uuid
from src.repositories.cache_repository import CacheRepository

bot = TeleBot(token=config.TELEGRAM_TOKEN)
client_service = ClientAPIService()

BASE_PATH = Path("src/bot/resources")

@bot.message_handler(commands=["start"])
def start(message: Message):
    image = open(BASE_PATH / Path("PRODLOGO.jpg"), "rb")

    # Нужно сюда вмонтировать картинку сверху
    bot.send_photo(
        message.chat.id, 
        caption=(
            f"Здравствуйте! \n"
            f"Это рекламный бот, созданный для просмотра рекламы пользователями и работы рекламодателей с рекламой. \n\n"
            f"Для начала вам необходимо войти в систему:\n"
            f"/client_sign_in"
        ),
        photo=image
    )


def insert_client_id(message: Message, cache: CacheRepository):
    client_id = message.text

    # Сообщение пустое.
    if not (client_id):
        bot.send_message(
            message.chat.id,
            text="Client-ID не был получен =("
        )
        return

    # Сообщение невалидно (не UUID)
    if not (check_uuid(client_id)):
        bot.send_message(
            message.chat.id,
            text="Ваш ID не соответствует формату UUID (это не Client-ID). Отправьте только ваш Client-ID"
        )
        return

    # Фиксируем Client-ID в кеш.
    cache.cache_client_id(
        str(message.chat.id), 
        str(client_id),
        time=3600 # Ставим в кеш на час
    )
    
    bot.send_message(
        message.chat.id,
        text="Ваш Client-ID был успешно зафиксирован! \nТеперь можно приступить к просмотру объявлений. \n/get_ad",
    )


@bot.message_handler(commands=["client_sign_in"])
def client_sign_in(message: Message):
    cache = CacheRepository(next(get_cache())) # Получение кеша

    bot.send_message(
        message.chat.id, 
        text="""
        Отправьте ваш Client-Id следующим сообщением для работы!
        """
    )
    bot.register_next_step_handler(
        message=message, 
        callback=lambda message: insert_client_id(message, cache)
    )




@bot.message_handler(commands=["get_ad"])
def client_get_ad(message: Message):
    cache = CacheRepository(next(get_cache()))

    client_id = cache.get_cached_client_id(user_id=str(message.chat.id))
    if not client_id:
        bot.send_message(
            message.chat.id,
            text="Вы ещё не ввели свой Client-ID."
        )
        return
    
    ad = client_service.client_view_ad(clientId=client_id)
    if not ad:
        bot.send_message(
            message.chat.id,
            text="К сожалению, больше нет доступной рекламы. =("
        )
        return
    ad_text = ad.to_str()  # Текст превью рекламы

    # Создание инлайн-кнопок
    markup = types.InlineKeyboardMarkup()
    btn_next = types.InlineKeyboardButton("Следующая реклама >>", callback_data="next_ad")
    btn_detail = types.InlineKeyboardButton("Подробнее", callback_data=f"detail:{ad.ad_id}")
    markup.add(btn_next, btn_detail)

    bot.send_message(
        message.chat.id,
        text=ad_text,
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('detail:'))
def handle_detail_callback(call):
    ad_id = call.data.split(':')[1]
    cache = CacheRepository(next(get_cache()))
    client_id = cache.get_cached_client_id(user_id=str(call.message.chat.id))
    
    if not client_id:
        bot.answer_callback_query(call.id, "Ошибка: Client-ID не найден.")
        return

    ad_clicked = client_service.client_click_ad(clientId=client_id, adId=ad_id)
    if not ad_clicked:
        bot.answer_callback_query(call.id, "Нельзя перейти по рекламе.")
        return

    # Обновляем сообщение с полным текстом и удаляем кнопки
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=ad_clicked.to_str(),
        reply_markup=None
    )


@bot.callback_query_handler(func=lambda call: call.data == 'next_ad')
def handle_next_ad_callback(call):
    cache = CacheRepository(next(get_cache()))
    client_id = cache.get_cached_client_id(user_id=str(call.message.chat.id))
    
    if not client_id:
        bot.answer_callback_query(call.id, "Ошибка: Client-ID не найден.")
        return

    ad = client_service.client_view_ad(clientId=client_id)
    if not ad:
        bot.send_message(
            chat_id=call.message.chat.id,
            text="К сожалению, больше нет доступной рекламы. =("
        )
        return

    markup = types.InlineKeyboardMarkup()
    btn_next = types.InlineKeyboardButton("Следующая реклама >>", callback_data="next_ad")
    btn_detail = types.InlineKeyboardButton("Подробнее", callback_data=f"detail:{ad.ad_id}")
    markup.add(btn_next, btn_detail)

    # Удаляем старое сообщение
    bot.delete_message(call.message.chat.id, call.message.message_id)
    
    # Отправляем новое
    bot.send_message(
        chat_id=call.message.chat.id,
        text=ad.to_str(),
        reply_markup=markup
    )


running = True

def signal_handler(sig, frame):
    global running
    running = False

    bot.stop_polling()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

while running:
    try:
        bot.polling(non_stop=True)

    except ApiException as e:
        if running:
            time.sleep(5)
            continue

    except Exception as e:
        if running:
            time.sleep(5)
            continue

