from stock import stock



ticker = "TSLA"
TRL = stock(ticker, days=400)
print(TRL.trade_history)