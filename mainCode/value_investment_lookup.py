from stock import stock, getNASDAQTickerList, getSP500TickerList
from decimal import *

def defensive_investor_portafolio(ticker):
	TMK = stock(ticker)

	####################### Enterprise Size ######################
	TMK.income()
	if TMK.income_stmts.empty:
		return False
	if TMK.income_stmts["totalRevenue"][0] > 500000:
		print("\tSales/Enterprise Size: Ok")
	else:
		print("\tSales/Enterprise Size : Fail")
		return False

	####################### Liabilities vs assets #################
	TMK.income('quarterly')
	try:
		TMK.currentRatio('quarterly')
	except Exception as insta:
		return False

	if TMK.financial["current-ratio"][0] > 2:
		print("\tCurrent ratio: Ok")
	else:
		print("\tCurrent ratio: Fail")
		return False

	########################## Earnings stability over 10 years ##################
	TMK.EPS('quarterly')
	if TMK.financial["EPS"][0] > 0:
		print("\tEarnings per share: Ok")
	else:
		print("\tEarnings per share: Fail")
		return False

	###################### Dividends more than 20 years ###########################

	if TMK.dividendCheck():
		print("\tDividends: Ok")
	else:
		print("\tDividends: Fail")
		return False
	####################### Earnings growth and profitablity ######################

	########################### Price to earning ratio ############################
	TMK.priceEarning('quarterly')
	print (TMK.valuation["price-earnings"])
	if TMK.valuation["price-earnings"][0] > 15:
		print("\tPrice earnings: Ok")
	else:
		print("\tPrice earnings: Fail")
		return False

	################################ Price to assets #########################

	return True

def main():
	#ticker_list = ['GPRO','SNAP','SPOT','TSLA','AAPL',"KO"]
	ticker_list = ["BRK-B"]
	ticker_nasdaq = getNASDAQTickerList()
	SP500_ticker = getSP500TickerList()
	#print (ticker_nasdaq)
	
	'''
	for ticker in ticker_list:
		print(ticker)
		print(ticker,": ", defensive_investor_portafolio(ticker))
	'''

	
	for index, ticker in SP500_ticker.iterrows():
		print(ticker["Symbol"])
		try:
			print(ticker["Symbol"],": ", defensive_investor_portafolio(ticker["Symbol"]))
		except KeyError:
			pass



	'''
	for index,ticker in ticker_nasdaq.iterrows():
		#print (ticker["ETF"])
		if "N" in ticker["ETF"]: 
			print(ticker["Symbol"])
			print(ticker["Symbol"],": ", defensive_investor_portafolio(ticker["Symbol"]))
			print()
	'''
if __name__ == '__main__':
	main()