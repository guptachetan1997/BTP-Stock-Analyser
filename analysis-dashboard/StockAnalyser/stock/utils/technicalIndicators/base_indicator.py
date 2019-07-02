"""
    The parent class for all indicators
"""


class Indicator:
    _name = "default"

    def __init__(self,config, ticker_obj):
        self.config = config
        self.data = ticker_obj.data
        self.ticker = ticker_obj

    def calculate(self):
        pass

    def get_json(self, after_date=None):
        working_data = self.data.round(3)
        if after_date:
            working_data = working_data[working_data["Date"]>=after_date]
        total_obj = []
        for _, row in working_data.iterrows():
            cur_obj = dict()
            cur_obj["date"] = row["Date"]
            cur_obj["ticker"] = self.ticker.ticker_string
            for period in self.config["periods"]:
                column_name = f"{self._name}_{self.config.get('action').lower()}_{period}"
                cur_obj[column_name] = row[column_name]
            total_obj.append(cur_obj)
        del working_data
        return total_obj

    def get_lookup_update(self, after_date=None):
        working_data = self.data.round(3)
        if after_date:
            working_data = working_data[working_data["Date"]>=after_date]
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
                _sets[f"{self._name}_{period}"] = row[f"{self._name}_{self.config.get('action').lower()}_{period}"]
            update["$set"] = _sets
            updates.append(update)
        del working_data
        return lookups, updates

    def push_to_mongo(self, after_date, mongo_client, mongo_db, mongo_collection):
        from pymongo import MongoClient
        client = MongoClient(mongo_client)
        db = client[mongo_db]
        collection = db[mongo_collection]
        lookups, updates = self.get_lookup_update(after_date=after_date)
        for a, b in zip(lookups, updates):
            collection.update(a, b, upsert=True)