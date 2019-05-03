from stock import stock
from decimal import *

def main():
	ticker_list = ['GPRO','SNAP','SPOT','TSLA','AAPL',"KO"]
	#sticker_list = ["AAPL"]
	for ticker in ticker_list:
		print(ticker)
		TMK = stock(ticker)

		TMK.priceBookRatio('quarterly')
		TMK.EPS('quarterly')
		TMK.currentRatio('quarterly')
		TMK.grahamNumber('quarterly')
		TMK.priceEarning('quarterly')
		TMK.priceGraham('quarterly')
		print(TMK.valuations[["Price-Book","price-earnings","Graham-number", "price-Graham"]])
		print(TMK.financial[["EPS","current-ratio"]])
		print("\n",TMK.income_stmts["Close"])
		#print(TMK.trade_history)
		print("Close:", TMK.trade_history["Close"][-1])

		'''
		print ("Earnings per share: ", )
		if TMK.financial["EPS"] > 0:
			print("Ok")
		else:
			print("Fail")

		print ("Graham percentage: ")
		if TMK.valuations["price-Graham"] < 100:
			print("Ok")
		else:
			print("Fail")

		print("Graham Number: ")
		if TMK.valuations["Graham-number"] < TMK.trade_history["Close"][0]:
			print("Ok")
		else:
			print ("Fail")

		'''


if __name__ == '__main__':
	main()