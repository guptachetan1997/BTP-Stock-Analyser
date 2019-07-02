"""
    The Factory class for indicators
"""
from stock.utils.technicalIndicators import atr, cci, ema, macd, rsi, sma, stoch, stochrsi, trix, wr, obv, cmf, mfi, pgo


class IndicatorFactory(object):

    @staticmethod
    def get(indicator):
        try:
            return getattr(globals()[indicator], indicator.upper())
        except KeyError:
            return None


# if __name__ == '__main__':
#     print(IndicatorFactory.get("atr"))
#     print(IndicatorFactory.get("atr"))
