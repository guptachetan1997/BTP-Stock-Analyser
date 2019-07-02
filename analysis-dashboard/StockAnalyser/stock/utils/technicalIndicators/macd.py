"""
    Calculate the Moving Average Convergence Divergence
"""
from stock.utils.technicalIndicators.base_indicator import Indicator


class MACD(Indicator):
    _name = "macd"

    def calculate(self):
        SIGNAL_SPEED = self.config["signal_speed"]
        for period in self.config["periods"]:
            FAST = period["fast"]
            SLOW = period["slow"]
            fast_ema = f"ema_{self.config['action'].lower()}_{FAST}"
            slow_ema = f"ema_{self.config['action'].lower()}_{SLOW}"
            if fast_ema not in self.data:
                fast_ema_obj = self.ticker.get_indicator(indicator_name="ema", indicator_config={"periods": [FAST], "action": self.config["action"]})
                fast_ema_obj.calculate()
            if slow_ema not in self.data:
                slow_ema_obj = self.ticker.get_indicator(indicator_name="ema", indicator_config={"periods": [SLOW], "action": self.config["action"]})
                slow_ema_obj.calculate()

            column_name = f"macd_{self.config['action'].lower()}_{FAST}_{SLOW}"
            signal_column_name = f"signal_{column_name}_{SIGNAL_SPEED}"
            self.data[column_name] = self.data[fast_ema] - self.data[slow_ema]
            signal_ema = self.ticker.get_indicator(indicator_name="ema", indicator_config={"periods": [SIGNAL_SPEED], "action": column_name})
            signal_ema.calculate()
            self.data[signal_column_name] = self.data[f"ema_{column_name}_{SIGNAL_SPEED}"]
            del self.data[f"ema_{column_name}_{SIGNAL_SPEED}"]

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
                column_name = f"{self._name}_{self.config.get('action').lower()}_{period.get('fast')}_{period.get('slow')}"
                signal_column_name = f"signal_{column_name}_{self.config['signal_speed']}"
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
                _sets[f"{self._name}_{period.get('fast')}_{period.get('slow')}"] = row[
                    f"{self._name}_{self.config.get('action').lower()}_{period.get('fast')}_{period.get('slow')}"]
                _sets[f"signal_{self._name}_{period.get('fast')}_{period.get('slow')}_{self.config['signal_speed']}"] = row[
                    f"signal_{self._name}_{self.config.get('action').lower()}_{period.get('fast')}_{period.get('slow')}_{self.config['signal_speed']}"]
            update["$set"] = _sets
            updates.append(update)
        del working_data
        return lookups, updates


# if __name__ == '__main__':
#     from ticker import Ticker
#
#     STOCK_DATA_API_URL = "http://192.168.15.70:8000/finValues?company={}&start={}"
#     DATA_START_DATE_LIMIT = "03-01-2017"
#     tick = Ticker("FB", DATA_START_DATE_LIMIT, STOCK_DATA_API_URL, fields=["High", "Low", "Open", "Close", "Volume"])
#     config = {"periods" : [{"fast" : 12, "slow" : 26}], "action" : "Close", "signal_speed" : 9}
#
#     macd = MACD(config=config, ticker_obj=tick)
#     macd.calculate()
#     print(macd.data.tail())