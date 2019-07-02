from django.shortcuts import render
from stock.models import Stock, StockPrice, StockNews, StockTweet
from datetime import datetime, date
from stock.utils.ticker import Ticker
import json
from stock.utils.signals import Signals
import math
from collections import Counter
import pandas as pd
from stock.utils.load_data import import_news_data, import_tweets_data
# Create your views here.


def home(request):
    tickers = Stock.objects.all().values_list('ticker', flat=True)
    return render(request, "stock/home.html", {"tickers": tickers})


def stock_detail(request, ticker):
    with open("/Users/chetangupta/Documents/College/BTP/stock analysis code/analysis-dashboard/StockAnalyser/stock/utils/INDICATOR_CONFIG.json") as file:
        config = json.load(file)

    try:
        stock_obj = Stock.objects.get(ticker__iexact=ticker)
        key_executives = stock_obj.key_executives.all()
        historical_price = StockPrice.objects.filter(ticker=stock_obj, date__gte=date(2014, 12, 4))
        historical_price_data = historical_price.order_by("-date")[:10]

        ticker_obj = Ticker(ticker_string=ticker, start_date="2014-12-04")

        for indicator_name in config["INDICATORS_CONFIG"]:
            indicator_obj = ticker_obj.get_indicator(indicator_name=indicator_name,
                                                     indicator_config=config["INDICATORS_CONFIG"][indicator_name])
            indicator_obj.calculate()
        indicator_starting_point = 850
        chart_payload = {
            "date": [x.date.strftime("%Y-%m-%d") for x in historical_price][indicator_starting_point:],
            "close": ["{}".format(x.close_price) for x in historical_price][indicator_starting_point:],
            "volume": [x.total_traded_quantity for x in historical_price][indicator_starting_point:]
        }
        for col in list(ticker_obj.data.columns.values):
            if col is not "Date":
                chart_payload[col.replace("|", "_")] = [0 if math.isnan(x) else x for x in list(
                    ticker_obj.data[col].values)][indicator_starting_point:]

        technical_analysis_signals = Signals(ticker=ticker, data_df=ticker_obj.data)
        stock_news = StockNews.objects.filter(ticker=stock_obj).order_by("-date")[:10]
        news_analysis_signal = Counter([x.sentiment for x in stock_news]).most_common(1)[0][0]

        stock_tweets = StockTweet.objects.filter(ticker=stock_obj).order_by("-date")[:10]
        tweets_analysis_signal = Counter([x.sentiment for x in stock_news]).most_common(1)[0][0]

        overall_signal = Counter([technical_analysis_signals.overall_signal,
                                  news_analysis_signal, tweets_analysis_signal]).most_common(1)[0][0]
        signals = {
            "overall": overall_signal,
            "technical_indicators": technical_analysis_signals.overall_signal,
            "all_technical_indicators": technical_analysis_signals.overall_signal_data,
            "news_analysis": news_analysis_signal,
            "twitter_analysis": tweets_analysis_signal
        }

    except Stock.DoesNotExist:
        stock_obj = None
        key_executives = None
        signals = None
        historical_price_data = None
        chart_payload = None
        stock_news = None,
        stock_tweets = None

    return render(request, "stock/stock.html", {
        "stock": stock_obj,
        "key_executives": key_executives,
        "signals": signals,
        "historical_data": historical_price_data,
        "chart_payload": chart_payload,
        "stock_news": stock_news,
        "stock_tweets": stock_tweets,
    })
