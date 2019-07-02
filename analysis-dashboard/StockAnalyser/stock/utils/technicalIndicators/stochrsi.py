"""
    Calculates the Fast Stochastic Oscillator of the RSI values
"""
from stock.utils.technicalIndicators.base_indicator import Indicator


class STOCHRSI(Indicator):
    # https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/stochrsi
    # StochRSI = [(Current RSI – Lowest Low RSI Value in n periods) / (Highest High RSI Value in n periods – Lowest Low RSI Value in n periods)] x 100

    _name = "stochrsi"

    def calculate(self):
        for period in self.config["periods"]:
            rsi_column_name = "rsi_close_14"
            if rsi_column_name not in self.data:
                rsi_obj = self.ticker.get_indicator(indicator_name="rsi", indicator_config={"periods" : [14], "action" : "Close"})
                rsi_obj.calculate()
            rolling_window = self.data[rsi_column_name].rolling(min_periods=1, window=period)
            lowest_rsi = rolling_window.min()
            highest_rsi = rolling_window.max()
            column_name = f"stochrsi_{self.config['action'].lower()}_{period}"
            self.data[column_name] = (self.data[rsi_column_name] - lowest_rsi)*100/(highest_rsi - lowest_rsi)


# if __name__ == '__main__':
#     from ticker import Ticker
#     STOCK_DATA_API_URL = "http://192.168.15.70:8000/finValues?company={}&start={}"
#     DATA_START_DATE_LIMIT = "03-01-2017"
#     tick = Ticker("FB", DATA_START_DATE_LIMIT, STOCK_DATA_API_URL, fields=["High", "Low", "Open", "Close", "Volume"])
#     config = {"periods" : [14], "action" : "RSI"}
#
#     stochrsi = STOCHRSI(config=config, ticker_obj=tick)
#     stochrsi.calculate()
#     print(stochrsi.data.tail())
