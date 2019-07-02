"""
    Calculate the Relative Strength Index
    # https://en.wikipedia.org/wiki/Relative_strength_index
"""

from stock.utils.technicalIndicators.base_indicator import Indicator


class RSI(Indicator):
    _name = "rsi"

    def calculate(self):
        self.data["changes"] = self.data[self.config["action"]] - self.data[self.config["action"]].shift()
        self.data["up_moves"] = [x if x > 0 else 0 for x in self.data["changes"]]
        self.data["down_moves"] = [-x if x < 0 else 0 for x in self.data["changes"]]
        for period in self.config["periods"]:
            self.data["avg_up"] = self.data["up_moves"].ewm(alpha=1 / period, adjust=True).mean()
            self.data["avg_down"] = self.data["down_moves"].ewm(alpha=1 / period, adjust=True).mean()
            self.data["RS"] = self.data["avg_up"] / self.data["avg_down"]
            column_name = f"rsi_{self.config['action'].lower()}_{period}"
            self.data[column_name] = 100.0 - 100.0 / (1 + self.data["RS"])
            del self.data["avg_up"]
            del self.data["avg_down"]
            del self.data["RS"]
        del self.data["changes"]
        del self.data["up_moves"]
        del self.data["down_moves"]

#
# if __name__ == '__main__':
#     from ticker import Ticker
#     STOCK_DATA_API_URL = "http://192.168.15.70:8000/finValues?company={}&start={}"
#     DATA_START_DATE_LIMIT = "03-01-2017"
#     tick = Ticker("FB", DATA_START_DATE_LIMIT, STOCK_DATA_API_URL, fields=["High", "Low", "Open", "Close", "Volume"])
#     config = {"periods" : [14], "action" : "Close"}
#
#     rsi = RSI(config=config, ticker_obj=tick)
#     rsi.calculate()
#     print(rsi.data.tail())
