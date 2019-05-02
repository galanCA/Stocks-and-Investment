from stock import stock


def main():
	ticker_list = ['GPRO','SNAP','SPOT']
	for ticker in ticker_list:
		print(ticker)
		TMK = stock(ticker)
		TMK.priceBookValue('quarterly')
		TMK.priceBookRatio('quarterly')
		TMK.EPS()
		TMK.currentRatio()
		print()
		print()
		print()

if __name__ == '__main__':
	main()