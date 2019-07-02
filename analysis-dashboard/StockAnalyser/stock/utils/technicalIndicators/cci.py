"""
    Calculates the commodity channel index for n periods.
"""

import numpy as np
from stock.utils.technicalIndicators.base_indicator import Indicator


class CCI(Indicator):
    _name = "cci"
    CONSTANT = 0.015

    def calculate(self):
        for period in self.config["periods"]:
            self.data["tp"] = (self.data["Close"] + self.data["High"] + self.data["Low"])/3
            sma_obj = self.ticker.get_indicator(indicator_name="sma", indicator_config={"periods" : [period], "action" : "tp"})
            sma_obj.calculate()
            mean_deviation = self.data["tp"].rolling(window=period, min_periods=1).apply(lambda x : np.fabs(x - x.mean()).mean())
            column_name = f"cci_{self.config['action'].lower()}_{period}"
            self.data[column_name] = (self.data["tp"] - self.data["sma_tp_{}".format(period)])/(self.CONSTANT * mean_deviation)
            self.data[column_name][0] = self.data[column_name][1]
            del self.data["tp"], self.data[f"sma_tp_{period}"]


# if __name__ == '__main__':
#     from ticker import Ticker
#
#     STOCK_DATA_API_URL = "http://192.168.15.70:8000/finValues?company={}&start={}"
#     DATA_START_DATE_LIMIT = "03-01-2017"
#     tick = Ticker("FB", DATA_START_DATE_LIMIT, STOCK_DATA_API_URL, fields=["High", "Low", "Open", "Close", "Volume"])
#     config = {"periods": [20], "action" : "TP"}
#
#     cci = CCI(config=config, ticker_obj=tick)
#     cci.calculate()
#     print(cci.data.tail())
