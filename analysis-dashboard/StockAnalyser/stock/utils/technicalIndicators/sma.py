"""
    Compute the n day Simple Moving Average
"""

from stock.utils.technicalIndicators.base_indicator import Indicator


class SMA(Indicator):
    _name = "sma"

    def calculate(self):
        for period in self.config["periods"]:
            if period > 0:
                column_name = f"sma_{self.config['action'].lower()}_{period}"
                calculated = self.data[self.config["action"]].rolling(window=period).mean()
                self.data[column_name] = calculated
                self.data[column_name] = self.data[column_name].fillna(0)


# if __name__ == '__main__':
#     from ticker import Ticker
#     STOCK_DATA_API_URL = "http://192.168.15.70:8000/finValues?company={}&start={}"
#     DATA_START_DATE_LIMIT = "03-01-2017"
#     tick = Ticker("FB", DATA_START_DATE_LIMIT, STOCK_DATA_API_URL, fields=["High", "Low", "Open", "Close", "Volume"])
#     config = {"periods" : [5, 7], "action" : "Close"}
#
#     sma = SMA(config=config, ticker_obj=tick)
#     sma.calculate()
#     print(sma.data.tail())
