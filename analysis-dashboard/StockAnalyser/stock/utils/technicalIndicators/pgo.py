"""
    Calculate the Pretty Good Oscillator
"""
from stock.utils.technicalIndicators.base_indicator import Indicator


class PGO(Indicator):
    _name = "pgo"

    def calculate(self):
        for period in self.config["periods"]:
            sma_close = f"sma_close_{period}"
            atr_close = f"atr_close_{period}"
            if sma_close not in self.data:
                sma_close_obj = self.ticker.get_indicator(indicator_name="sma", indicator_config={"periods" : [period], "action" : "Close"})
                sma_close_obj.calculate()
            if atr_close not in self.data:
                atr_close_obj = self.ticker.get_indicator(indicator_name="atr", indicator_config={"periods" : [period], "action" : "Close"})
                atr_close_obj.calculate()

            column_name = f"pgo_{self.config['action'].lower()}_{period}"
            self.data[column_name] = (self.data["Close"] - self.data[sma_close])/self.data[atr_close]


# if __name__ == '__main__':
#     from ticker import Ticker
#     STOCK_DATA_API_URL = "http://192.168.15.70:8000/finValues?company={}&start={}"
#     DATA_START_DATE_LIMIT = "03-01-2017"
#     tick = Ticker("FB", DATA_START_DATE_LIMIT, STOCK_DATA_API_URL, fields=["High", "Low", "Open", "Close", "Volume"])
#
#     config = {"periods" : [14], "action" : "Close"}
#
#     pgo = PGO(config=config, ticker_obj=tick)
#     pgo.calculate()
#     print(pgo.data.tail())