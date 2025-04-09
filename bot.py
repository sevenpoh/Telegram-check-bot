
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext
import asyncio

TOKEN = "7977593128:AAHzwfhgfKxc-FOZv04zoMcmeBBNoJG-f7A"

async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Comprar", callback_data='comprar')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Olá! Seja bem-vindo ao bot de checagem!", reply_markup=reply_markup)

if __name__ == '__main__':
    from playwright_install import install_browser
    install_browser()

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
