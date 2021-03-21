"""Money and Calorie Calculator."""

import datetime as dt
from typing import List

date_format = '%d.%m.%Y'


class Record:
    """Class Record to define the format of user spending records."""

    def __init__(self, amount: int, comment: str, date=None) -> None:
        """Set the required attributes for the record object.

        Attributes:
        amount (int): amount of spend money or calories consumed
        comment (str): user's text about the amounts
        date (None): if date is None, assign default value - current date
        """

        self.amount = amount
        self.comment = comment
        if date is not None:
            self.date = dt.datetime.strptime(date, date_format).date()
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
        self.today = dt.date.today()

    def add_record(self, record):
        """Method add_record() to add record to the list records."""

        self.records.append(record)

    def get_today_stats(self) -> int:
        """Method get_today_stats() calculates expences/calories for today."""

        today_stats = []
        for record in self.records:
            if record.date == self.today:
                today_stats.append(record.amount)
        return sum(today_stats)

    def get_today_remained(self) -> float:
        """Method get_today_remained() calculates the available
        cash/calorie limit."""

        remained = self.limit - self.get_today_stats()
        return remained

    def get_week_stats(self) -> int:
        """Method get_week_stats() calculates the amount of
        money spent/calories for the week."""

        week_ago = self.today - dt.timedelta(days=7)
        week_stats = []
        for record in self.records:
            if week_ago < record.date <= self.today:
                week_stats.append(record.amount)
        return sum(week_stats)


class CaloriesCalculator(Calculator):
    """Class CaloriesCalculator extended class Calculator."""

    def get_calories_remained(self) -> str:
        """Method get_calories_remained() applied metod get_today_remained()
        This method returns message about the calorie limit status."""

        cal_remained = self.get_today_remained()
        if cal_remained > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {cal_remained} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    """Class CashCalculator extended class Calculator.
    Added currency exchange rate constants"""

    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency: str) -> str:
        """Method get_today_cash_remained(currency)
        applied method get_today_remained().

        Parameters:
        currency (str): one of the strings - 'usd', 'eur', 'rub'
        
        This method returns message about the status of the daily balance
        in the supported currency."""

        currencies = {
            'usd': (CashCalculator.USD_RATE, 'USD'),
            'eur': (CashCalculator.EURO_RATE, 'Euro'),
            'rub': (CashCalculator.RUB_RATE, 'руб'),
        }
        cash_remained = self.get_today_remained()
        if cash_remained == 0:
            return 'Денег нет, держись'
        if currency not in currencies:
            return f'Неподдерживаемый тип валюты {currency}'
        rate, name = currencies[currency]
        currency_remained = round(cash_remained / rate, 2)
        if cash_remained > 0:
            return f'На сегодня осталось {currency_remained} {name}'
        else:
            cash_remained = abs(currency_remained)
            return ('Денег нет, держись: твой долг - '
                    f'{cash_remained} {name}')
