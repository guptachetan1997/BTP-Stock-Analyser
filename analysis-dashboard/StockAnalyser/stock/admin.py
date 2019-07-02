from django.contrib import admin

# Register your models here.
from stock.models import Stock, StockPrice, KeyExecutive, StockNews, StockTweet

admin.site.register(Stock)
admin.site.register(StockPrice)
admin.site.register(KeyExecutive)
admin.site.register(StockNews)
admin.site.register(StockTweet)