from fastapi import FastAPI
import asyncio
from playwright.async_api import async_playwright

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "online"}

@app.get("/check")
async def check_card():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto("https://example.com")
            await browser.close()
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}