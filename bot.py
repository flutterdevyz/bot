import asyncio
import sqlite3

from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ContentType
)
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage


# ================= TOKEN =================

TOKEN = "8740388801:AAF8jW7DwM5rf9jzJ851cYmE3gXLJLsVZcM"
ADMIN_NUMBER = "+998777360751"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


# ================= DATABASE =================

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
name TEXT,
age INTEGER,
role TEXT,
stress INTEGER,
phone TEXT
)
""")

# Media table 🔥
cursor.execute("""
CREATE TABLE IF NOT EXISTS media(
id INTEGER PRIMARY KEY AUTOINCREMENT,
file_id TEXT,
type TEXT
)
""")

conn.commit()


# ================= STATES =================

class ProfileState(StatesGroup):
    name = State()
    age = State()
    role = State()
    stress = State()
    phone = State()


# ================= KEYBOARDS =================

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧘 Meditatsiya")],
        [KeyboardButton(text="🌬 Nafas mashqlari")],
        [KeyboardButton(text="🎯 Diqqatni jamlash")],
        [KeyboardButton(text="💆 Relaksatsiya")],
        [KeyboardButton(text="😴 Uyqu")],
        [KeyboardButton(text="📊 Test va monitoring")],
        [KeyboardButton(text="📅 Kundalik")],
        [KeyboardButton(text="🆘 Favqulodda yordam")],
        [KeyboardButton(text="⭐ Premium")],
        [KeyboardButton(text="ℹ Loyiha haqida")],
        [KeyboardButton(text="📤 Media yuklash")]
    ],
    resize_keyboard=True
)

phone_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Telefon yuborish", request_contact=True)]
    ],
    resize_keyboard=True
)


# ================= START =================

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(ProfileState.name)
    await message.answer("Ismingizni kiriting:")


# ================= PROFILE STEPS =================

@dp.message(ProfileState.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(ProfileState.age)
    await message.answer("Yoshingizni kiriting:")


@dp.message(ProfileState.age)
async def get_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(ProfileState.role)
    await message.answer("Talaba / O‘quvchi / Boshqa?")


@dp.message(ProfileState.role)
async def get_role(message: Message, state: FSMContext):
    await state.update_data(role=message.text)
    await state.set_state(ProfileState.stress)
    await message.answer("Stress darajangiz (1-10):")


@dp.message(ProfileState.stress)
async def get_stress(message: Message, state: FSMContext):
    await state.update_data(stress=message.text)
    await state.set_state(ProfileState.phone)

    await message.answer(
        "Telefon raqamingizni yuboring:",
        reply_markup=phone_button
    )


# ================= PHONE + ADMIN CHECK =================

@dp.message(ProfileState.phone, F.content_type == ContentType.CONTACT)
async def get_phone(message: Message, state: FSMContext):

    phone_number = message.contact.phone_number
    data = await state.get_data()

    role = "USER"

    if ADMIN_NUMBER.replace("+", "") in phone_number:
        role = "ADMIN"

    cursor.execute("""
    INSERT OR REPLACE INTO users(id,name,age,role,stress,phone)
    VALUES(?,?,?,?,?,?)
    """, (
        message.from_user.id,
        data["name"],
        data["age"],
        role,
        data["stress"],
        phone_number
    ))

    conn.commit()
    await state.clear()

    await message.answer(
        f"✅ Profil saqlandi\nRol: {role}",
        reply_markup=menu
    )


# ================= ADMIN MEDIA UPLOAD =================

@dp.message(F.text == "📤 Media yuklash")
async def admin_media(message: Message):

    cursor.execute("SELECT role FROM users WHERE id=?", (message.from_user.id,))
    user = cursor.fetchone()

    if not user or user[0] != "ADMIN":
        await message.answer("❌ Siz admin emassiz!")
        return

    await message.answer("📎 Rasm yoki video yuboring.")


@dp.message(F.content_type.in_({ContentType.PHOTO, ContentType.VIDEO}))
async def save_media(message: Message):

    cursor.execute("SELECT role FROM users WHERE id=?", (message.from_user.id,))
    user = cursor.fetchone()

    if not user or user[0] != "ADMIN":
        return

    if message.photo:
        file_id = message.photo[-1].file_id
        media_type = "photo"
    else:
        file_id = message.video.file_id
        media_type = "video"

    # 🔥 MEDIA DATABASE GA SAQLANADI
    cursor.execute(
        "INSERT INTO media(file_id,type) VALUES(?,?)",
        (file_id, media_type)
    )
    conn.commit()

    await message.answer("✅ Media saqlandi!")


# ================= MODULES =================

@dp.message(F.text == "🧘 Meditatsiya")
async def meditation(message: Message):
    await message.answer(
        "🧘 Meditatsiya:\n\n"
        "1️⃣ 5 daqiqa\n"
        "2️⃣ 10 daqiqa\n"
        "3️⃣ Audio\n"
        "4️⃣ Favqulodda"
    )


@dp.message(F.text == "🌬 Nafas mashqlari")
async def breathing(message: Message):
    await message.answer(
        "🌬 Nafas:\n"
        "🔹 4-4-4-4\n"
        "🔹 4-7-8\n"
        "🔹 5 daqiqa"
    )


@dp.message(F.text == "🎯 Diqqatni jamlash")
async def focus(message: Message):
    await message.answer(
        "🎯 Mindfulness:\n"
        "✔ Fokus\n"
        "✔ 5-4-3-2-1\n"
        "✔ Test"
    )


@dp.message(F.text == "💆 Relaksatsiya")
async def relax(message: Message):
    await message.answer(
        "💆 Relaksatsiya:\n"
        "🔸 Mushak\n"
        "🔸 Tana skanerlash\n"
        "🔸 Ko'z mashqi"
    )


@dp.message(F.text == "📊 Test va monitoring")
async def monitoring(message: Message):
    await message.answer(
        "📊 Testlar:\n"
        "/test yozib testni boshlang"
    )


@dp.message(F.text == "📅 Kundalik")
async def daily(message: Message):
    await message.answer(
        "📅 Kundalik:\n"
        "Kayfiyat\nStress\nEnergiya"
    )


@dp.message(F.text == "🆘 Favqulodda yordam")
async def emergency(message: Message):
    await message.answer(
        "⚠ 1 daqiqalik nafas:\n"
        "4 soniya nafas\n"
        "4 soniya ushlab tur\n"
        "4 soniya chiqar"
    )


@dp.message(F.text == "⭐ Premium")
async def premium(message: Message):
    await message.answer(
        "⭐ Premium:\n"
        "✔ Psixolog\n"
        "✔ Individual tavsiya\n"
        "✔ Grafik"
    )


@dp.message(F.text == "ℹ Loyiha haqida")
async def about(message: Message):
    await message.answer(
        "🧠 Xotirjamlik bot — ruhiy salomatlik platformasi."
    )


# ================= RUN =================

async def main():
    print("✅ Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())