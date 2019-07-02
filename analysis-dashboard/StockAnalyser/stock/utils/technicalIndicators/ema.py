"""
    Compute the n day Exponential Moving Average
"""

from stock.utils.technicalIndicators.base_indicator import Indicator


class EMA(Indicator):
    _name = "ema"

    def calculate(self):
        for period in self.config["periods"]:
            if period > 0:
                column_name = f"ema_{self.config['action'].lower()}_{period}"
                # Over here adjust=False calculates the EMA recursively otherwise it calculates using constant weight
                # ref : https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.ewm.html
                calculated = self.data[self.config["action"]].ewm(span=period, adjust=False).mean()
                self.data[column_name] = calculated


# if __name__ == '__main__':
#     from ticker import Ticker
#
#     STOCK_DATA_API_URL = "http://192.168.15.70:8000/finValues?company={}&start={}"
#     DATA_START_DATE_LIMIT = "03-01-2017"
#     tick = Ticker("FB", DATA_START_DATE_LIMIT, STOCK_DATA_API_URL, fields=["High", "Low", "Open", "Close", "Volume"])
#     config = {"periods" : [12, 26], "action" : "Close"}
#     ema = EMA(config=config, ticker_obj=tick)
#     ema.calculate()
#     print(ema.data.tail())