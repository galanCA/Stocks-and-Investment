from stock import stock, getNASDAQTickerList, getSP500TickerList
from decimal import *

def defensive_investor_portafolio(ticker):
	TMK = stock(ticker)

	####################### Enterprise Size ######################
	'''
	Maker sure the enterprise has more than certain amount of sales a year
	'''
	TMK.income()
	if TMK.income_stmts.empty:
		return False
	if TMK.income_stmts["totalRevenue"][0] > 500000:
		print("\t[ Ok ] Sales/Enterprise Size")
	else:
		print("\t[Fail] Sales/Enterprise Size")
		return False

	####################### Liabilities vs assets #################
	'''
	Current Liabilities or the ratio between assets over liabilities be greater than 2
	'''
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
	'''
	10 Years of Profits will make sure the enterprise is a sound enterprise
	'''
	TMK.EPS()
	for eps in TMK.financial["EPS"]:
		if eps < 0:
			print("\t[Fail] Earnings per share Stability")
			return False
		
	print("\t[ Ok ] Earnings per share Stability")


	###################### Dividends more than 20 years ###########################
	'''
	Pay dividends
	'''
	if TMK.dividendCheck():
		print("\t[ Ok ] Dividends")
	else:
		print("\t[Fail] Dividends")
		return False

	####################### Earnings growth and profitablity ######################
	'''
	Make sure the enterprise growth with at least inflation 3%
	'''
	eps_growth = 100*((TMK.financial["EPS"][0] - TMK.financial["EPS"][-1])/TMK.financial["EPS"][-1])
	if eps_growth > 3:
		print("\t[ Ok ] Earnings per share Growth")
	else:
		print("\t[Fail] Earnings per share Growth")
		return False

	########################### Price to earning ratio ############################
	'''
	Price to Earnings is su
	'''
	'''
	TMK.priceEarning('quarterly')
	#print (TMK.valuations["price-earnings"])
	if TMK.valuations	["price-earnings"][0] > 10:
		print("\t[ Ok ] Price earnings")
	else:
		print("\t[Fail] Price earnings")
		return False
	'''

	################################ Price to assets #########################
	'''
	Make sure that assets to price is not too expensive
	'''
	TMK.priceBookRatio('quarterly')
	if TMK.valuations["Price-Book"][0] < 1.5:
		print("\t[ Ok ] Price to Book value")
	else:
		print("\t[Fail] Price to Book value")
		return False

	############################# End ####################################
	return True

def main():
	#
	# tickerSwitcher = "ticker list"
	tickerSwitcher = "S&P500"

	if tickerSwitcher is "ticker list":
		ticker_list = ['CTL','ADS','COG','GPRO','SNAP','SPOT','TSLA','AAPL',"KO"]
		for ticker in ticker_list:
			print(ticker)
			print(ticker,": ", defensive_investor_portafolio(ticker))
	

	elif tickerSwitcher is "S&P500":
		SP500_ticker = getSP500TickerList()
		for index, ticker in SP500_ticker.iterrows():
			print(ticker["Symbol"])
			try:
				print(ticker["Symbol"],": ", defensive_investor_portafolio(ticker["Symbol"]))
			except KeyError:
				pass

	elif tickerSwitcher is "NASDAQ":
		ticker_nasdaq = getNASDAQTickerList()
		for index,ticker in ticker_nasdaq.iterrows():
			#print (ticker["ETF"])
			if "N" in ticker["ETF"]: 
				print(ticker["Symbol"])
				print(ticker["Symbol"],": ", defensive_investor_portafolio(ticker["Symbol"]))
				print("\n")

if __name__ == '__main__':
	main()