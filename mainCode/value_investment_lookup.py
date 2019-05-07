from stock import stock, getTickerList
from decimal import *

def GrahamCheck(ticker):
	TMK = stock(ticker)

	TMK.priceBookRatio('quarterly')
	TMK.EPS('quarterly')
	TMK.currentRatio('quarterly')
	TMK.grahamNumber('quarterly')
	TMK.priceEarning('quarterly')
	TMK.priceGraham('quarterly')
	#print(TMK.valuations[["Price-Book","price-earnings","Graham-number", "price-Graham"]])
	#print(TMK.financial[["EPS","current-ratio"]])
	#print("\n",TMK.income_stmts["Close"])
	#print(TMK.trade_history)
	#print("Close:", TMK.trade_history["Close"][-1])

	#print ("Earnings per share: ", )
	if TMK.financial["EPS"][0] > 0:
		print("Earnings per share: Ok")
	else:
		print("Earnings per share: Fail")
		return False

	#print ("Graham percentage: ")
	if TMK.valuations["price-Graham"][0] < 100:
		print("Graham percentage: Ok")
	else:
		print("Graham percentage: Fail")
		return False

	#print("Graham Number: ")
	if TMK.valuations["Graham-number"][0] < TMK.trade_history["Close"][0]:
		print("Graham Number: Ok")
	else:
		print ("Graham Number: Fail")
		return False

	return True

def main():
	ticker_list = ['GPRO','SNAP','SPOT','TSLA','AAPL',"KO"]
	#sticker_list = ["AAPL"]
	ticker_nasdaq = getTickerList()
	#print (ticker_nasdaq)
	
	for index,ticker in ticker_nasdaq.iterrows():
		#print (ticker["ETF"])
		if "N" in ticker["ETF"]: 
			print(ticker["Symbol"])
			print(ticker["Symbol"],": ", GrahamCheck(ticker["Symbol"]))
		

if __name__ == '__main__':
	main()