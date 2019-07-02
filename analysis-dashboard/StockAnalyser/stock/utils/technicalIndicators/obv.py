"""
    Calculate the On Balance Volume
"""

from stock.utils.technicalIndicators.base_indicator import Indicator


class OBV(Indicator):
    _name = "obv"

    def calculate(self):
        for period in self.config["periods"]:
            self.data["close_price_changes"] = self.data["Close"] - self.data["Close"].shift()
            obv = []
            for change,volume in zip(self.data["close_price_changes"], self.data["Volume"]):
                if change > 0:
                   obv.append(obv[-1] + volume)
                elif change == 0:
                    obv.append(obv[-1])
                elif change < 0:
                    obv.append(obv[-1] - volume)
                else:
                    obv.append(volume)
            column_name = f"obv_{self.config['action'].lower()}_{period}"
            self.data[column_name] = obv
            del self.data["close_price_changes"]


# if __name__ == '__main__':
#     from ticker import Ticker
#     STOCK_DATA_API_URL = "http://192.168.15.70:8000/finValues?company={}&start={}"
#     DATA_START_DATE_LIMIT = "03-01-2017"
#     tick = Ticker("FB", DATA_START_DATE_LIMIT, STOCK_DATA_API_URL, fields=["High", "Low", "Open", "Close", "Volume"])
#     config = {"action" : "CloseVolume", "periods" : [1]}
#
#     obv = OBV(config=config, ticker_obj=tick)
#     obv.calculate()
#     print(obv.data.tail())
