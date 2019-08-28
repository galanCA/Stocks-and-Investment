import sys
sys.path.append('../Functions and Libs/')

from stock import stock, getNASDAQTickerList, getSP500TickerList, getOtherTickerList
from decimal import *
from email_msg import emailMessage, email_information


def defensive_investor_portafolio(ticker, highprice=10000, 
									max_current_ratio=2, 
									min_price_earnings=22.5, 
									max_price_book_value=1, 
									min_total_revenue = 500000, 
									dividends_on = True, 
									min_earnings_stability=0, 
									min_earnings_growth=6):
	try:
		TMK = stock(ticker)
	except:
		return False

	if (highprice <TMK.trade_history["Close"][-1]):
		print ("\t [Fail] Price")
		return False

	####################### Liabilities vs assets #################
	'''
	Current Liabilities or the ratio between assets over liabilities be greater than 2
	'''
	try:
		TMK.currentRatio('quarterly')
	except Exception as insta:
		return False

	if TMK.financial["current-ratio"][0] > max_current_ratio:
		print("\t[ Ok ] Current ratio")
	else:
		print("\t[Fail] Current ratio")
		return False

	########################### Price to earning ratio ############################
	'''
	Price to Earnings is su
	'''
	try:
		TMK.trailingPE()
	except Exception as insta:
		return False
		
	if TMK.trading["price-earnings"][0] < min_price_earnings:
		print("\t[ Ok ] Price earnings")
	else:
		print("\t[Fail] Price earnings")
		return False

	########################## Price to assets ########################
	try:
		TMK.pricePerBookValue()
	except Exception as insta:
		return False
	if TMK.trading["price-book value"][0] < max_price_book_value and TMK.trading["price-book value"][0] >= 0:
		print("\t[ Ok ] Price book value")
	else:
		print("\t[Fail] Price book value")
		return False

	####################### Enterprise Size ######################
	'''
	Maker sure the enterprise has more than certain amount of sales a year
	'''
	try:
		TMK.income()
	except Exception as insta:
		return False



	if TMK.income_stmts.empty:
		return False
	if TMK.income_stmts["totalRevenue"][0] > min_total_revenue:
		print("\t[ Ok ] Sales/Enterprise Size")
	else:
		print("\t[Fail] Sales/Enterprise Size")
		return False

	###################### Dividends more than 20 years ###########################
	'''
	Pay dividends
	'''
	if dividends_on:
		if TMK.dividendCheck():
			print("\t[ Ok ] Dividends")
		else:
			print("\t[Fail] Dividends")
			return False

	########################## Earnings stability over 10 years ##################
	'''
	10 Years of Profits will make sure the enterprise is a sound enterprise
	'''
	
	try:
		TMK.EPS()
	except Exception as insta:
		return False

	'''
	if all(i >= min_earnings_stability for i in TMK.financial["EPS"]):
		print("\t[ Ok ] Earnings per share Stability")
	else:
		print("\t[Fail] Earnings per share Stability")
	'''
	for  eps in TMK.financial["EPS"]:
		if eps < min_earnings_stability:
			print("\t[Fail] Earnings per share Stability")
			return False

	print("\t[ Ok ] Earnings per share Stability")
	
	

	####################### Earnings growth and profitablity ######################
	'''
	Make sure the enterprise growth with at least inflation 3% - uses (1 + 0.03)^Years

	idealy get the 3 year average at the beginning and the end to prevent dips for a 10 year

	This case will be 2 year average of 4 years

	Curretly uses 12 for 

	'''

	try:
		eps_avg_beginning = (TMK.financial["EPS"][2] + TMK.financial["EPS"][3])/2
		eps_avg_end = (TMK.financial["EPS"][0] + TMK.financial["EPS"][1])/2
	except IndexError:
		return False

	eps_growth = 100*((eps_avg_end - eps_avg_beginning)/eps_avg_beginning)
	if eps_growth > min_earnings_growth:
		print("\t[ Ok ] Earnings per share Growth")
	else:
		print("\t[Fail] Earnings per share Growth")
		return False

	############################# End ####################################
	return True

def valueStocks(ticker):
	'''
	Check When to buy when to sell. 
		Find the risk-rewards
		Check how managment is doing
	'''

	TMK = stock(ticker)	


	###################### Current price to book ratio #################
	TMK.bookValuePerShare()
	TMK.pricePerBookValue()


	print ("Current Price: ", TMK.trade_history["Close"][-1])
	print ("Book value: %0.2f" %(TMK.trading["book value per share"][0]))
	
	print ("Price - book value: %0.2f " %(TMK.trading["price-book value"][0]))
	#print ("Sell at: %0.2f" % (TMK.trading["book value per share"][0]*2))

	print ("Percent return: %0.2f%%" %(100*(TMK.trading["book value per share"][0]-TMK.trade_history["Close"][-1])/TMK.trade_history["Close"][-1]) )


	msg = "%s: \nCurrent Price:\t\t%0.2f\nBook value:\t\t%0.2f\nPrice-book value:\t%0.2f\n"%(ticker, TMK.trade_history["Close"][-1], TMK.trading["book value per share"][0],TMK.trading["price-book value"][0])

	return msg

def main():
	to_email, from_email, pwd_email, title = email_information('../email_passwd.init')

	tickerSwitcher = "Full"
	#tickerSwitcher = "Other"
	#tickerSwitcher = "NASDAQ"
	#tickerSwitcher = "ticker list"
	#tickerSwitcher = "S&P500"

	if tickerSwitcher is "ticker list":
		print ("Specific Ticker")
		ticker_list = ['FANH', 'IMOS', 'JOBS', 'MOMO', 'NATH', 'NCMI', 'NWLI', 'OMAB', 'OSN', 'SNFCA', 'SNH', 'SNHNL', 'WILC', 'YNDX', 'YY']

		passTestStock = []
		for ticker in ticker_list:
			print(ticker)	
			worthy = defensive_investor_portafolio(ticker,dividends_on=False)
			print(ticker,": ", worthy,"\n")
			if worthy:
				passTestStock.append(ticker)
	

	elif tickerSwitcher is "S&P500":
		print("S&P 500 list")
		SP500_ticker = getSP500TickerList()
		passTestStock = []

		for index, ticker in SP500_ticker.iterrows():
			print(ticker["Symbol"])
			try:
				worthy = defensive_investor_portafolio(ticker["Symbol"],dividends_on=False)
				print(ticker["Symbol"],": ", worthy)
				if worthy:
					passTestStock.append(ticker["Symbol"])

			except KeyError:
				pass

		print("Stock to look into: ", passTestStock)

	elif tickerSwitcher is "NASDAQ":
		print ("NASDAQ List")
		ticker_nasdaq = getNASDAQTickerList()
		passTestStock = []
		nasdaq_length = len(ticker_nasdaq)
		print (nasdaq_length)
		for index, ticker in ticker_nasdaq.iterrows():
			if "N" in ticker["ETF"]: 
				print("%s - %0.2f%%" % (ticker["Symbol"], float(index)/float(nasdaq_length)*100))
				try:
					worthy = defensive_investor_portafolio(ticker["Symbol"],dividends_on=False)
				except KeyError:
					continue
				print(ticker["Symbol"],": ", worthy)
				print("\n")
				if worthy:
					passTestStock.append(ticker["Symbol"])

	elif tickerSwitcher is "Other":
		print ("Other List")
		passTestStock = []
		ticker_other = getOtherTickerList()
		other_length = len(ticker_other)

		for index, ticker in ticker_other.iterrows():
			if "N" in ticker["ETF"]:
				print("%s - %0.2f%%" % (ticker["NASDAQ Symbol"], float(index)/float(other_length)*100))
				try:
					worthy = defensive_investor_portafolio(ticker["NASDAQ Symbol"], dividends_on=False)
				except KeyError:
					continue
				print(ticker["NASDAQ Symbol"],": ", worthy)
				print("\n")
				if worthy:
					passTestStock.append(ticker["NASDAQ Symbol"])

	elif tickerSwitcher is "Full":
		print("Full")
		passTestStock = []
		ticker_nasdaq = getNASDAQTickerList()
		ticker_other = getOtherTickerList()
		nasdaq_length = len(ticker_nasdaq)
		other_length = len(ticker_other)
		print("total tickers", nasdaq_length+other_length)

		for index, ticker in ticker_nasdaq.iterrows():
			if "N" in ticker["ETF"]: 
				print("%s - %0.3f%%" % (ticker["Symbol"], float(index)/float(nasdaq_length+other_length)*100))
				try:
					worthy = defensive_investor_portafolio(ticker["Symbol"],dividends_on=False)
				except KeyError:
					continue
				print(ticker["Symbol"],": ", worthy)
				print("\n")
				if worthy:
					passTestStock.append(ticker["Symbol"])

		for index, ticker in ticker_other.iterrows():
			if "N" in ticker["ETF"]:
				print("%s - %0.3f%%" % (ticker["NASDAQ Symbol"], float(index+nasdaq_length)/float(nasdaq_length+other_length)*100))
				try:
					worthy = defensive_investor_portafolio(ticker["NASDAQ Symbol"], dividends_on=False)
				except KeyError:
					continue
				
				print(ticker["NASDAQ Symbol"],": ", worthy)
				print("\n")
				if worthy:
					passTestStock.append(ticker["NASDAQ Symbol"])

	print("Stock to look into: ", passTestStock)

	print("Stock that pass the test")
	email_msg = ""
	for ticker in passTestStock:
		print (ticker)
		email_msg = email_msg + valueStocks(ticker)
		print(" ")

	print("email content: ")
	print(email_msg)

	emailMessage(to_email, from_email, pwd_email, title, email_msg)

if __name__ == '__main__':
	main()
