from django.db import models

# Create your models here.


class Stock(models.Model):
    ticker = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    website = models.URLField()

    def __str__(self):
        return self.ticker


class KeyExecutive(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    yob = models.IntegerField()
    stock = models.ForeignKey(Stock, related_name="key_executives", on_delete=models.CASCADE)

    def __str__(self):
        return "{} -- {} -- {}".format(self.name, self.title, self.stock.ticker)


class StockPrice(models.Model):
    ticker = models.ForeignKey(Stock, related_name="price", on_delete=models.CASCADE)
    date = models.DateField()
    open_price = models.DecimalField(max_digits=8, decimal_places=4)
    high_price = models.DecimalField(max_digits=8, decimal_places=4)
    low_price = models.DecimalField(max_digits=8, decimal_places=4)
    close_price = models.DecimalField(max_digits=8, decimal_places=4)
    total_traded_quantity = models.BigIntegerField()

    def __str__(self):
        return "{} -- {} -- Rs. {}".format(self.ticker, self.date, self.close_price)


class StockNews(models.Model):
    ticker = models.ForeignKey(Stock, related_name="news", on_delete=models.CASCADE)
    date = models.DateField()
    headline = models.TextField()
    sentiment = models.CharField(max_length=10)

    def __str__(self):
        return "{} -- {} -- {}".format(self.ticker, self.date, self.sentiment)


class StockTweet(models.Model):
    ticker = models.ForeignKey(Stock, related_name="tweets", on_delete=models.CASCADE)
    date = models.DateField()
    tweet = models.TextField()
    sentiment = models.CharField(max_length=10)

    def __str__(self):
        return "{} -- {} -- {}".format(self.ticker, self.date, self.sentiment)
