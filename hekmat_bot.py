import requests
import re
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# لیست آدرس‌های منابع حکمت
HIKMAT_URLS = [
    "https://tehranloh.ir/%D8%AD%DA%A9%D9%85%D8%AA+%D9%87%D8%A7%DB%8C+%D9%86%D9%87%D8%AC+%D8%A7%D9%84%D8%A8%D9%84%D8%A7%D8%BA%D9%87",
    "https://tehranloh.ir/%d8%b4%d8%b1%d8%ad-%d8%ad%da%a9%d9%85%d8%aa-%d9%87%d8%a7%db%8c-%d9%86%d9%87%d8%ac-%d8%a7%d9%84%d8%a8%d9%84%d8%a7%d8%ba%d9%87/",
    "https://tehranloh.ir/%d8%ad%da%a9%d9%85%d8%aa-%d9%87%d8%a7%db%8c-%d9%86%d9%87%d8%ac-%d8%a7%d9%84%d8%a8%d9%84%d8%a7%d8%ba%d9%87-%d8%a8%d8%a7-%d8%aa%d8%b1%d8%ac%d9%85%d9%87-%d9%81%d8%a7%d8%b1%d8%b3%db%8c/"
]

def get_all_hikmats_from_html(url):
    response = requests.get(url)
    html = response.text
    matches = re.findall(
        r'<strong>(.*?)</strong>\s*</span></p>\s*<p>(.*?)</p>\s*<p><span[^>]+>(.*?)</span>',
        html, re.DOTALL
    )
    hikmat_list = []
    for title, arabic, persian in matches:
        hikmat_list.append({
            "title": title.strip(),
            "arabic": arabic.strip(),
            "persian": persian.strip(),
        })
    return hikmat_list

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 ربات حکمت‌های نهج‌البلاغه\n\n"
        "هر روز یا هر لحظه یک حکمت تصادفی از نهج البلاغه را به شما نمایش می‌دهد.\n\n"
        "توسعه‌دهنده: متین تلخابی (Matin)\n"
        "• گیت‌هاب: https://github.com/Matin-Talkhabi\n"
        "• ارتباط در صورت مشکل: @KMmatin_00\n\n"
        "دستورات:\n"
        "• /random — دریافت حکمت تصادفی\n"
        "• /start — نمایش همین بخش معرفی و منو\n"
        "\nاین بات منبع حکمت‌ها را از سایت تهران‌لوح دریافت می‌کند و همیشه به‌روز است."
    )
    keyboard = [
        [InlineKeyboardButton("🎲 حکمت تصادفی", callback_data="random_hikmat")],
        [InlineKeyboardButton("⁉️ راهنما", callback_data="help")],
        [InlineKeyboardButton("📄 گیت‌هاب من", url="https://github.com/Matin-Talkhabi")],
        [InlineKeyboardButton("🗨 ارتباط با سازنده", url="https://t.me/KMmatin_00")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "random_hikmat":
        url = random.choice(HIKMAT_URLS)
        hikmat_list = get_all_hikmats_from_html(url)
        chosen = random.choice(hikmat_list)
        msg = f"عنوان:\n{chosen['title']}\n\nعربی:\n{chosen['arabic']}\n\nفارسی:\n{chosen['persian']}"
        await query.edit_message_text(text=msg)
    elif query.data == "help":
        help_msg = (
            "📌 راهنمای ربات:\n"
            "• هر وقت خواستید حکمت تصادفی/روزانه دریافت کنید، کافیست دکمه ‘حکمت تصادفی’ یا دستور /random را بزنید.\n"
            "• تمامی محتوا از سایت tehranloh.ir خوانده می‌شود و هیچ‌گونه دخیره‌سازی دائمی هم انجام نمی‌شود.\n"
            "• توسعه‌دهنده: متین تلخابی — ارتباط: @KMmatin_00"
        )
        await query.edit_message_text(text=help_msg)

async def random_hikmat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = random.choice(HIKMAT_URLS)
    hikmat_list = get_all_hikmats_from_html(url)
    chosen = random.choice(hikmat_list)
    msg = f"عنوان:\n{chosen['title']}\n\nعربی:\n{chosen['arabic']}\n\nفارسی:\n{chosen['persian']}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

if __name__ == '__main__':
    input_token_bot = input("Enter your bot token: ")
    token = input_token_bot.strip()
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("random", random_hikmat))
    from telegram.ext import CallbackQueryHandler
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot is running ...")
    app.run_polling()
