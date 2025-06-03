import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

API_TOKEN = '7828861240:AAGaewzp3BvS3fISYz5z7cMeXY761LKBPDo'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

ADMIN_TELEGRAM = "@sardorbeksobirjonov"
ADMIN_PHONE = "94 089 81 19"
ADMIN_CHAT_ID = 7752032178  # Adminning chat idsi

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📋 Menu 📜"),
            KeyboardButton(text="🛒 Buyurtma berish 📝"),
            KeyboardButton(text="📞 Adminlar bilan bog'lanish 🤝"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

services = [
    "🤖 Telegram bot yasash 🤖",
    "🌐 Web sayt yaratish 🌐",
    "🎨 Logi yasash 🎨",
    "🖼️ Banner yasash 🖼️",
    "🎞️ Animatsiya tayorlash 🎞️",
    "📊 Slide tayorlash 📊",
    "📄 Diplom va rezume tayorlash 📄",
    "✉️ Taklifnoma tayorlash ✉️",
    "🎉 Tug‘ilgan kun uchun tabrik tayorlash 🎉",
    "🎥 Video va audio montaj qilish 🎥",
    "📚 PDF qilish 📚",
    "🆔 Telegram nik yaratish 🆔",
    "🖼️ Ismga rasm va video tayorlash 🖼️",
    "⚙️ Ishlar bajarish ⚙️",
    "👤 Avatar tayorlash 👤",
    "📈 Nakrutka qilish 📈",
    "📱 Telegram akkaunt olish 📱",
    "🖥️ 3D ko‘rinishdagi loyihalar 🖥️",
    "✨ Va boshqa xizmatlarimiz mavjud ✨"
]

menu_text = "📋 *MENU* 📋\n\n" + "\n".join(f"• {item}" for item in services)

user_states = {}

WAITING_FOR_ORDER = "waiting_for_order"
WAITING_FOR_PHONE = "waiting_for_phone"
WAITING_FOR_AD_TEXT = "waiting_for_ad_text"

# Foydalanuvchilar ro'yxatini saqlash uchun oddiy ro'yxat (ishni davom ettirish uchun)
all_users = set()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    all_users.add(user_id)  # foydalanuvchini ro'yxatga qo'shish
    await message.answer(
        "👋 Assalomu alaykum!\n\n"
        "Quyidagi tugmalardan birini tanlang va xizmatlarimizdan foydalaning👇",
        reply_markup=start_keyboard
    )
    user_states.pop(user_id, None)

@dp.message()
async def all_messages_handler(message: Message):
    user_id = message.from_user.id
    text = message.text
    all_users.add(user_id)  # har safar yangilarini qo'shamiz

    # Buyurtma jarayoni holati
    if user_id in user_states:
        state = user_states[user_id]

        if state == WAITING_FOR_ORDER:
            user_states[user_id] = {
                "step": WAITING_FOR_PHONE,
                "order": text
            }
            await message.answer(
                "✅ Buyurtmangiz qabul qilindi!\n"
                "📲 Iltimos, telefon raqamingizni kiriting:\n"
                "📲 Masalan: +998 94 089 00 00",
                reply_markup=ReplyKeyboardRemove()
            )
            return

        elif isinstance(state, dict) and state.get("step") == WAITING_FOR_PHONE:
            order = state.get("order")
            phone = text

            admin_msg = (
                f"📩 *Yangi buyurtma kelib tushdi!*\n\n"
                f"👤 Foydalanuvchi: @{message.from_user.username if message.from_user.username else 'No username'}\n"
                f"🆔 ID: {user_id}\n"
                f"📞 Telefon raqam: {phone}\n"
                f"🛒 Buyurtma: {order}"
            )
            try:
                await bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_msg)
            except Exception as e:
                print(f"❌ Adminlarga xabar yuborishda xato: {e}")

            await message.answer(
                "🎉 Buyurtmangiz qabul qilindi va adminlarga yuborildi!\n\n"
                f"📞 Adminlar bilan bog‘lanish:\n"
                f"💬 Telegram: {ADMIN_TELEGRAM}\n"
                f"📱 Telefon: +{ADMIN_PHONE}",
                reply_markup=start_keyboard
            )
            user_states.pop(user_id, None)
            return

        # Reklama matnini qabul qilish
        elif state == WAITING_FOR_AD_TEXT and user_id == ADMIN_CHAT_ID:
            ad_text = text
            sent_count = 0
            for uid in all_users:
                try:
                    await bot.send_message(uid, f"📢 *Reklama:* \n\n{ad_text}")
                    sent_count += 1
                except Exception as e:
                    print(f"❌ {uid} ga reklama yuborishda xato: {e}")
            await message.answer(f"✅ Reklama {sent_count} ta foydalanuvchiga yuborildi!", reply_markup=start_keyboard)
            user_states.pop(user_id, None)
            return

    # Tugmalar va matn bo‘yicha javoblar
    if text == "📋 Menu 📜":
        await message.answer(menu_text, reply_markup=start_keyboard)
    elif text == "🛒 Buyurtma berish 📝":
        user_states[user_id] = WAITING_FOR_ORDER
        await message.answer(
            "✍️ Iltimos, kerakli xizmat nomini kiriting (masalan: logo):",
            reply_markup=ReplyKeyboardRemove()
        )
    elif text == "📞 Adminlar bilan bog'lanish 🤝":
        contact_text = (
            "📞 *Adminlar bilan bog'lanish:* 🤝\n\n"
            f"👤 Admin: {ADMIN_TELEGRAM}\n"
            f"📱 Telefon: +{ADMIN_PHONE}\n\n"
            "📩 Siz har qanday savol bilan adminlarga murojaat qilishingiz mumkin.\n"
            "🔔 Tez orada sizga javob berishadi!"
        )
        await message.answer(contact_text, reply_markup=start_keyboard)
    elif text.lower() == "reklama1020":
        # Faqat adminga reklama matnini so'raymiz
        if user_id == ADMIN_CHAT_ID:
            user_states[user_id] = WAITING_FOR_AD_TEXT
            await message.answer("📢 Iltimos, reklama matnini kiriting:")
        else:
            await message.answer("❌ Bu buyruq faqat admin uchun!")
    else:
        await message.answer(
            "❗ Iltimos, menyudan birini tanlang yoki /start buyrug'ini yuboring.",
            reply_markup=start_keyboard
        )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
