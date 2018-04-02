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

 
class stock():
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

		t0  = datetime.date(1970,1,1)

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

			dt = datetime.timedelta(days=line["date"]/86400)
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

	def plot(self):
		fig = plt.figure()
		ax1 = plt.subplot2grid((6,1), (0,0), rowspan=6, colspan=1)
		ax1.xaxis_date()

		plt_candle(ax1, self.historic, width=1, colorup='g', colordown='k', alpha=0.75)

		#plt_candle(self)
		#plt.plot(self.historic["date"], self.historic["close"])
		plt.grid(True)
		plt.show()


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


	def RSI(self, price_use="close",time_period=12, plot_data = True):

		if (price_use != "close"): # or (price_use != "open"):
			raise Exception("price choose its not correct") 

		RSI_value = []
		for i in xrange(self.data_lenght,time_period,-1):
			[up_gain, down_gain] = self.price_difference(self.historic[price_use][(i-time_period):i])
			average_gain = reduce(lambda x,y:x+y,up_gain)/len(up_gain)
			average_loss = reduce(lambda x,y:x+y,down_gain)/len(down_gain)
			RS = average_gain/(-average_loss)
			RSI_value.append(100 - 100/(1+RS))

		if plot_data:
			fig = plt.figure()
			plt.plot(self.historic["date"][time_period:self.data_lenght], RSI_value)
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

if __name__=="__main__":
	#testStockProperties()
	#historicTest()
    classTest()


'''
def ETF_parse(ticker):
	url = "http://finance.yahoo.com/quote/%s?p=%s"%(ticker,ticker)
	response = requests.get(url)
	#print "Parsing %s"%(url)
	sleep(4)
	parser = html.fromstring(response.text)

	summary_table = parser.xpath('//div[contains(@data-test,"summary-table")]//tr')
	summary_data = OrderedDict()
	other_details_json_link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com".format(ticker)
	summary_json_response = requests.get(other_details_json_link)
	YTR = None
	beta3Y = None
	yearAvgReturn5 = None
	yearAvgReturn3 = None
	try:
		json_loaded_summary =  json.loads(summary_json_response.text)
		#print "json: ", json_loaded_summary#["quoteSummary"]["result"][0]["defaultKeyStatistics"]
		YTR = json_loaded_summary["quoteSummary"]["result"][0]["defaultKeyStatistics"]['ytdReturn']['raw']
		beta3Y = json_loaded_summary["quoteSummary"]["result"][0]["defaultKeyStatistics"]['beta3Year']['raw']
		try:
			yearAvgReturn3 = json_loaded_summary["quoteSummary"]["result"][0]["defaultKeyStatistics"]["threeYearAverageReturn"]['raw']*100
			yearAvgReturn5 = json_loaded_summary["quoteSummary"]["result"][0]["defaultKeyStatistics"]["fiveYearAverageReturn"]['raw']*100
		except:
			pass
		yield_stock = json_loaded_summary["quoteSummary"]["result"][0]["defaultKeyStatistics"]["yield"]['raw']		
		summary_data.update({'YTD return':YTR,'beta 3Y':beta3Y,'Avg return per 5 year':yearAvgReturn5,'Avg return per 3 year':yearAvgReturn3,'yield':yield_stock,'ticker':ticker,'url':url})
		return summary_data
	except ValueError:
		print "Failed to parse json response"
		return {"error":"Failed to parse json response"}

def parse(ticker):
	url = "http://finance.yahoo.com/quote/%s?p=%s"%(ticker,ticker)
	response = requests.get(url)
	print "Parsing %s"%(url)
	sleep(4)
	parser = html.fromstring(response.text)
	summary_table = parser.xpath('//div[contains(@data-test,"summary-table")]//tr')
	summary_data = OrderedDict()
	other_details_json_link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com".format(ticker)
	summary_json_response = requests.get(other_details_json_link)
	try:
		json_loaded_summary =  json.loads(summary_json_response.text)
		y_Target_Est = json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["targetMeanPrice"]['raw']
		earnings_list = json_loaded_summary["quoteSummary"]["result"][0]["calendarEvents"]['earnings']
		eps = json_loaded_summary["quoteSummary"]["result"][0]["defaultKeyStatistics"]["trailingEps"]['raw']
		datelist = []
		for i in earnings_list['earningsDate']:
			datelist.append(i['fmt'])
		earnings_date = ' to '.join(datelist)
		for table_data in summary_table:
			raw_table_key = table_data.xpath('.//td[contains(@class,"C(black)")]//text()')
			raw_table_value = table_data.xpath('.//td[contains(@class,"Ta(end)")]//text()')
			table_key = ''.join(raw_table_key).strip()
			table_value = ''.join(raw_table_value).strip()
			summary_data.update({table_key:table_value})
		summary_data.update({'1y Target Est':y_Target_Est,'EPS (TTM)':eps,'Earnings Date':earnings_date,'ticker':ticker,'url':url})
		return summary_data
	except ValueError:
		print "Failed to parse json response"
		return {"error":"Failed to parse json response"}
'''