# scrapers/bigbasket_scraper.py

import time
import random
import requests
from typing import List, Dict

from utils.session_manager import SessionManager


class BigBasketScraper:

    BASE_URL = "https://www.bigbasket.com"

    PRODUCT_API = (
        "https://www.bigbasket.com/listing-svc/v2/products"
    )

    def __init__(self):

        from utils.session_manager import SessionManager

        self.session = SessionManager().get_session()
        print(self.session.cookies.get_dict())

        self.session.headers.update(
            {
                "accept": "application/json",
                "accept-language": "en-IN,en;q=0.9",
                "referer": "https://www.bigbasket.com/",
                "origin": "https://www.bigbasket.com",
                "user-agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                    " AppleWebKit/537.36 (KHTML, like Gecko)"
                    " Chrome/138.0 Safari/537.36",
            }
        )

    ####################################################################

    def fetch_prices(
        self,
        product: str,
        page: int = 1,
        bucket_id: int = 61,
    ) -> List[Dict]:

        params = {
            "type": "ps",
            "slug": product.lower().replace(" ", "-"),
            "page": page,
            "bucket_id": bucket_id,
        }
        print(self.session.cookies.get_dict())
        response = self.session.get(
            self.PRODUCT_API,
            params=params,
            timeout=30,
        )

        #response.raise_for_status()
        print("=" * 100)
        print(response.status_code)
        print(response.url)
        print(response.text)
        print("=" * 100)

        data = response.json()

        return self.parse_products(data)

    ####################################################################

    def parse_products(self, data):


        products = []

        tabs = data.get("tabs", [])

        for tab in tabs:

            product_info = tab.get("product_info", {})

            for p in product_info.get("products", []):

                discount = (
                    p.get("pricing", {})
                     .get("discount", {})
                )

                prim_price = discount.get("prim_price", {})

                products.append({

                    "id": p.get("id"),

                    "name": p.get("desc"),

                    "brand": p.get("brand", {}).get("name"),

                    "weight": p.get("w"),

                    "price": float(prim_price.get("sp", 0)),

                    "mrp": float(discount.get("mrp", 0)),

                    "discount": discount.get("d_text"),

                    "availability": p.get("availability", {}).get("button"),

                    "url": "https://www.bigbasket.com" + p.get("absolute_url", ""),

                    "image": p.get("images", [{}])[0].get("l")
                })

        return products