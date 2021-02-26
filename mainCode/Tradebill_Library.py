


# Libraries
from stock import stock
import numpy as np

import matplotlib.pyplot 		as plt

def wsbMomentum(ticker,n_days=400,fEMA_period=22,sEMA_period=11,ema_IS=13, fast_ema_IS=12, slow_ema_IS=26, `signal_IS=9):
	'''
	Weekly Impulse: 0, red; 1, green; 2, neutral after red.
	Daily Impulse: 0, red; 1, green; 2, neutral after red.
	Daily Price: 0, above value; 1, in the value zone; 2, below value - between the two ema
	MACD-H bullish divergece:
	Perfection:
	'''
	score = 0

	# Data
	stock_daily = stock(ticker, days=n_days)
	stock_weekly = stock(ticker, days=n_days, period="weekly")

	# Weekly Impulse
	stock_weekly.Impulse_System(plot_data=False)
	score += (stock_weekly.impulse_data[-1] + 1)
	
	# Daily Impulse
	stock_daily.Impulse_System(plot_data=False)
	score += (stock_daily.impulse_data[-1] + 1)


	# Daily Price
	fast_ema = stock_daily.EMA(period=fEMA_period, plot_data = False)
	slow_ema = stock_daily.EMA(period=sEMA_period, plot_data = False)
		
	if stock_daily.trade_history["Close"][-1] < min(fast_ema[-1], slow_ema[-1]):
		score += 2
	elif stock_daily.trade_history["Close"][-1] > max(fast_ema[-1], slow_ema[-1]):
		score += 0
	else:
		score += 1
	
	# weekly MACD-H bullish divergence
	stock_weekly.MACD()
	signal = 9
	offset = len(stock_weekly.trade_history.index)-len(stock_weekly.MACD_line)-1+signal
	dHist = np.diff(stock_weekly.MACD_histogram)
	
	prev_s = 0
	local_minMax = []
	for i, s in enumerate(np.sign(dHist)):
		if s != prev_s:
			local_minMax.append(i)#=offset for date
			prev_s = s

	bar_high = stock_weekly.MACD_histogram[local_minMax[-4:-1]]
	if bar_high[0] < 0 and bar_high[1] > 0 and bar_high[2] < 0:
		score += 1
		if bar_high[0] > bar_high[2]:
			score += 1

	
	# Perfection
	if (stock_daily.trade_history["Close"][-1] - stock_daily.trade_history["Close"][-2]) > 0:
		score += 1

	if (stock_weekly.trade_history["Close"][-1] - stock_weekly.trade_history["Close"][-2]) > 0:
		score += 1

	return score

def channelTrade(ticker):
	'''
	Possible systems
		ATR use to check the true value
		RSI use to confirm the undervalue price. +1 if <50, +2 <35.
		SI
		EMA
	'''
	print("a")

if __name__ == '__main__':
	score = wsbMomentum("GME")
	print("Final score: ", score)
	#plt.show()