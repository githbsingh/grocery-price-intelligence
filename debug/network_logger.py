from playwright.sync_api import sync_playwright


import json
import os

os.makedirs("responses", exist_ok=True)

counter = 0

from urllib.parse import urlparse

def handle_response(response):
    try:
        if "listing-svc/v2/products" in response.url:

            print("=" * 100)
            print("URL:", response.url)

            print("\nSTATUS:", response.status)

            data = response.json()

            print("\nTOP LEVEL KEYS:")
            print(data.keys())

            import json

            with open("products_response.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            print("\nSaved to products_response.json")

    except Exception as e:
        print(e)

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False,
        slow_mo=300
    )

    page = browser.new_page()

    page.on("response", handle_response)

    page.goto(
        "https://www.bigbasket.com/",
        wait_until="networkidle"
    )

    print("\nSearch for Tomato manually...")
    input("Press ENTER after searching...")
    cookies = page.context.cookies()

    print("=" * 100)
    print("COOKIES")
    
    for cookie in cookies:
        print(cookie["name"], "=", cookie["value"])
    browser.close()