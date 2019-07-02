"""
    Calculates the Average True Range
"""

from stock.utils.technicalIndicators.base_indicator import Indicator


class ATR(Indicator):
    _name = "atr"

    def calculate(self):
        for period in self.config["periods"]:
            yesterday_close = self.data["Close"].shift()
            self.data["high_minus_low"] = self.data["High"] - self.data["Low"]
            self.data["high_minus_yesterday_close"] = (self.data["High"] - yesterday_close).abs()
            self.data["today_low_minus_yesterday_close"] = (self.data["Low"] - yesterday_close).abs()
            self.data["TR"] = self.data.loc[:, ['high_minus_low', 'high_minus_yesterday_close', 'today_low_minus_yesterday_close']].max(axis=1)
            column_name = f"atr_{self.config['action'].lower()}_{period}"
            self.data[column_name] = self.data["TR"].ewm(alpha=1 / period, adjust=True).mean()

            del self.data["high_minus_low"]
            del self.data["high_minus_yesterday_close"]
            del self.data["today_low_minus_yesterday_close"]
            del self.data["TR"]


# if __name__ == '__main__':
#     from ticker import Ticker
#
#     STOCK_DATA_API_URL = "http://192.168.15.70:8000/finValues?company={}&start={}"
#     DATA_START_DATE_LIMIT = "03-01-2017"
#     tick = Ticker("FB", DATA_START_DATE_LIMIT, STOCK_DATA_API_URL, fields=["High", "Low", "Open", "Close", "Volume"])
#     config = {"periods" : [14], "action" : "Close"}
#
#     atr = ATR(config=config, ticker_obj=tick)
#     atr.calculate()
#     print(atr.data.head())
