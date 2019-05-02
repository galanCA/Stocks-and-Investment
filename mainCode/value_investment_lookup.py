from stock import stock


def main():
	ticker_list = ['GPRO','SNAP','SPOT']
	#ticker_list = ["KO"]
	for ticker in ticker_list:
		print(ticker)
		TMK = stock(ticker)

		TMK.priceBookRatio('quarterly')
		TMK.EPS('quarterly')
		TMK.currentRatio('quarterly')
		TMK.grahamNumber('quarterly')
		TMK.priceEarning('quarterly')
		TMK.priceGraham('quarterly')
		print(TMK.valuations[["Price-Book","Graham-number","price-earnings", "price-Graham"]])
		print(TMK.financial[["EPS","current-ratio"]])
		print(TMK.trade_history["Close"][0])


if __name__ == '__main__':
	main()