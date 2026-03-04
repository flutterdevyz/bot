import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

TOKEN = "8740388801:AAE5CFKL6VBbyK9R80L1cd-Ndi_md82p4h8"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ================= MENU =================

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
        [KeyboardButton(text="⭐️ Premium")],
        [KeyboardButton(text="ℹ️ Loyiha haqida")],
    ],
    resize_keyboard=True
)

# ================= START =================

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "🧠 Xotirjamlik botiga xush kelibsiz!\n\n"
        "Avval ro'yxatdan o'tamiz.\n"
        "Ismingizni kiriting:"
    )

# ================= MENU HANDLERS =================

@dp.message(F.text == "🧘 Meditatsiya")
async def meditation(message: Message):
    await message.answer(
        "Meditatsiya tanlang:\n"
        "1️⃣ 5 daqiqalik tez tinchlanish\n"
        "2️⃣ 10 daqiqalik chuqur meditatsiya\n"
        "3️⃣ Favqulodda meditatsiya"
    )

@dp.message(F.text == "🌬 Nafas mashqlari")
async def breathing(message: Message):
    await message.answer(
        "Nafas texnikasini tanlang:\n"
        "🔹 4-4-4-4 Box breathing\n"
        "🔹 4-7-8 texnika\n"
        "🔹 Tezkor stress kamaytirish"
    )

@dp.message(F.text == "🎯 Diqqatni jamlash")
async def focus(message: Message):
    await message.answer(
        "Diqqat mashqlari:\n"
        "🔸 3 daqiqalik fokus\n"
        "🔸 5-4-3-2-1 texnika\n"
        "🔸 10 daqiqa diqqat sinovi"
    )

@dp.message(F.text == "💆 Relaksatsiya")
async def relax(message: Message):
    await message.answer("💆 Mushaklarni bo‘shashtirish mashqi boshlanmoqda...")

@dp.message(F.text == "😴 Uyqu")
async def sleep(message: Message):
    await message.answer("😴 Uyqudan oldingi audio va maslahatlar tayyorlanmoqda...")

@dp.message(F.text == "📊 Test va monitoring")
async def test_monitor(message: Message):
    await message.answer("📊 Stress testi boshlaymiz.\n\nBugun o'zingizni qanday his qilyapsiz? (1-10)")

@dp.message(F.text == "📅 Kundalik")
async def daily(message: Message):
    await message.answer("📅 Bugungi kayfiyatingizni baholang (1-10)")

@dp.message(F.text == "🆘 Favqulodda yordam")
async def emergency(message: Message):
    await message.answer(
        "⚠️ Hozir 1 daqiqalik nafas mashqini qilamiz.\n\n"
        "4 soniya nafas oling...\n"
        "4 soniya ushlab turing...\n"
        "4 soniya chiqaring...\n"
        "4 soniya kuting...\n\n"
        "Yaxshiroq his qilyapsizmi?"
    )

@dp.message(F.text == "⭐️ Premium")
async def premium(message: Message):
    await message.answer(
        "⭐️ Premium funksiyalar:\n"
        "🔹 Shaxsiy psixolog chat\n"
        "🔹 Individual tavsiyalar\n"
        "🔹 Chuqur testlar"
    )

@dp.message(F.text == "ℹ️ Loyiha haqida")
async def about(message: Message):
    await message.answer(
        "🧠 Xotirjamlik — yoshlar uchun stressni kamaytirish va ruhiy salomatlik boti."
    )

# ================= RUN =================

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())