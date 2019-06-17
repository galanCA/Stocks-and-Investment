from stock import stock, getNASDAQTickerList, getSP500TickerList
from decimal import *

def defensive_investor_portafolio(ticker):
	TMK = stock(ticker)

	######################## Total Debt vs Current Ratio ################
	'''
	Debt to current ratio secures low debt load to the company

	try:
		TMK.debtPerCurrentRatio('quarterly')
	except Exception as insta:
		return False

	if TMK.financial["debt-current-ratio"][0] < 1.10:
		print("\t[ Ok ] Debt to Current ratio")
	else:
		print("\t[Fail] Debt to Current ratio")
		return False
	'''

	####################### Liabilities vs assets #################
	'''
	Current Liabilities or the ratio between assets over liabilities be greater than 2
	'''
	try:
		TMK.currentRatio('quarterly')
	except Exception as insta:
		return False

	if TMK.financial["current-ratio"][0] > 2:
		print("\t[ Ok ] Current ratio")
	else:
		print("\t[Fail] Current ratio")
		return False

	########################### Price to earning ratio ############################
	'''
	Price to Earnings is su
	'''
	
	TMK.trailingPE()
	#print(TMK.trading["price-earnings"][0])
	if TMK.trading["price-earnings"][0] < 22.5:
		print("\t[ Ok ] Price earnings")
	else:
		print("\t[Fail] Price earnings")
		return False

	########################## Price to assets ########################
	TMK.pricePerBookValue()

	if TMK.trading["price-book value"][0] < 2:
		print("\t[ Ok ] Price book value")
	else:
		print("\t[Fail] Price book value")
		return False

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

	###################### Dividends more than 20 years ###########################
	'''
	Pay dividends
	'''
	if TMK.dividendCheck():
		print("\t[ Ok ] Dividends")
	else:
		print("\t[Fail] Dividends")
		return False

	########################## Earnings stability over 10 years ##################
	'''
	10 Years of Profits will make sure the enterprise is a sound enterprise
	'''
	TMK.EPS()
	for  eps in TMK.financial["EPS"]:
		if eps < 0:
			print("\t[Fail] Earnings per share Stability")
			return False
		
	print("\t[ Ok ] Earnings per share Stability")

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

	
	
	############################# End ####################################
	return True

def asdadsd(ticker):
	TMK = stock(ticker)

	###################### Current price to book ratio #################
	TMK.pricePerBookValue()

	TMK.trading["price-book value"][0]

	TMK.valuation["book value"][0]




	###################### When to sell #############



def main():
	tickerSwitcher = "NASDAQ"
	#tickerSwitcher = "ticker list"
	#tickerSwitcher = "S&P500"

	if tickerSwitcher is "ticker list":
		ticker_list = ['GSBC','AMG','SNA','COG','GPRO','SNAP','SPOT','TSLA','AAPL',"KO"]
		for ticker in ticker_list:
			print(ticker)
			print(ticker,": ", defensive_investor_portafolio(ticker))
	

	elif tickerSwitcher is "S&P500":
		SP500_ticker = getSP500TickerList()
		passTestStock = []

		for index, ticker in SP500_ticker.iterrows():
			print(ticker["Symbol"])
			try:
				worthy = defensive_investor_portafolio(ticker["Symbol"])
				print(ticker["Symbol"],": ", worthy)
				if worthy:
					passTestStock.append(ticker["Symbol"])

			except KeyError:
				pass

		print("Stock to look into: ", passTestStock)

	elif tickerSwitcher is "NASDAQ":
		ticker_nasdaq = getNASDAQTickerList()
		passTestStock = []
		nasdaq_length = len(ticker_nasdaq)

		for index, ticker in ticker_nasdaq.iterrows():

			if "N" in ticker["ETF"]: 
				print(float(index)/float(nasdaq_length)	,"% ", ticker["Symbol"])
				try:
					worthy = defensive_investor_portafolio(ticker["Symbol"])
				except KeyError:
					continue
				print(ticker["Symbol"],": ", worthy)
				print("\n")
				if worthy:
					passTestStock.append(ticker["Symbol"])

		print("Stock to look into: ", passTestStock)

if __name__ == '__main__':
	main()