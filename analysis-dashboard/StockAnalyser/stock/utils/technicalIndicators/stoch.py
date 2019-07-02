"""
    Calculates the Fast Stochastic Oscillator
"""

from stock.utils.technicalIndicators.base_indicator import Indicator


class STOCH(Indicator):
    # http: // stockcharts.com / school / doku.php?id = chart_school:technical_indicators: stochastic_oscillator_fast_slow_and_full
    # % K = (Current Close - Lowest Low) / (Highest High - Lowest Low) * 100
    # % D = 3 - day SMA of % K
    # Lowest Low = lowest low for the look - back period
    # Highest High = highest high for the look - back period
    # % K is multiplied by 100 to move the decimal point two places

    _name = "stoch"

    def calculate(self):
        for period in self.config["periods"]:
            lowest_lows = self.data["Low"].rolling(min_periods=1, window=period["k"]).min()
            highest_highs = self.data["High"].rolling(min_periods=1, window=period["k"]).max()
            column_name = f"stoch_{period['k']}"
            signal_column_name = f"signal_stoch_{period['k']}"
            self.data[column_name] = (self.data["Close"] - lowest_lows)*100/(highest_highs - lowest_lows)
            sma_obj = self.ticker.get_indicator(indicator_name="sma", indicator_config={"periods" : [period["d"]], "action" : column_name})
            sma_obj.calculate()
            self.data[signal_column_name] = self.data["sma_{}_{}".format(column_name, period["d"])]
            del self.data[f"sma_{column_name}_{period['d']}"]

    def get_json(self, after_date=None):
        working_data = self.data.round(3)
        if after_date:
            working_data = working_data[working_data["Date"] >= after_date]
        total_obj = []
        for _, row in working_data.iterrows():
            cur_obj = dict()
            cur_obj["date"] = row["Date"]
            cur_obj["ticker"] = self.ticker.ticker_string
            for period in self.config["periods"]:
                column_name = f"{self._name}_{period.get('k')}"
                signal_column_name = f"signal_{column_name}"
                cur_obj[column_name] = row[column_name]
                cur_obj[signal_column_name] = row[signal_column_name]
            total_obj.append(cur_obj)
        del working_data
        return total_obj

    def get_lookup_update(self, after_date=None):
        working_data = self.data.round(3)
        if after_date:
            working_data = working_data[working_data["Date"] >= after_date]
        lookups = list()
        updates = list()
        for _, row in working_data.iterrows():
            lookup = dict()
            lookup["date"] = row["Date"]
            lookup["ticker"] = self.ticker.ticker_string
            lookups.append(lookup)

            update = dict()
            _sets = dict()
            for period in self.config["periods"]:
                _sets[f"{self._name}_{period.get('k')}"] = row[f"{self._name}_{period.get('k')}"]
                _sets[f"signal_{self._name}_{period.get('k')}"] = row[f"signal_{self._name}_{period.get('k')}"]
            update["$set"] = _sets
            updates.append(update)
        del working_data
        return lookups, updates


# if __name__ == '__main__':
#     from ticker import Ticker
#     STOCK_DATA_API_URL = "http://192.168.15.70:8000/finValues?company={}&start={}"
#     DATA_START_DATE_LIMIT = "03-01-2017"
#     tick = Ticker("FB", DATA_START_DATE_LIMIT, STOCK_DATA_API_URL, fields=["High", "Low", "Open", "Close", "Volume"])
#
#     config = {"periods" : [{"k" : 14, "d" : 3}]}
#
#     stoch = STOCH(config=config, ticker_obj=tick)
#     stoch.calculate()
#     print(stoch.data.tail())
