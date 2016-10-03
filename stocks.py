import csv
import urllib.request

yahoo_url = "http://download.finance.yahoo.com/d/quotes.csv?s="
options = "&f=l1oghjkj1"

def get_stock_info(ticker):
    data = urllib.request.urlopen(yahoo_url + ticker + options).read().decode("utf-8").split(",")
    response = "%s | Last Trade: $%s | Open: $%s | Low: $%s | High: $%s | 52WK Low: $%s | 52WK High: $%s | Mkt Cap: $%s" % (ticker, data[0], data[1], data[2], data[3], data[4], data[5], data[6])
    return response
