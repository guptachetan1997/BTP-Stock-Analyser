"""
    The Ticker class
"""
import pandas as pd
import datetime
from stock.utils.technicalIndicators.indicator_factory import IndicatorFactory
from stock.models import StockPrice, Stock


class Error(Exception):
    """Base class for other exceptions"""
    pass


class NotEnoughDataFromStockAPI(Error):
    """Raised when their is not enough data from the API"""
    pass


class NoDataFromStockAPI(Error):
    """Raised when their is no data from the API"""
    pass


class IndicatorDoesNotExist(Error):
    """Raised when an invalid/non-existent indicator is given"""
    pass


class Ticker:
    def __init__(self, ticker_string, start_date, fields=["High", "Low", "Open", "Close"]):
        self.ticker_string = ticker_string
        self.data = None
        self.data_flag = False
        self.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        self.fields = fields
        self._get_data()

    @staticmethod
    def _convert_qs_to_df(stock_price_qs):
        all_data = []
        for stock_price in stock_price_qs:
            stock_price_obj = {
                "Date": stock_price.date,
                "High": float(stock_price.high_price),
                "Low": float(stock_price.low_price),
                "Open": float(stock_price.open_price),
                "Close": float(stock_price.close_price),
                "Volume": stock_price.total_traded_quantity
            }
            all_data.append(stock_price_obj)
        df = pd.DataFrame(all_data)
        return df

    def _get_data(self):
        self.data_flag = False
        try:
            stock_obj = Stock.objects.get(ticker=self.ticker_string)
            data = StockPrice.objects.filter(ticker=stock_obj, date__gte=self.start_date).order_by("date")
            self.data = self._convert_qs_to_df(data)
        except Exception as e:
            print(e)
            self.data = pd.DataFrame(columns=["Date"] + self.fields)

    def get_indicator(self, indicator_name, indicator_config):
        indicator_class = IndicatorFactory.get(indicator_name)
        if indicator_class is None:
            raise IndicatorDoesNotExist
        else:
            return indicator_class(config=indicator_config, ticker_obj=self)


