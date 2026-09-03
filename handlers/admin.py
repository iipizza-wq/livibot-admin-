from aiogram import Router, types
from aiogram.filters import Command

# Создаём роутер
router = Router()

# Твой Telegram ID (узнай у @userinfobot)
ADMIN_IDS = [287889641]  # ЗАМЕНИ НА СВОЙ ID


@router.message(Command("admin"))
async def admin_command(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ У тебя нет доступа.")
        return

    await message.answer(
        "🔐 **Админ-панель**\n\n"
        "Здесь будут функции:\n"
        "• Рассылка сообщений\n"
        "• Статистика\n"
        "• Управление пользователями\n\n"
        "*(Функции в разработке)*",
        parse_mode="Markdown"
    )