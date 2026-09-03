from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Text

from loader import dp

# ===== ТВОИ ПЕРЕМЕННЫЕ =====
VIDEO_URL = "http://195.133.60.26:8080/vecherniy.mp4"
CLUB_BOT_LINK = "https://t.me/livi_club_bot"
SITE_LINK = "https://leralivi.ru/"

BTN_GET_COMPLEX = "🎥 Хочу получить комплекс"
BTN_CLUB = "Хочу в клуб. Перейти для подписки"
BTN_SITE = "🌐 Узнать подробнее"
BTN_SHARE_PHONE = "📱 Поделиться номером"

COMPLEX_TEXT = (
    "Вечерний комплекс — 15 минут. Делай перед сном, в удобной одежде, "
    "на коврике или прямо в кровати.\n\n"
    "[🎥 Смотреть видео «Лера Ливи»](http://195.133.60.26:8080/vecherniy.mp4)\n\n"
    "Сделаешь — напиши мне, что почувствовала. Мне важно знать 💛\n\n"
    "Если хочешь задать вопрос лично — просто напиши мне в этот чат."
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

CLUB_SUCCESS_TEXT = (
    "Супер! Твой номер телефона получен 📱\n\n"
    "Добавляю тебя в список участников клуба. Я свяжусь с тобой в ближайшее время "
    "(в течение часа), чтобы подтвердить доступ и отправить все материалы.\n\n"
    "Добро пожаловать в LIVICLUB! 🕊✨"
)

# ===== ОБРАБОТЧИК КНОПКИ "Хочу получить комплекс" =====
@dp.message(Text(text=BTN_GET_COMPLEX))
async def handle_get_complex(message: types.Message):
    await message.answer(
        COMPLEX_TEXT,
        reply_markup=CLUB_KEYBOARD,
        parse_mode='Markdown'
    )

# ===== ОБРАБОТЧИК КНОПКИ "Хочу в клуб. Перейти для подписки" =====
@dp.message(Text(text=BTN_CLUB))
async def handle_club_button(message: types.Message):
    await message.answer(
        "Нажми на кнопку ниже, чтобы поделиться номером:",
        reply_markup=PHONE_KEYBOARD
    )

# ===== ОБРАБОТЧИК КНОПКИ "Узнать подробнее" =====
@dp.message(Text(text=BTN_SITE))
async def handle_site_button(message: types.Message):
    await message.answer(
        f"Подробнее о клубе на сайте: {SITE_LINK}"
    )

# ===== ОБРАБОТЧИК НОМЕРА ТЕЛЕФОНА =====
@dp.message(lambda message: message.contact is not None)
async def handle_contact(message: types.Message):
    phone = message.contact.phone_number
    user_id = message.from_user.id
    
    # Сохраняем номер в базе (если есть)
    # Здесь можно добавить сохранение в БД
    
    await message.answer(
        CLUB_SUCCESS_TEXT,
        reply_markup=SITE_ONLY_KEYBOARD
    )
    await message.answer(
        f"Для подписки перейди в бота: {CLUB_BOT_LINK}"
    )