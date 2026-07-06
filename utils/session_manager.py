from playwright.sync_api import sync_playwright
import requests


class SessionManager:

    def get_session(self):

        session = requests.Session()

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=False
            )

            context = browser.new_context()

            page = context.new_page()

            page.goto(
                "https://www.bigbasket.com/",
                wait_until="networkidle"
            )

            print("=" * 80)
            print("Select your city manually.")
            print("Search any product.")
            print("Then press ENTER here.")
            print("=" * 80)

            input()

            cookies = context.cookies()

            browser.close()

        for cookie in cookies:

            session.cookies.set(
                cookie["name"],
                cookie["value"]
            )

        session.headers.update(
            {
                "accept": "application/json",
                "referer": "https://www.bigbasket.com/",
                "origin": "https://www.bigbasket.com",
                "user-agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 Chrome/149 Safari/537.36",
                "x-channel": "BB-WEB",
                "x-entry-context": "bbnow",
                "x-entry-context-id": "10",
            }
        )

        return session