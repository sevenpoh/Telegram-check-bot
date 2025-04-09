from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"Olá {user.first_name}, bem-vindo ao bot!")

if __name__ == '__main__':
    app = ApplicationBuilder().token("7977593128:AAHzwfhgfKxc-FOZv04zoMcmeBBNoJG-f7A").build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()