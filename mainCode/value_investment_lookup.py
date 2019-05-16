from stock import stock, getNASDAQTickerList, getSP500TickerList
from decimal import *

def defensive_investor_portafolio(ticker):
	TMK = stock(ticker)

	####################### Enterprise Size ######################
	TMK.income()
	if TMK.income_stmts.empty:
		return False
	if TMK.income_stmts["totalRevenue"][0] > 500000:
		print("\t[ Ok ] Sales/Enterprise Size")
	else:
		print("\t[Fail] Sales/Enterprise Size")
		return False

	####################### Liabilities vs assets #################
	TMK.income('quarterly')
	try:
		TMK.currentRatio('quarterly')
	except Exception as insta:
		return False

	if TMK.financial["current-ratio"][0] > 2:
		print("\t[ Ok ] Current ratio")
	else:
		print("\t[Fail] Current ratio")
		return False

	########################## Earnings stability over 10 years ##################
	TMK.EPS('quarterly')
	if TMK.financial["EPS"][0] > 0:
		print("\t[ Ok ] Earnings per share")
	else:
		print("\t[Fail] Earnings per share")
		return False

	###################### Dividends more than 20 years ###########################

	if TMK.dividendCheck():
		print("\t[ Ok ] Dividends")
	else:
		print("\t[Fail] Dividends")
		return False
	####################### Earnings growth and profitablity ######################

	########################### Price to earning ratio ############################
	TMK.priceEarning('quarterly')
	#print (TMK.valuations["price-earnings"])
	if TMK.valuations	["price-earnings"][0] > 15:
		print("\t[ Ok ] Price earnings")
	else:
		print("\t[Fail] Price earnings")
		return False

	################################ Price to assets #########################

	return True

def main():
	#
	tickerSwitcher = "ticker list"

	if tickerSwitcher is "ticker list":
		ticker_list = ['GPRO','SNAP','SPOT','TSLA','AAPL',"KO"]
		for ticker in ticker_list:
			print(ticker)
			print(ticker,": ", defensive_investor_portafolio(ticker))
	

	elif tickerSwitcher is "NASDAQ":
		ticker_nasdaq = getNASDAQTickerList()
		for index, ticker in SP500_ticker.iterrows():
			print(ticker["Symbol"])
			try:
				print(ticker["Symbol"],": ", defensive_investor_portafolio(ticker["Symbol"]))
			except KeyError:
				pass

	elif tickerSwitcher is "S&P500":
		SP500_ticker = getSP500TickerList()
		for index,ticker in ticker_nasdaq.iterrows():
			#print (ticker["ETF"])
			if "N" in ticker["ETF"]: 
				print(ticker["Symbol"])
				print(ticker["Symbol"],": ", defensive_investor_portafolio(ticker["Symbol"]))
				print()

if __name__ == '__main__':
	main()