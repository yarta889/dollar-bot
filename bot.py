import telebot
from telebot import types
import requests

# توکن ربات شما
BOT_TOKEN = "8947126303:AAEzNel3F6eZZZISHmrGeqjfpZijBxjJV1o"
bot = telebot.TeleBot(BOT_TOKEN)

def main_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_dollar = types.KeyboardButton('💵 قیمت دلار و تتر')
    btn_crypto = types.KeyboardButton('🪙 ارز دیجیتال')
    btn_gold = types.KeyboardButton('🥇 طلا و سکه')
    btn_help = types.KeyboardButton('ℹ️ راهنما')
    markup.add(btn_dollar, btn_crypto, btn_gold, btn_help)
    return markup

def inline_refresh_markup():
    markup = types.InlineKeyboardMarkup()
    btn_refresh = types.InlineKeyboardButton(text="🔄 بروزرسانی قیمت", callback_data="refresh_dollar")
    markup.add(btn_refresh)
    return markup

def get_dollar_price():
    try:
        res = requests.get("https://api.nobitex.ir/market/stats", timeout=5).json()
        latest = int(res['stats']['usdt-irt']['latest']) // 10
        high = int(res['stats']['usdt-irt']['dayHigh']) // 10
        low = int(res['stats']['usdt-irt']['dayLow']) // 10
        
        return (
            f"💵 **قیمت لحظه‌ای دلار (تتر):**\n\n"
            f"🔹 قیمت فعلی: **{latest:,} تومان**\n"
            f"📈 بیشترین امروز: {high:,} تومان\n"
            f"📉 کمترین امروز: {low:,} تومان"
        )
    except:
        return "⚠️ دریافت قیمت با خطا مواجه شد."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "👋 سلام! به ربات نرخ لحظه‌ای خوش آمدید.\nبرای دریافت قیمت‌ها از دکمه‌های زیر استفاده کنید:",
        reply_markup=main_keyboard()
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "refresh_dollar":
        price_text = get_dollar_price()
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=price_text,
            reply_markup=inline_refresh_markup(),
            parse_mode="Markdown"
        )
        bot.answer_callback_query(call.id, text="قیمت بروز شد ✅")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text

    if text in ['💵 قیمت دلار و تتر', 'دلار', 'تتر']:
        bot.reply_to(message, get_dollar_price(), reply_markup=inline_refresh_markup(), parse_mode="Markdown")

    elif text in ['🪙 ارز دیجیتال', 'بیت کوین', 'بیتکوین']:
        try:
            res = requests.get("https://api.nobitex.ir/market/stats", timeout=5).json()
            btc = int(res['stats']['btc-irt']['latest']) // 10
            eth = int(res['stats']['eth-irt']['latest']) // 10
            resp = (
                f"🪙 **نرخ لحظه‌ای رمزارزها:**\n\n"
                f"🟠 **بیت‌کوین:** {btc:,} تومان\n"
                f"🔷 **اتریوم:** {eth:,} تومان"
            )
            bot.reply_to(message, resp, parse_mode="Markdown")
        except:
            bot.reply_to(message, "⚠️ خطایی در استعلام قیمت رمزارزها رخ داد.")

    elif text in ['🥇 طلا و سکه', 'طلا', 'سکه']:
        bot.reply_to(message, "🥇 جهت دریافت نرخ دقیق طلا و سکه، در ساعات کاری بازار مجدد استعلام بگیرید.")

    elif text == 'ℹ️ راهنما':
        bot.reply_to(message, "🔹 این ربات را به گروه‌ها اضافه کنید؛ با فرستادن کلمه «دلار» نرخ لحظه‌ای ارسال می‌شود.")

bot.infinity_polling()
