'''
Author: Cesar Galan
date created: 2/5/2018
Function: class to get stock data from multiples parts

Todo:
1) plotting the correct date
3) work on the 

Working on:
2) being able to get more than 2000 data points for crypto

Done:


'''
# Libraries
from lxml import html  
import requests
from exceptions import ValueError
from time import sleep
import json
import argparse
from collections import OrderedDict
from time import sleep
import datetime

import pandas as pd
import pandas_datareader.data as web


# plot
from pylab import *
import matplotlib.pyplot as plt
import time
from matplotlib.dates import  DateFormatter, WeekdayLocator, HourLocator, \
     DayLocator, MONDAY, SecondLocator
from matplotlib.finance import candlestick,\
     plot_day_summary, candlestick2

class Technical_Analysis(object):
	def __init__(self, ticker=None, currency='USD', amount='2000', days=1, period=60, exchange='NASD'):
		self.ticker = ticker
		self.currency = currency
		self.amount = amount
		self.period = period
		self.days = days
		self.exchange=exchange


		self.historic_data()
		self.date_correction()
		#print self.trade_history
		self.trade_history = self.reshape_data()
		
	def date_correction(self):
		try:
			if isinstance(self.trade_history["date"][0], datetime.datetime):
				return None
		except:
			pass
		print self.trade_history
		keys = self.trade_history[0].keys()

		t0  = datetime.datetime(1970,1,1)
		timezone = datetime.timedelta(hours=6)

		FLAG = False
		for key in keys:
			if key == 'time':
				FLAG = True
				break
		#print keys

		for new_date in self.trade_history:
			if FLAG:
				dt = datetime.timedelta(seconds=new_date.pop('time'))
			else:
				dt = datetime.timedelta(seconds=new_date['date'])
			new_date['date'] = t0+dt-timezone

	def reshape_data(self):

		try:
			keys = self.trade_history[0].keys()
		except:
			keys = self.trade_history.keys()
			if len(keys) > 0:
				return self.trade_history
			else:
				raise

		temp_data = {l:[] for l in keys}

		for line in self.trade_history:
			for key_name in keys:
				try:
					temp_data[key_name].append(line[key_name])
				except:
					if (line[u'type'] == u'DIVIDEND'):
						break

		for k in keys:
			temp_data[k] = np.array(temp_data.pop(k))


		return temp_data

	def time_interval(self, interval=datetime.timedelta(seconds=1) ):
		keys = self.trade_history.keys()
		trade_interval = {k:[] for k in keys}
		
		if interval.seconds:

			if interval.seconds == 1:
				return self.trade_history

			j = interval.seconds
			L = len(self.trade_history["date"])
			for i in xrange(0, L, j):
				if (i+j) > L:
					j = L-i-1
				trade_interval["date"].append(self.trade_history["date"][i])
				trade_interval["open"].append(self.trade_history["open"][i])
				trade_interval["high"].append(max(self.trade_history["high"][i:i+j]))
				trade_interval["low"].append(min(self.trade_history["low"][i:i+j]))
				trade_interval["close"].append(self.trade_history["close"][i+j])

			return trade_interval

		elif interval.days:
			j =  interval.days*3600 
			print j

			L = len(self.trade_history["date"])
			print "Length ",L
			for i in xrange(0, L, j):
				if (i+j) > L:
					j = L-i-1

				print i, i+j
				trade_interval["date"].append(self.trade_history["date"][i])
				trade_interval["open"].append(self.trade_history["open"][i])
				trade_interval["high"].append(max(self.trade_history["high"][i:i+j]))
				trade_interval["low"].append(min(self.trade_history["low"][i:i+j]))
				trade_interval["close"].append(self.trade_history["close"][i+j])

			return trade_interval

	def support_breach(self, plot_data=True):
		breach_count = 0
		closing_price = 0
		current_support = 0
		new_high = 0
		breach_number = []

		for i in xrange(0,len(self.trade_history)-1):
			
			# New high?
			if self.trade_history[i]["close"] > new_high:
				current_support = self.trade_history[i]["close"] 
				breach_count = 0
				new_high = current_support

			# Current support
			if self.trade_history[i]["close"] < current_support:
				current_support = self.trade_history[i]["close"]
				if self.trade_history[i+1]["close"] > current_support:
					breach_count = breach_count + 1
					print "Breach Count incremented: ", breach_count


			breach_number.append(breach_count)

		return breach_number

	def RSI(self, price_use="close",time_period=14, plot_data = True):

		if (price_use != "close"): # or (price_use != "open"):
			raise Exception("price choose its not correct") 

		RSI_value = []
		for i in xrange(len(self.trade_history[price_use]),time_period,-1):
			[up_gain, down_gain] = self.price_difference(self.trade_history[price_use][(i-time_period):i])
			if not up_gain:
				RSI_value.append(0)
				continue
			if not down_gain:
				RSI_value.append(100)
				continue	

			average_gain = reduce(lambda x, y: x+y, up_gain)/len(up_gain)
			average_loss = reduce(lambda x, y: x+y, down_gain)/len(down_gain)
			RS = average_gain/(-average_loss)
			RSI_value.append(100 - 100/(1+RS))

		if plot_data:
			self.__techincal_plot(self.trade_history["date"][time_period:len(self.trade_history[price_use])], RSI_value)

		return RSI_value

	def price_difference(self, price):
		diff = []

		for i in xrange(0,len(price)-1):
			diff.append(price[i+1] - price[i])

		up_gain = []
		down_gain = []
		for data in diff:
			if data > 0:
				up_gain.append(data)
			elif data < 0:
				down_gain.append(data)

		return [up_gain, down_gain]

	def SMA(self, price="close", period=20, plot_data = True):
		sma = []
		for i in xrange(period,len(self.trade_history[price])):
			# take the average of i-period to i
			temp = reduce(lambda x, y: x+y, self.trade_history[price][i-period:i])/period

			sma.append(temp)

		if plot_data:
			self.__techincal_plot(self.trade_history["date"][time_period:len(self.trade_history[price_use])], sma)

		return sma

	def EMA(self, price="close", period=20, plot_data = True):
		sma = self.SMA(price=price, period=period, plot_data=False)
		wma = (2/(period+1))
		ema = []
		for i in xrange(period, len(self.trade_history[price])):
			ema.append( self.trade_history[price][i]-ema[i-1]*wma + ema[i-1] )

		if plot_data:
			self.__techincal_plot(self.trade_history["date"][time_period:len(self.trade_history[price_use])], ema)

		return ema

	def Bolli_Bands(self, period=20, std_multipliyer=2, plot_data=True):
		sma = self.SMA(period=period, plot_data= False)
		upper_band = sma + (np.std(sma)*std_multipliyer)
		lower_band = sma - (np.std(sma)*std_multipliyer)

		if plot_data:
			time = self.trade_history["date"][time_period:len(self.trade_history[price_use])]
			self.__techincal_plot(time, sma)
			self.__techincal_plot(time, upper_band)
			self.__techincal_plot(time, lower_bands)

		return [sma, upper_band, lower_band]

	def MACD(self,short_period = 12, long_period=26):
		short_term_ema = self.EMA(period=short_period)
		long_term_emd = self.EMA(period=long_period)

		#signal line

	def PPO(self):
		pass
		pass

	def plot(self):

		mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
		alldays    = DayLocator()              # minor ticks on the days
		minute = MinuteLocator()
		weekFormatter = DateFormatter('%b %d %H:%M:%S')  # e.g., Jan 12
		dayFormatter = DateFormatter('%d')      # e.g., 12
		fig, ax = plt.subplots()
		fig.subplots_adjust(bottom=0.2)
		#ax.xaxis.set_major_locator(mondays)
		#ax.xaxis.set_minor_locator(alldays)
		ax.xaxis.set_major_formatter(weekFormatter)
		self._candlestick(ax,
					self.trade_history["date"],
					self.trade_history["open"],
					self.trade_history["close"],
					self.trade_history["high"],
					self.trade_history["low"],
					width=0.0006, colorup="g", colordown="r")

		ax.xaxis_date()
		ax.autoscale_view()
		plt.setp( plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

		plt.show()

	def _candlestick(self,ax, date,open,close,high,low, width=0.2, colorup='k', colordown='r',
		alpha=1.0, ochl=True):
		"""
		Plot the time, open, high, low, close as a vertical line ranging
		from low to high.  Use a rectangular bar to represent the
		open-close span.  If close >= open, use colorup to color the bar,
		otherwise use colordown

		Parameters
		----------
		ax : `Axes`
			an Axes instance to plot to
		quotes : sequence of quote sequences
			data to plot.  time must be in float date format - see date2num
			(time, open, high, low, close, ...) vs
			(time, open, close, high, low, ...)
			set by `ochl`
		width : float
			fraction of a day for the rectangle width
		colorup : color
			the color of the rectangle where close >= open
		colordown : color
			the color of the rectangle where close <  open
		alpha : float
			the rectangle alpha level
		ochl: bool
			argument to select between ochl and ohlc ordering of quotes

		Returns
		-------
		ret : tuple
			returns (lines, patches) where lines is a list of lines
			added and patches is a list of the rectangle patches added

		"""

		OFFSET = width / 2.0

		lines = []
		patches = []
		l = len(date)
		for i in xrange(0,l):
			#if ochl:
			#	t, open, close, high, low = q[:5]
			#else:
			#	t, open, high, low, close = q[:5]
			dateNum = date2num(date[i])
			if close[i] >= open[i]:
				color = colorup
				lower = open[i]
				height = close[i] - open[i]
			else:
				color = colordown
				lower = close[i]
				height = open[i] - close[i]

			vline = Line2D(
				xdata=(dateNum, dateNum), ydata=(low[i], high[i]),
				color=color,
				linewidth=0.5,
				antialiased=True,
				)

			rect = Rectangle(
				xy=(dateNum - OFFSET, lower),
				width=width,
				height=height,
				facecolor=color,
				edgecolor=color,
			)
			rect.set_alpha(alpha)

			lines.append(vline)
			patches.append(rect)
			ax.add_line(vline)
			ax.add_patch(rect)
		ax.autoscale_view()

		return lines, patches

	def __techincal_plot(self, time, data):
		fig = plt.figure()
		plt.plot(time, data)
		plt.grid(True)
		plt.show()

class stock(Technical_Analysis):

	def __init__(self, ticker, period=60, days=1, exchange='NASD'):
		Technical_Analysis.__init__(self, ticker, period=period, days=days, exchange=exchange)

	def historic_data(self, period=60, days=1):
		result = web.DataReader('AAPL', 'yahoo', '2017-01-01', '2018-01-01')

	def historic_data_google(self, period=60, days=1, exchange='NASD'):
		url = 'https://finance.google.com/finance/getprices' + \
			'?p={days}d&f=d,o,h,l,c,v&q={ticker}&i={period}&x={exchange}'.format(ticker=self.ticker, 
																					period=self.period, 
																					days=self.days,
																					exchange=self.exchange)

		response = requests.get(url)
		content = response.content.splitlines()
		print content 

		date = []
		opend = []
		closed = []
		highd = []
		lowd = []
		volume = []

		t0  = datetime.datetime(1970,1,1)

		#print content
		for line in content:
			split = line.split(",")
			if len(split) == 6:
				if 'COLUMNS' in split[0]:
					continue

				if 'a' in split[0]:
					dt = datetime.timedelta(seconds=int(split[0].replace('a','')))
					date.append(t0 + dt)
				else:
					date.append(t0 + dt + datetime.timedelta(minutes=float(split[0])))
				opend.append(float(split[4]))
				closed.append(float(split[1]))
				highd.append(float(split[2]))
				lowd.append(float(split[3]))
				volume.append(int(split[5]))
	
		
		self.trade_history = {"date":date,"open":opend,"close":closed,"high":highd, "low":lowd, "volume":volume}
		#print self.trade_history

	def historic_data_yahoo(self):
		url = "http://finance.yahoo.com/quote/%s/history?p=%s"%(self.ticker,self.ticker)
		response = requests.get(url)
		html = response.content
		self.trade_history = self.html2data(html)
		#print self.trade_history
		#self.trade_history = self.reshape_data(temp_data)
		#self.data_lenght = len(self.historic["date"])
		#print self.data_lenght

	def html2data(self, html):
		Ibegin = html.find("HistoricalPriceStore") + len("HistoricalPriceStore") + 12
		Iend = html.find("isPending") - 2
		try:
			data = json.loads(html[Ibegin:Iend])
		except:
			print "broken self"
			raise

		return data

class cryptocurrency(Technical_Analysis):
	def __init__(self, ticker, currency='USD', amount='2000'):
		Technical_Analysis.__init__(self, ticker, currency=currency, amount=amount)

	def historic_data(self):
		url = "https://min-api.cryptocompare.com/data/histominute" +\
		"?fsym=%s"%(self.ticker) +\
		"&tsym=%s"%(self.currency) +\
		"&limit=%s"%(self.amount) +\
		"&aggregate=1" 
		#"&toTs"

		response = requests.get(url)

		self.trade_history = response.json()['Data']

		
		for i in xrange(1,int(self.amount)/2000):
			url = "https://min-api.cryptocompare.com/data/histominute" +\
			"?fsym=%s"%(self.ticker) +\
			"&tsym=%s"%(self.currency) +\
			"&limit=%s"%(self.amount) +\
			"&aggregate=1" +\
			"&toTs=%s"%(self.trade_history[0]["time"])

			response = requests.get(url)

			temp = response.json()['Data']

			for data in self.trade_history:
				temp.append(data)

			
			self.trade_history = temp

		if (float(self.amount)/2000.0 - int(self.amount)/2000):
			rest = int((float(self.amount)/2000.0 - int(self.amount)/2000)*2000)
			url = "https://min-api.cryptocompare.com/data/histominute" +\
			"?fsym=%s"%(self.ticker) +\
			"&tsym=%s"%(self.currency) +\
			"&limit=%s"%(rest) +\
			"&aggregate=1" +\
			"&toTs=%s"%(self.trade_history[0]["time"])

			response = requests.get(url)

			temp = response.json()['Data']

			for data in self.trade_history:
				temp.append(data)

			self.trade_history = temp


########### Test Cases ##############
def testStockProperties():
	ticker = 'ITA'
	print "Fetching data for %s"%(ticker)
	scraped_data = ETF_parse(ticker)
	print "Writing data to output file"
	print "Data: ", scraped_data 

def historicTest():
	#ticker = 'ITA'
	ticker = 'AAPL'
	apple_data = historic_stock(ticker)
	#print apple_data 

def classTest():
	#ticker = 'ITA'
	ticker = 'AAPL'
	apple_stock = stock(ticker)
	apple_stock.RSI()

def supTest():
	ticker = 'AAPL'
	apple_stock = stock(ticker)
	apple_stock.support_breach()

def parent_classes():
	# stock
	TTMI = stock('ITA')
	#print TTMI.trade_history
	TTMI.plot()
	#TTMI.RSI()
	#crypto
	#ETH = cryptocurrency('ETH', amount='7000')
	#print ETH.trade_history["date"]

	#print "ETH: ", ETH.trade_history["date"]
	#print ETH.time_interval(datetime.timedelta(days=1))
	#ETH.plot()

def other_test():
	

	result = web.DataReader('AAPL', 'yahoo', '2017-01-01', '2018-01-01')
	print result


	
if __name__=="__main__":
	#parent_classes()
	other_test()




'''
import requests
url = 'https://min-api.cryptocompare.com/data/histominute' +\
        '?fsym=ETH' +\
        '&tsym=USD' +\
        '&limit=2000' +\
        '&aggregate=1'
response = requests.get(url)
data = response.json()['Data']

import pandas as pd
df = pd.DataFrame(data)
print(df)




class stock_yahoo():
	def __init__(self, ticker):
		self.ticker = ticker
		self.historic_stock()

	def historic_stock(self):
		url = "http://finance.yahoo.com/quote/%s/history?p=%s"%(self.ticker,self.ticker)
		response = requests.get(url)
		html = response.content
		temp_data = self.html2data(html)
		self.historic = self.reshape_data(temp_data)
		self.data_lenght = len(self.historic["date"])
		print self.data_lenght
		#print self.data_lenght
		#for dateline in self.historic["date"]: 
		#print self.historic["date"]

	def reshape_data(self, data):
		temp_volume = []
		temp_high = []
		temp_adjclose = []
		temp_low = []
		temp_date = []
		temp_close = []
		temp_open = []

		t0  = datetime.datetime(1970,1,1)

		for line in data:
			try:
				if not line["volume"] or not line["high"] or not line["adjclose"] or not line["low"] or not line["close"] or not line["open"]:
					continue

				temp_volume.append(line["volume"])
				temp_high.append(line["high"])
				temp_adjclose.append(line["adjclose"])
				temp_low.append(line["low"])
				temp_close.append(line["close"])
				temp_open.append(line["open"])
			except:
				continue

			dt = datetime.timedelta(seconds=line["date"])
			temp_date.append(t0+dt)

		temp_data = {"volume":temp_volume,
					"high":temp_high,
					"adjclose":temp_adjclose,
					"low":temp_low,
					"close":temp_close,
					"open":temp_open,
					"date":temp_date
					}
		return temp_data

	def html2data(self, html):
		Ibegin = html.find("HistoricalPriceStore") + len("HistoricalPriceStore") + 12
		Iend = html.find("isPending") - 2
		try:
			data = json.loads(html[Ibegin:Iend])
		except:
			print "broken self"
			raise

		return data

	def convert_date(self, data):
		t0  = datetime.date(1970,1,1)
		for day_trade in data:
			dt = datetime.timedelta(days=day_trade["date"]/86400)
			day_trade["date"] = t0 + dt
		return data

	


	def investment_return(self, average_price):
		percent_return = []
		return_investment = []
		try:
			for j in xrange(0,self.data_lenght):
				percent_return.append(((self.historic["close"][j] - average_price)/average_price)*100)
				return_investment.append((percent_return[j]/100)*average_price)
		except:
			print "length: ", self.data_lenght
			for i in xrange(0,self.data_lenght): 
				print self.historic["date"][i], self.historic["close"][i]
			raise

		return [return_investment, percent_return]
'''