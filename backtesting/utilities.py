import yfinance as yf
import os

def check_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def search_ticker(query):
    stock = yf.Ticker(query)
    info = stock.info
    print(f"Available attributes: {', '.join(info.keys())}")

    print(f"Ticker: {query}")
    print(f"Short Name: {info.get('shortName', 'Not Found')}")
    print(f"Long Name: {info.get('longName', 'Not Found')}")
    print(f"Sector: {info.get('sector', 'Not Found')}")
    print(f"Industry: {info.get('industry', 'Not Found')}")
    print(f"Country: {info.get('country', 'Not Found')}")
    print(f"Currency: {info.get('currency', 'Not Found')}")
    print(f"Exchange: {info.get('exchange', 'Not Found')}")
    print(f"Previous Close: {info.get('regularMarketPreviousClose', 'Not Found')}")
    print(f"Market Cap: {info.get('marketCap', 'Not Found')}")
    print("")
