from abc import ABC, abstractmethod


class BaseScraper(ABC):

    @abstractmethod
    def fetch_prices(self, city: str, product: str):
        pass