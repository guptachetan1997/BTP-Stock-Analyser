"""
    Calculates the Williams' %R
"""

from stock.utils.technicalIndicators.base_indicator import Indicator


class WR(Indicator):
    _name = "wr"

    def calculate(self):
        for period in self.config["periods"]:
            lowest_lows = self.data["Low"].rolling(min_periods=1, window=period).min()
            highest_highs = self.data["High"].rolling(min_periods=1, window=period).max()
            column_name = f"wr_{self.config['action'].lower()}_{period}"
            self.data[column_name] = ((highest_highs - self.data["Close"])*(-100))/(highest_highs - lowest_lows)


# if __name__ == '__main__':
#     from ticker import Ticker
#     STOCK_DATA_API_URL = "http://192.168.15.70:8000/finValues?company={}&start={}"
#     DATA_START_DATE_LIMIT = "03-01-2017"
#     tick = Ticker("FB", DATA_START_DATE_LIMIT, STOCK_DATA_API_URL, fields=["High", "Low", "Open", "Close", "Volume"])
#     config = {"periods" : [14], "action" : "Close"}
#
#     wr = WR(config=config, ticker_obj=tick)
#     wr.calculate()
#     print(wr.data.tail())
