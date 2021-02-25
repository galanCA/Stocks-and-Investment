


# Libraries
from stock import stock


def wsbMomentum(ticker):
	'''
	Weekly Impulse: 0, red; 1, green; 2, neutral after red.
	Daily Impulse: 0, red; 1, green; 2, neutral after red.
	Daily Price: 0, above value; 1, in the value zone; 2, below value - between the two ema
	MACD-H bullish divergece:
	Perfection:
	'''
	score = 0

	# Data
	stock_daily = stock(ticker, days=400)
	stock_weekly = stock(ticker, days=400, period="weekly")

	# Weekly Impulse
	stock_weekly.Impulse_System()
	score += (stock_weekly.impulse_data[-1] + 1)
	#print(score)
	
	# Daily Impulse
	stock_daily.Impulse_System()
	score += (stock_daily.impulse_data[-1] + 1)
	#print(score)

	# Daily Price
	fast_ema = stock_daily.EMA(period=22, plot_data = False)
	slow_ema = stock_daily.EMA(period=11, plot_data = False)
	#print(fast_ema[-1], slow_ema[-1], stock_daily.trade_history["Close"][-1])
	
	if stock_daily.trade_history["Close"][-1] < min(fast_ema[-1], slow_ema[-1]):
		score += 2
	elif stock_daily.trade_history["Close"][-1] > max(fast_ema[-1], slow_ema[-1]):
		score += 0
	else:
		score += 1

	# weekly MACD-H bullish divergence



	return score


if __name__ == '__main__':
	score = wsbMomentum("TSLA")
	print("Final score: ", score)