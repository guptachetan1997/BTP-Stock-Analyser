"""
    Calculate the Money Flow Index
"""
from stock.utils.technicalIndicators.base_indicator import Indicator


class MFI(Indicator):
    _name = "mfi"

    def calculate(self):
        self.data["TP"] = (self.data["High"] + self.data["Low"] + self.data["Close"]) / 3
        self.data["MoneyFlow"] = self.data["TP"] * self.data["Volume"]
        tp_changes = (self.data["TP"] - self.data["TP"].shift())
        self.data["PositiveFlow"] = [y if x > 0 else 0 for x, y in zip(tp_changes, self.data["MoneyFlow"])]
        self.data["NegativeFlow"] = [y if x < 0 else 0 for x, y in zip(tp_changes, self.data["MoneyFlow"])]
        for period in self.config["periods"]:
            self.data["MoneyRatio"] = self.data["PositiveFlow"].rolling(window=period).sum() / self.data[
                "NegativeFlow"].rolling(window=period).sum()
            column_name = f"mfi_{self.config['action'].lower()}_{period}"
            self.data[column_name] = 100 - (100/(1 + self.data["MoneyRatio"]))
            del self.data["MoneyRatio"]
        del self.data["TP"], self.data["MoneyFlow"], self.data["PositiveFlow"], self.data["NegativeFlow"]





if __name__ == '__main__':
    from ticker import Ticker
    STOCK_DATA_API_URL = "http://192.168.15.70:8000/finValues?company={}&start={}"
    DATA_START_DATE_LIMIT = "03-01-2017"
    tick = Ticker("FB", DATA_START_DATE_LIMIT, STOCK_DATA_API_URL, fields=["High", "Low", "Open", "Close", "Volume"])
    config = {"action" : "CloseVolume", "periods" : [15]}

    mfi = MFI(config=config, ticker_obj=tick)
    mfi.calculate()
    print(mfi.data.tail())
