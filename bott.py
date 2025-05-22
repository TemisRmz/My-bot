import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot("8157482865:AAFE3jvmcp5hC41w0frzY9w8ByS1JbCWYZE")  # توکن ربات

user_step = {}
user_data = {}
admin_chat_id = 6524398619  # آیدی عددی ادمین (تو)

@bot.message_handler(commands=['start'])
def start_handler(message):
    keyboard = InlineKeyboardMarkup()
    start_button = InlineKeyboardButton(text="شروع کنید", callback_data="start_process")
    keyboard.add(start_button)
    bot.send_message(message.chat.id, "برای شروع روی دکمه زیر بزنید:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "start_process")
def process_start(call):
    user_step[call.message.chat.id] = 'waiting_nft'
    user_data[call.message.chat.id] = {}
    bot.send_message(call.message.chat.id, "کد NFT خود را وارد کنید:")

@bot.message_handler(func=lambda message: user_step.get(message.chat.id) == 'waiting_nft')
def get_nft_code(message):
    user_data[message.chat.id]['nft_code'] = message.text
    user_step[message.chat.id] = 'waiting_wallet'
    bot.send_message(message.chat.id, "آدرس ولت خود را وارد کنید:")

@bot.message_handler(func=lambda message: user_step.get(message.chat.id) == 'waiting_wallet')
def get_wallet_address(message):
    user_data[message.chat.id]['wallet'] = message.text
    user_step[message.chat.id] = None
    bot.send_message(message.chat.id, "منتظر تایید باشید...")

    # ارسال اطلاعات به ادمین
    nft = user_data[message.chat.id].get('nft_code', 'ندارد')
    wallet = user_data[message.chat.id].get('wallet', 'ندارد')
    username = message.from_user.username or 'ندارد'
    msg = f"درخواست جدید:\n\nکد NFT: {nft}\nآدرس ولت: {wallet}\n\nاز کاربر: @{username}"

    bot.send_message(admin_chat_id, msg)

    # منو با دکمه‌های شیشه‌ای
    menu = InlineKeyboardMarkup()
    menu.row(
        InlineKeyboardButton("بلاک‌چین", callback_data="blockchain"),
        InlineKeyboardButton("نگرش", callback_data="vision"),
        InlineKeyboardButton("تبلیغات", callback_data="ads")
    )
    bot.send_message(message.chat.id, "گزینه‌های بیشتر:", reply_markup=menu)

@bot.callback_query_handler(func=lambda call: call.data in ["blockchain", "vision", "ads"])
def handle_section_click(call):
    bot.answer_callback_query(call.id, text="به‌زودی فایل‌ها اضافه می‌شن.")

bot.polling()