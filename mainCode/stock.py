'''
Author: Cesar Galan
date created: 2/5/2018
Function: class to get stock data and crypto from multiples places


Todo:
1) plotting the correct date
3) Add import EDGAR


Working on:
2) being able to get more than 2000 data points for crypto
'''
'''
Goal is to extract 
	Valuations measures
		Market Cap - Done
		Enterprise Value - Done
		Trailing P/E 			- To work on
		Foward P/E 				- To work on
		PEG Ratio 				- To work on
		Price/Sales 			- To work on
		Price/Book 				- To work on
		Enterprise Value/Revenue - Done
		Enterprise Value/EBITDA - To work on - Developt EBITDA first 
		ROTS 					- To work on
		Book Value - Done

	Financials
		Profit Margin				- To work on, might be on balance sheet
		Operating Margin			- To work on, might be on balance sheet
		Return on assets
		Return on Equity
		Revenue - Income statement
		Revenue Per share
		Quaterly Revenue Growth 	
		Gross Profit
		EBITDA 						- To work on
		Net Income Avi to Common
		Dilute EPS
		Quaterly Earnings Growth
		Total Cash 
		Total Cash Per Share
		Total Debt
		Total Debt/Equity
		Current Ratio
		Book Value per share - Done
		Operating Cash Flow
		Levered Free Cash Flow
		EPS - Done
		TTM 						- To work on

	Trading informations
		Beta
		50-Day Moving Average
		200 DayMoving Average
		Avg Vol (3Month)
		Shares Outstanding 			- last quaterly report - Done
		Float
		% Held by Insiders
		% Held by institutions
		Shares Shorts
		Short Ratio
		Short% of Float
		Shares Shorts (Prior Month)
'''

# Libraries
import requests
import json
import argparse
import datetime
import time
import itertools
import numpy

from lxml import html  
from exceptions import ValueError
from time import sleep
from collections import OrderedDict
from time import sleep
from yahoofinancials import YahooFinancials

# Libraries with different names
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt

# plot
from pylab import *
from matplotlib.dates import  DateFormatter, WeekdayLocator, HourLocator, \
     DayLocator, MONDAY, SecondLocator
# from matplotlib.finance     
#from mpl_finance import candlestick2, plot_day_summary, candlestick2

class Fundamental_Analysis(object):
	# Create valuations, Financial and Trading information for pandas
	def __init__(self, ticker):
		'''
		'''
		self.fundamentals = YahooFinancials(ticker)

	def balance(self, timeline='annual'):
		self.balance_stmts = self.__statements(timeline, 'balance')
		return self.balance_stmts

	def income(self, timeline='annual'):
		self.income_stmts = self.__statements(timeline, 'income')
		return self.income_stmts

	def cash(self, timeline='annual'):
		self.cash_stmts = self.__statements(timeline, 'cash')
		return self.cash_stmts

	def earnings(self):
		'''
		'''
		raise Exception("To be developt")

	def outstandingShares(self):
		self.outstanding_shares = self.fundamentals.get_num_shares_outstanding()
		return self.outstanding_shares

	def marketCap(self):
		'''
		get market cap through yahoo,

		TODO: Calculate your own 
		'''
		self.market_cap = self.fundamentals.get_market_cap()
		return self.market_cap

	'''
	################# Information Derived from statements ####################
	'''
	'''
	### Valuations ####
	'''
	def EVperRevenue(self):
		'''
		Enterprise Value per revenue: 
		'''
		# Check if data has being loaded
		self.__createValuationMetrics()
		self.__createIncomeMetrics()
		
		# check if statemnts values exists
		if not self.__missingStatementInformation(self.valuations,"EV"):
			self.enterpriseValue()

		# Calculate
		#print self.income_stmts["totalRevenue"]
		ev_revenue =[]
		for total_revenue, EV in itertools.izip(self.income_stmts["totalRevenue"], self.valuations["EV"]):
			ev_revenue.append(EV/total_revenue)

		self.valuations["ev_revenue"] = ev_revenue

		return ev_revenue

	def priceBookValue(self):
		self.__createValuationMetrics()
		self.__createMarketCap()

		# Check statement values exists
		if not self.__missingStatementInformation(self.valuations,"book value"):
			self.bookValue()

		PB = []
		for book  in self.valuations["book value"]:
			PB.append(self.market_cap/book)

		self.valuations["PB"] = PB
		return PB

	def enterpriseValue(self):
		'''
		Enterprise Value: How much would it cost to buy the company outright

		Link: https://www.investopedia.com/terms/e/enterprisevalue.asp
		'''
		# Check if data has being loaded
		self.__createValuationMetrics()
		self.__createMarketCap()
		self.__createBalance()
		self.__checkpdIndex(self.valuations, self.balance_stmts.index)

		# check if statemnts values exists
		self.__missingStatementInformation(self.balance_stmts,"shortLongTermDebt")
		self.__missingStatementInformation(self.balance_stmts,"longTermDebt")
		self.__missingStatementInformation(self.balance_stmts,"cash")

		EV = []
		for shortDebt, longDebt, cash_equivalents in itertools.izip(self.balance_stmts["shortLongTermDebt"], self.balance_stmts["longTermDebt"],self.balance_stmts["cash"]):
			total_debt = shortDebt + longDebt
			EV.append(self.market_cap + total_debt - cash_equivalents)

		self.valuations["EV"] = EV
		return EV

	def trailingPE(self):
		'''
		trailing Price Earning ratio
		'''
		raise Exception("To be developt")
		pass

	def fowardPE(self):
		'''
		foward PE ratio
		'''

		raise Exception("To be developt")

	def bookValue(self):
		'''
		book value: tangable assets minus liabilities
		Tangable assets define as total assets minus intangable assets

		Assuptions: Current outstanding shares are the same througout the years

		https://www.investopedia.com/terms/b/bookvalue.asp
		'''
		# Check if the data has being loaded
		self.__createBalance()
		self.__createValuationMetrics()
		self.__createOutstandShMetrics()
		self.__checkpdIndex(self.valuations, self.balance_stmts.index)

		book_value = []
		book_value_per_share = []
		for total_assets, intangible_assets, total_liability in itertools.izip(self.balance_stmts["totalAssets"],self.balance_stmts["intangibleAssets"],self.balance_stmts["totalLiab"]):
			tangable_assets = total_assets - intangible_assets
			book_value.append(tangable_assets - total_liability)
			book_value_per_share.append((tangable_assets - total_liability)/self.outstanding_shares)

		self.valuations["book value"] = book_value
		self.valuations["book value per share"] = book_value_per_share

		return [book_value, book_value_per_share]

	def PEG(self):
		'''
		'''
		raise Exception("To be developt")

	def priceSalesRatio(self):
		'''
		price to sales ratio

		Needs to find Sales number
		'''
		# Check pandas dataframe exist
		'''
		self.__createValuationMetrics()
		self.__

		self.__downloadBalanceStockInformation(self.balance_stmts)
		'''
		raise Exception("To be developt")

	def priceBookRatio(self):
		'''
		price to book ratio: define as the 
		'''
		#raise Exception("To be developt")
		self.__createValuationMetrics()

		if not self.__missingStatementInformation(self.valuations, "book value per share"):
			self.bookValue()

		self.__downloadBalanceStockInformation(self.balance_stmts)

		

	def enterpriseEBITDA(self):
		'''
		'''
		raise Exception("To be developt")

		# 
		self.__missingStatementInformation(self.valuation, "EV")
		self.__missingStatementInformation(self.financial, "EBITDA")

	def ROTS(self):
		'''
		'''
		raise Exception("To be developt")

	'''
	### Financials ####
	'''
	def EPS(self):
		'''
		EPS: Earnings per shares 

		link: https://www.fool.com/knowledge-center/how-to-calculate-earnings-per-share-on-a-balance-s.aspx
		'''
		# Check if the data has being loaded
		self.__createIncomeMetrics()
		self.__createOutstandShMetrics()
		self.__createCashMetrics()
		self.__createFinancialMetrics()
		self.__checkpdIndex(self.financial, self.income_stmts.index)

		# Check statement values exists
		self.__missingStatementInformation(self.cash_stmts,"dividendsPaid")
		self.__missingStatementInformation(self.income_stmts,"netIncome")

		EPS = []
		
		for net_income, dividends in itertools.izip(self.income_stmts["netIncome"], self.cash_stmts["dividendsPaid"]):
			total_earnings = net_income+dividends
			EPS.append(total_earnings/self.outstanding_shares)

		self.financial["EPS"] = EPS

		return EPS

	def EBITDA(self):
		'''
		No clue what this is
		'''
		raise Exception("To be Developt")

	def TTM(self):
		'''
		'''
		raise Exception("To be developt")

	'''
	### Trading ####
	'''
	def beta(self):
		'''
		'''
		raise Exception("To be Developt")

	'''
	### Private Functions ###
	'''
	def __createOutstandShMetrics(self):
		try:
			self.outstanding_shares
		except AttributeError:
			self.outstandingShares()

	def __createMarketCap(self):
		try:
			self.market_cap
		except AttributeError:
			self.marketCap()

	def __createIncomeMetrics(self):
		try:
			self.income_stmts
		except AttributeError:
			self.income()

	def __createCashMetrics(self):
		try:
			self.cash_stmts
		except AttributeError:
			self.cash()

	def __createBalance(self):
		try:
			self.balance_stmts
		except AttributeError:
			self.balance()

	def __createValuationMetrics(self):
		try:
			self.valuations
		except AttributeError:
			self.valuations = pd.DataFrame()

	def __createFinancialMetrics(self):
		try:
			self.financial
		except AttributeError:
			self.financial = pd.DataFrame()

	def __statements(self, timeline, type_stmts):
		if "annual" in timeline or "quarterly" in timeline:
			raw = self.fundamentals.get_financial_stmts(timeline, type_stmts)
			stmts = self.__raw2pd(raw[raw.keys()[0]])
			return stmts

		else:
			print("The timeline is not define correctly")

	def __raw2pd(self,raw_data):
		# Get all the list dont repeat
		key_list = []
		for sheet in raw_data[self.ticker]:
			key = sheet.values()[0].keys()

			tmp_list = list(set(key) - set(key_list))
			key_list.extend(tmp_list)
		

		# Split the data for pd
		date_index = []
		data_pd = []
		for sheet in raw_data[self.ticker]:
			date_temp = sheet.keys()[0]
			
			date_index.append(date_temp)
			temp_data = []
			for tempKey in key_list:
				try:
					temp_data.append(sheet[date_temp][tempKey])
				except KeyError:
					temp_data.append(None)
			data_pd.append(temp_data)

		return pd.DataFrame(data=data_pd,
					 index=date_index,
					 columns=key_list)

	def __checkpdIndex(self, pd_frame, index):
		if pd_frame.empty:
			pd_frame["date"] = index
			pd_frame.set_index('date', inplace=True)
			return True

		return False

	def __missingStatementInformation(self, statement, colmn):
		'''
		This is used to check if the information exist already in the pandas data frame
		'''
		try:
			statement[colmn]
			return True
		except KeyError:
			statement[colmn] = 0
			return False

	def __downloadBalanceStockInformation(self, Q_sheet):
		'''
		Create it to download the day trade of the balance sheet
		Todo test what is fastest Individual download or full download and the parse it
		''' 
		#raise Exception("To be Developt")
		print Q_sheet.index

		self._statementsTrade(Q_sheet.index)

		# Download the data

		# Store it in the balance dataframe

class Technical_Analysis(object):
	def __init__(self, ticker=None, currency='USD', amount='2000', days=1, period=60, exchange='NASD', from_date=None, end_date=None):
		self.ticker = ticker
		self.currency = currency
		self.amount = amount
		self.period = period
		self.days = days
		self.exchange=exchange

		if not from_date:
			self.historic_data(ticker, period=period)
		else:
			self.historic_data(ticker, from_date=from_date, to_date=end_date)

		#self.date_correction()
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

	def plot_line(self, day_value="Close"):
		weekFormatter = DateFormatter('%b %d %H:%M:%S')
		fig, ax = plt.subplots()
		fig.subplots_adjust(bottom=0.2)
		ax.xaxis.set_major_formatter(weekFormatter)
		plt.plot(self.trade_history.index,self.trade_history[day_value])
		#fig.subplots_adjust()
		ax.xaxis_date()
		ax.autoscale_view()
		plt.title(self.ticker)
		plt.setp( plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

		plt.show()
		
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
					self.trade_history.index,
					self.trade_history["Open"],
					self.trade_history["Close"],
					self.trade_history["High"],
					self.trade_history["Low"],
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

class stock(Technical_Analysis,Fundamental_Analysis):

	def __init__(self, ticker, period=60, days=30, exchange='NASD', from_date=None, to_date=None):
		Technical_Analysis.__init__(self, ticker, period=period, days=days, exchange=exchange, from_date=from_date, end_date=to_date)
		Fundamental_Analysis.__init__(self, ticker)

	def historic_data(self,ticker, period=60, days=1, from_date=None, to_date=None):
		
		if not from_date:
			today = datetime.datetime.today()
			start_date = today-datetime.timedelta(period)
			self.trade_history = web.DataReader(ticker, 'yahoo', start_date, today)
		else:
			self.trade_history = web.DataReader(ticker, 'yahoo', from_date, to_date)

	def _statementsTrade(self, Q_dates):
		# 
		Qtrade = pd.DataFrame()
		#print Qtrade
		#print Q_dates
		#print isinstance(datetime.datetime.strptime(Q_dates[2],"%Y-%m-%d"),datetime.datetime)
		#a = datetime.datetime.strptime(Q_dates[2],"%Y-%m-%d") + datetime.timedelta(2)
		hist = web.DataReader(self.ticker, 'yahoo', Q_dates[-1], Q_dates[0])
		print hist[datetime.datetime.strptime(Q_dates[2],"%Y-%m-%d")]
		'''
		for qD, x in Q_dates.iterrows():
			print "date check", qD
			t = web.DataReader(self.ticker, 'yahoo', qD, qD)
			print t

		'''

		return Qtrade
		

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
	AOK = stock('BRK-B')
	#print ITA.trade_history.index[0]
	#print TTMI.trade_history
	AOK.plot_line()
	#TTMI.RSI()
	#crypto
	#ETH = cryptocurrency('ETH', amount='7000')
	#print ETH.trade_history["date"]

	#print "ETH: ", ETH.trade_history["date"]
	#print ETH.time_interval(datetime.timedelta(days=1))
	#ETH.plot()

def other_test():
	result = web.DataReader('AAPL', 'yahoo', '2018-01-01', '2019-01-01')
	print result

def fundamental_test():
	ticker =  "SPOT"
	TRL = stock(ticker)	
	#print TRL.balance()
	#print TRL.income()
	#print TRL.cash()
	#print TRL.cash_stmts.columns
	#print TRL.cash('quarterly')
	#print TRL.EPS()
	#print TRL.bookValue()
	#print TRL.marketCap()
	#print TRL.enterpriseValue()
	#print TRL.priceBookValue()
	#print TRL.EVRevenue()
	#print TRL.priceSalesRatio()
	print TRL.priceBookRatio()

	#print TRL.valuations
	#print TRL.trade_history

if __name__=="__main__":
	#parent_classes()
	#other_test()
	fundamental_test()

