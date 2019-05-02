from stock import stock


def main():
	#ticker_list = ['GPRO','SNAP','SPOT']
	ticker_list = ["KO"]
	for ticker in ticker_list:
		print(ticker)
		TMK = stock(ticker)

		TMK.priceBookRatio('quarterly')
		TMK.EPS('quarterly')
		TMK.currentRatio('quarterly')
		TMK.grahamNumber('quarterly')
		print(TMK.valuations[["Price-Book","Graham-number"]])
		print(TMK.financial[["EPS","current-ratio"]])
		print(TMK.trade_history[["Close","Open","High","Low"]][0])


if __name__ == '__main__':
	main()