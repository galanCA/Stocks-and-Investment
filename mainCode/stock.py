'''
Author: Cesar Galan
date created: 2/5/2018
Function: class to get stock data from multiples parts

Todo:
1) add more places to get the data such as pandas_datareader.data

'''

from lxml import html  
import requests
from exceptions import ValueError
from time import sleep
import json
import argparse
from collections import OrderedDict
from time import sleep
import datetime
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc as plt_candle

class Technical_Analysis(object):
	def __init__(self, ticker=None, currency='USD', amount='2000'):
		self.ticker = ticker
		self.currency = currency
		self.amount = amount

		self.historic_data()
		self.date_correction()
		#print self.trade_history
		self.trade_history = self.reshape_data()
		


	def date_correction(self):
		t0  = datetime.datetime(1970,1,1)

		keys = self.trade_history[0].keys()

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
			new_date['date'] = t0+dt

	def reshape_data(self):
		keys = self.trade_history[0].keys()

		temp_data = {l:[] for l in keys}

		for line in self.trade_history:
			for key_name in keys:
				try:
					temp_data[key_name].append(line[key_name])
				except:
					if (line[u'type'] == u'DIVIDEND'):
						break

		return temp_data

	def support_breach(self):
		breach_count = 0
		closing_price = 0
		current_support = 0
		new_high = 0

		for i in xrange(0,len(self.trade_history)-1):
			
			#print "closing price", self.trade_history[i]["close"]
			
			# New high?
			if self.trade_history[i]["close"] > new_high:
				current_support = self.trade_history[i]["close"] 
				breach_count = 0
				new_high = current_support
				#print "New High ", new_high

			#else:
				#print "No New high"

			# Current support
			if self.trade_history[i]["close"] < current_support:
				current_support = self.trade_history[i]["close"]
				#print "Current support ", current_support
				if self.trade_history[i+1]["close"] > current_support:
					breach_count = breach_count + 1
					print "Breach Count incremented: ", breach_count

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
			fig = plt.figure()
			plt.plot(self.trade_history["time"][time_period:len(self.trade_history[price_use])], RSI_value)
			plt.grid(True)
			plt.show()

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

	def plot(self):
		fig = plt.figure()
		ax1 = plt.subplot2grid((6,1), (0,0), rowspan=6, colspan=1)
		ax1.xaxis_date()


		plt_candle(ax1, self.trade_history, width=1) #colorup='g', colordown='k', alpha=0.75)

		#plt_candle(self)
		#plt.plot(self.historic["date"], self.historic["close"])
		plt.grid(True)
		plt.show()


class stock(Technical_Analysis):

	def __init__(self, ticker):
		Technical_Analysis.__init__(self, ticker)

	def historic_data(self):
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

class cryptocurrency(Technical_Analysis):
	def __init__(self, ticker):
		Technical_Analysis.__init__(self, ticker)

	def historic_data(self):
		url = "https://min-api.cryptocompare.com/data/histominute" +\
		"?fsym=%s"%(self.ticker) +\
		"&tsym=%s"%(self.currency) +\
		"&limit=%s"%(self.amount) +\
		"&aggregate=1" 

		response = requests.get(url)

		self.trade_history = response.json()['Data']
		#self.timeTo = self.trade_history['TimeTo']




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
	ETH = cryptocurrency('ETH')
	print "ETH: ", ETH.trade_history
	
	F = stock('F')
	print "F: ", F.trade_history

	AAPL = stock('AAPL')
	print "AAPL: ",AAPL.trade_history

if __name__=="__main__":
	#testStockProperties()
	#historicTest()
    #supTest()
    parent_classes()




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
'''