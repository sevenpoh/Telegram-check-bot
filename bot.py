from fastapi import FastAPI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import asyncio

app = FastAPI()
BOT_TOKEN = os.getenv("BOT_TOKEN", "7977593128:AAHzwfhgfKxc-FOZv04zoMcmeBBNoJG-f7A")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Olá {update.effective_user.first_name}, bem-vindo(a)!")

async def run_bot():
    app_builder = ApplicationBuilder().token(BOT_TOKEN).build()
    app_builder.add_handler(CommandHandler("start", start))
    await app_builder.initialize()
    await app_builder.start()
    await app_builder.updater.start_polling()

@app.on_event("startup")
async def on_startup():
    asyncio.create_task(run_bot())

@app.get("/")
def read_root():
    return {"status": "Bot online"}
