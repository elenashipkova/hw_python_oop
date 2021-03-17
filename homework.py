import datetime as dt
from typing import List, Union


class Record:
    def __init__(self, amount, comment, date=None) -> None:
        self.amount = amount
        self.comment = comment
        if date is not None:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        else:
            self.date = dt.date.today()

    def show_record(self):
        return f'{self.amount}, {self.date}, {self.comment}'


class Calculator:
    def __init__(self, limit: float) -> None:
        self.limit = limit
        self.records: List[Union[str, float, dt.date]] = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        current_mom = dt.date.today()
        current_mom_amount = 0
        for record in self.records:
            if record.date == current_mom:
                current_mom_amount += record.amount
        return current_mom_amount

    def get_today_remained(self):
        remained = round((self.limit - self.get_today_stats()), 2)
        return remained

    def get_week_stats(self):
        current_mom = dt.date.today()
        last_week = current_mom - dt.timedelta(days=6)
        last_week_amount = 0
        for record in self.records:
            if last_week <= record.date <= current_mom:
                last_week_amount += record.amount
        return last_week_amount


class CaloriesCalculator(Calculator):
    def __init__(self, limit: float) -> None:
        super().__init__(limit)

    def get_calories_remained(self):
        cal_remained = self.get_today_remained()
        if cal_remained > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {cal_remained} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1.0

    def __init__(self, limit: float) -> None:
        super().__init__(limit)

    def get_today_cash_remained(self, currency):
        currencies = {
            'usd': CashCalculator.USD_RATE,
            'eur': CashCalculator.EURO_RATE,
            'rub': CashCalculator.RUB_RATE,
        }
        cash_remained = self.get_today_remained()
        currency_type = currencies[currency]
        currency_remained = round(cash_remained / currency_type, 2)
        curr_print = {
            'usd': 'USD',
            'eur': 'Euro',
            'rub': 'руб',
        }
        if cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained > 0:
            return (f'На сегодня осталось '
                    f'{currency_remained} {curr_print[currency]}')
        else:
            return (f'Денег нет, держись: твой долг - '
                    f'{abs(currency_remained)} {curr_print[currency]}')

cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=1000, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='сосиска'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=400,
                                  comment='обед',
                                  date='08.11.2019'))

print(cash_calculator.get_today_cash_remained('eur'))
