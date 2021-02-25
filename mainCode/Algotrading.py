'''
Author: Cesar Galan
Date created: 2/21/2021
Function: Automize the look up of probable stocks




'''


# Libraries
from stock import stock





ticker = "TSLA"
TRL = stock(ticker, days=400)
print(TRL.trade_history)

