from dataclasses import dataclass
from datetime import datetime


@dataclass
class Price:

    platform: str
    city: str
    product: str
    price: float
    unit: str
    scraped_at: datetime