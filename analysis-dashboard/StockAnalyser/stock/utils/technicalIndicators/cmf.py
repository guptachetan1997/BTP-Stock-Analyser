"""
    Calculate the Chaikin Money Flow
    #https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/cmf
"""

from stock.utils.technicalIndicators.base_indicator import Indicator


class CMF(Indicator):
    _name = "cmf"

    def calculate(self):
        for period in self.config["periods"]:
            numerator = (((self.data["Close"] - self.data["Low"]) - (self.data["High"] - self.data["Close"])) * (
                    self.data["Volume"] / (self.data["High"] - self.data["Low"]))).rolling(min_periods=1, window=period).sum()
            denominator = self.data["Volume"].rolling(window=period, min_periods=1).sum()
            column_name = f"cmf_{self.config['action'].lower()}_{period}"
            self.data[column_name] = numerator/denominator
            del numerator, denominator


# if __name__ == '__main__':
#     from ticker import Ticker
#
#     STOCK_DATA_API_URL = "http://192.168.15.70:8000/finValues?company={}&start={}"
#     DATA_START_DATE_LIMIT = "03-01-2017"
#     tick = Ticker("FB", DATA_START_DATE_LIMIT, STOCK_DATA_API_URL, fields=["High", "Low", "Open", "Close", "Volume"])
#
#     config = {"action" : "CloseVolume", "periods" : [21]}
#     cmf = CMF(config=config, ticker_obj=tick)
#     cmf.calculate()
#     print(cmf.data.tail())
