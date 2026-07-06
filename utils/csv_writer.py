import pandas as pd
import os


def save_prices(prices):

    rows = []

    for p in prices:

        rows.append(
            {
                "platform": p.platform,
                "city": p.city,
                "product": p.product,
                "price": p.price,
                "unit": p.unit,
                "scraped_at": p.scraped_at
            }
        )

    df = pd.DataFrame(rows)

    os.makedirs("data", exist_ok=True)

    file = "data/prices.csv"

    if os.path.exists(file):
        df.to_csv(file, mode="a", header=False, index=False)
    else:
        df.to_csv(file, index=False)