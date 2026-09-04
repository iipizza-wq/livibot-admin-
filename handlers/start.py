import sqlite3
import os
from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

router = Router()
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "bot.db")

# === ТВОИ ПЕРЕМЕННЫЕ ===
VIDEO_URL = "http://195.133.60.26:8080/vecherniy.mp4"
CLUB_BOT_LINK = "https://t.me/livi_club_bot"
SITE_LINK = "https://leralivi.ru/"

BTN_GET_COMPLEX = "🎥 Хочу получить комплекс"
BTN_CLUB = "Хочу в клуб. Перейти для подписки"
BTN_SITE = "🌐 Узнать подробнее"
BTN_SHARE_PHONE = "📱 Поделиться номером"

START_TEXT = (
    "Привет!\n\n"
    "Я бот Леры Ливи. Здесь ты можешь получить короткий комплекс — "
    "под конкретный запрос твоего тела.\n\n"
    "Нажми на кнопку ниже, чтобы получить комплекс."
)

COMPLEX_TEXT = (
    "Вечерний комплекс — 15 минут. Делай перед сном, в удобной одежде, "
    "на коврике или прямо в кровати.\n\n"
    "[🎥 Смотреть видео «Лера Ливи»](http://195.133.60.26:8080/vecherniy.mp4)\n\n"
    "Сделаешь — напиши мне, что почувствовала. Мне важно знать 💛\n\n"
    "Если хочешь задать вопрос лично — просто напиши мне в этот чат."
)

CLUB_SUCCESS_TEXT = (
    "Супер! Твой номер телефона получен 📱\n\n"
    "Добавляю тебя в список участников клуба. Я свяжусь с тобой в ближайшее время "
    "(в течение часа), чтобы подтвердить доступ и отправить все материалы.\n\n"
    "Добро пожаловать в LIVICLUB! 🕊✨"
)

START_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=BTN_GET_COMPLEX)]],
    resize_keyboard=True
)

CLUB_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=BTN_CLUB)],
        [KeyboardButton(text=BTN_SITE)]
    ],
    resize_keyboard=True
)

PHONE_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=BTN_SHARE_PHONE, request_contact=True)],
        [KeyboardButton(text=BTN_SITE)]
    ],
    resize_keyboard=True
)

SITE_ONLY_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=BTN_SITE)]],
    resize_keyboard=True
)

def save_user(user_id: int, username: str = None, full_name: str = None):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT OR IGNORE INTO users (user_id, username, full_name) VALUES (?, ?, ?)",
            (user_id, username, full_name)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Ошибка сохранения пользователя: {e}")

def save_phone(user_id: int, phone: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "UPDATE users SET phone = ? WHERE user_id = ?",
            (phone, user_id)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Ошибка сохранения номера: {e}")

@router.message(CommandStart())
async def bot_start(message: types.Message):
    save_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name
    )
    await message.answer(
        "Начинаем заново!",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(START_TEXT, reply_markup=START_KEYBOARD)

@router.message(lambda message: message.text == BTN_GET_COMPLEX)
async def handle_get_complex(message: types.Message):
    await message.answer(
        COMPLEX_TEXT,
        reply_markup=CLUB_KEYBOARD,
        parse_mode='Markdown'
    )

@router.message(lambda message: message.text == BTN_CLUB)
async def handle_club_button(message: types.Message):
    await message.answer(
        "Нажми на кнопку ниже, чтобы поделиться номером:",
        reply_markup=PHONE_KEYBOARD
    )

@router.message(lambda message: message.text == BTN_SITE)
async def handle_site_button(message: types.Message):
    await message.answer(
        f"Подробнее о клубе на сайте: {SITE_LINK}"
    )

@router.message(lambda message: message.contact is not None)
async def handle_contact(message: types.Message):
    phone = message.contact.phone_number
    user_id = message.from_user.id
    save_phone(user_id, phone)
    await message.answer(
        CLUB_SUCCESS_TEXT,
        reply_markup=SITE_ONLY_KEYBOARD
    )
    await message.answer(
        f"Для подписки перейди в бота: {CLUB_BOT_LINK}"
    )
