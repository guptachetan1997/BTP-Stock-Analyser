"""
    Calculates the TRIX i.e 1% change in Triple Smoothed Exponential Moving Average
"""

from stock.utils.technicalIndicators.base_indicator import Indicator


class TRIX(Indicator):
    _name = "trix"

    def calculate(self):
        for period in self.config["periods"]:
            if period > 0:
                single_ema = f"ema_{self.config['action'].lower()}_{period}"
                double_ema = f"ema_{single_ema}_{period}"
                triple_ema = f"ema_{double_ema}_{period}"
                if single_ema not in self.data:
                    ema_1 = self.ticker.get_indicator(indicator_name="ema", indicator_config={"periods" : [period], "action" : self.config["action"]})
                    ema_1.calculate()
                ema_2 = self.ticker.get_indicator(indicator_name="ema", indicator_config={"periods" : [period], "action" : single_ema})
                ema_2.calculate()
                ema_3 = self.ticker.get_indicator(indicator_name="ema", indicator_config={"periods" : [period], "action" : double_ema})
                ema_3.calculate()
                column_name = f"trix_{self.config['action'].lower()}_{period}"
                shifts = self.data[triple_ema].shift()
                self.data[column_name] = ((self.data[triple_ema] - shifts)*100)/shifts
                del self.data[double_ema]
                del self.data[triple_ema]


# if __name__ == '__main__':
#     from ticker import Ticker
#     STOCK_DATA_API_URL = "http://192.168.15.70:8000/finValues?company={}&start={}"
#     DATA_START_DATE_LIMIT = "03-01-2017"
#     tick = Ticker("FB", DATA_START_DATE_LIMIT, STOCK_DATA_API_URL, fields=["High", "Low", "Open", "Close", "Volume"])
#     config = {"periods": [14], "action": "Close"}
#
#     trix = TRIX(config=config, ticker_obj=tick)
#     trix.calculate()
#     print(trix.data.tail())