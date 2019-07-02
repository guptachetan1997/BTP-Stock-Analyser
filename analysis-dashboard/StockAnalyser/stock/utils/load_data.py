import pandas as pd
from datetime import datetime
from stock.models import Stock, StockPrice, StockNews, StockTweet


def import_price_data():
    csv_file = "/Users/chetangupta/Documents/College/BTP/stock analysis code/analysis-dashboard/StockAnalyser/stock/utils/price_data.csv"
    price_df = pd.read_csv(csv_file)
    stock_ids = {x.ticker: x for x in Stock.objects.all()}
    for row in price_df.iterrows():
        stock_price_obj = StockPrice()
        stock_price_obj.ticker = stock_ids[row[1]["Symbol"]]
        stock_price_obj.date = datetime.strptime(row[1]["date"], "%Y-%m-%d").date()
        stock_price_obj.open_price = row[1]["Open Price"]
        stock_price_obj.high_price = row[1]["High Price"]
        stock_price_obj.low_price = row[1]["Low Price"]
        stock_price_obj.close_price = row[1]["Close Price"]
        stock_price_obj.total_traded_quantity = row[1]["Total Traded Quantity"]
        stock_price_obj.save()


def import_news_data():
    csv_file = "/Users/chetangupta/Documents/College/BTP/stock analysis code/analysis-dashboard/StockAnalyser/stock/utils/predicted_news.csv"
    news_df = pd.read_csv(csv_file, sep="~")
    stock_ids = {x.ticker: x for x in Stock.objects.all()}
    for row in news_df.iterrows():
        stock_news_obj = StockNews()
        stock_news_obj.ticker = stock_ids[row[1]["Symbol"]]
        stock_news_obj.date = datetime.strptime(row[1]["date"], "%Y-%m-%d").date()
        stock_news_obj.headline = row[1]["headline"]
        if row[1]["prediction"] == 0:
            stock_news_obj.sentiment = "Sell"
        else:
            stock_news_obj.sentiment = "Buy"
        stock_news_obj.save()


def import_tweets_data():
    csv_file = "/Users/chetangupta/Documents/College/BTP/stock analysis code/analysis-dashboard/StockAnalyser/stock/utils/predicted_tweets.csv"
    news_df = pd.read_csv(csv_file, sep="~")
    stock_ids = {x.ticker: x for x in Stock.objects.all()}
    for row in news_df.iterrows():
        stock_tweet_obj = StockTweet()
        stock_tweet_obj.ticker = stock_ids[row[1]["Symbol"]]
        stock_tweet_obj.date = datetime.strptime(row[1]["date"], "%Y-%m-%d").date()
        stock_tweet_obj.tweet = row[1]["tweet"]
        if row[1]["change_prediction"] == 0:
            stock_tweet_obj.sentiment = "Sell"
        else:
            stock_tweet_obj.sentiment = "Buy"
        stock_tweet_obj.save()
