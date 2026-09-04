from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import sqlite3
import os

router = Router()

# Твой ID
ADMIN_IDS = [287889641]  # ЗАМЕНИ НА СВОЙ ID

# База данных
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "bot.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_users_table():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            username TEXT,
            full_name TEXT,
            phone TEXT,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


class BroadcastStates(StatesGroup):
    waiting_for_message = State()


def admin_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="📨 Рассылка")],
            [KeyboardButton(text="👥 Пользователи")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )


@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ У тебя нет доступа.")
        return

    await message.answer(
        "🔐 **Админ-панель**\n\nВыбери действие:",
        parse_mode="Markdown",
        reply_markup=admin_keyboard()
    )


@router.message(F.text == "📊 Статистика")
async def admin_statistics(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    conn = get_db()
    users = conn.execute("SELECT COUNT(*) as count FROM users").fetchone()
    conn.close()

    total = users["count"] if users else 0

    await message.answer(
        f"📊 **Статистика**\n\n👥 Всего пользователей: {total}\n📅 За сегодня: 0\n\n*(Подробная статистика в разработке)*",
        parse_mode="Markdown",
        reply_markup=admin_keyboard()
    )


@router.message(F.text == "👥 Пользователи")
async def admin_users(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    conn = get_db()
    users = conn.execute(
        "SELECT user_id, username, full_name, phone, registered_at FROM users ORDER BY registered_at DESC LIMIT 10"
    ).fetchall()
    conn.close()

    if not users:
        await message.answer("📭 Пользователей пока нет.", reply_markup=admin_keyboard())
        return

    text = "👥 **Последние 10 пользователей:**\n\n"
    for u in users:
        text += f"🆔 {u['user_id']}\n"
        if u['username']:
            text += f"👤 @{u['username']}\n"
        text += f"📝 {u['full_name']}\n"
        if u['phone']:
            text += f"📱 {u['phone']}\n"
        text += f"📅 {u['registered_at']}\n\n"

    await message.answer(text, parse_mode="Markdown", reply_markup=admin_keyboard())


@router.message(F.text == "📨 Рассылка")
async def admin_broadcast_start(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return

    await state.set_state(BroadcastStates.waiting_for_message)
    await message.answer(
        "📨 **Рассылка**\n\nОтправь текст, который я разошлю всем пользователям.\n\n❗️ *Сообщение будет отправлено всем, кто есть в базе.*\nДля отмены отправь /cancel",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="🔙 Отмена")]],
            resize_keyboard=True
        )
    )


@router.message(F.text == "🔙 Отмена")
@router.message(Command("cancel"))
async def cancel_broadcast(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("✅ Рассылка отменена.", reply_markup=admin_keyboard())


@router.message(BroadcastStates.waiting_for_message)
async def send_broadcast(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return

    text = message.text

    conn = get_db()
    users = conn.execute("SELECT user_id FROM users").fetchall()
    conn.close()

    if not users:
        await message.answer("📭 Нет пользователей для рассылки.", reply_markup=admin_keyboard())
        await state.clear()
        return

    await message.answer("🚀 Начинаю рассылку...")

    sent = 0
    failed = 0

    for user in users:
        try:
            await message.bot.send_message(
                chat_id=user["user_id"],
                text=f"📨 **Сообщение от админа:**\n\n{text}",
                parse_mode="Markdown"
            )
            sent += 1
        except Exception:
            failed += 1

    await message.answer(
        f"✅ **Рассылка завершена!**\n\n📤 Отправлено: {sent}\n❌ Ошибок: {failed}",
        reply_markup=admin_keyboard()
    )
    await state.clear()


@router.message(F.text == "🔙 Назад")
async def admin_back(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    await admin_panel(message)
