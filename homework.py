"""Money and Calorie Calculator."""
import datetime as dt
from typing import List, Tuple, Dict, Optional

DATE_FORMAT = '%d.%m.%Y'


class Record:
    """Class Record to define the format of user spending records."""

    def __init__(self,
                 amount: int,
                 comment: str,
                 date: Optional[str] = None) -> None:
        """Set the required attributes for the record object.

        Attributes:
        amount (int): amount of spend money or calories consumed
        comment (str): user's text about the amounts
        date (Optional[str]): if date is None, assign default value -
        current date"""
        self.amount = amount
        self.comment = comment
        if date is not None:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()
        else:
            self.date = dt.date.today()


class Calculator:
    """Class Calculator - application for calculating expences and calories."""

    def __init__(self, limit: int) -> None:
        """Set the required attributes for the calculator object.

        Attributes:
        limit (int): the amount of daily spending/calorie limit set by the user
        records (List[Record]): list for storing records of expenses amounts
        or calories
        today (dt.date.today()): current date
        """
        self.limit = limit
        self.records: List[Record] = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self) -> int:
        """Calculate expences/calories for today."""
        return sum(record.amount for record in self.records
                   if record.date == dt.date.today())

    def get_today_remained(self) -> float:
        """Calculate the available cash/calorie limit."""
        remained = self.limit - self.get_today_stats()
        return remained

    def get_week_stats(self) -> int:
        """Calculate the amount of money spent/calories for the week."""
        week_ago = dt.date.today() - dt.timedelta(days=7)
        return sum(record.amount for record in self.records
                   if week_ago < record.date <= dt.date.today())


class CaloriesCalculator(Calculator):
    """Class CaloriesCalculator calculate amount of the calories consumed
    and remained based on the limit."""

    def get_calories_remained(self) -> str:
        """Return message about the calorie limit status."""
        cal_remained = self.get_today_remained()
        if cal_remained > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {cal_remained} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    """Class CashCalculator calculate cash expenses and the remaining
    avialable limit in the supported currency.
    Contain currency exchange rate constants."""
    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency: str) -> str:
        """Return message about the status of the daily balance
        in the supported currency.

        Parameters:
        currency (str): one of the strings - 'usd', 'eur', 'rub'."""
        currencies: Dict[str, Tuple[float, str]] = {
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro'),
            'rub': (self.RUB_RATE, 'руб'),
        }
        currency_remained = self.get_today_remained()
        if currency_remained == 0:
            return 'Денег нет, держись'
        if currency not in currencies:
            return f'Неподдерживаемый тип валюты {currency}'
        rate, name = currencies[currency]
        currency_remained = round(currency_remained / rate, 2)
        if currency_remained < 0:
            debt = abs(currency_remained)
            return f'Денег нет, держись: твой долг - {debt} {name}'
        return f'На сегодня осталось {currency_remained} {name}'
