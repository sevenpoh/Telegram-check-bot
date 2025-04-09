
from playwright.sync_api import sync_playwright

def install_browser():
    with sync_playwright() as p:
        p.chromium.launch()
