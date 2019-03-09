# Add new path
import sys
sys.path.append('C:\\Users\\Cesar Workdesk\\Documents\\Projects\\Lab-inventory\\mainCode\\')

# Build/Import libraries
from google_sheet_class import Gsheet
from stock import stock
import numpy as np
import pandas as pd

import datetime

# Constants
MAINSPREADSHEET_ID = '1wUBzSk-RY2fQC2Rri06v-ZJ6oHjwmhIIgBYVxncaUms'

# test
#history_investment = Gsheet(MAINSPREADSHEET_ID)

def Investment_data(stock_hist, Book, day_value="Close"):
	ticker  = stock_hist.ticker
	temp_array = np.zeros(len(stock_hist.trade_history.index) )
	for i in xrange(0,len(Book)):
		prev_frac = 0
		if Book.iloc[i]["Ticker"] in ticker:
			Date = Book.iloc[i].name
			Share_frac = float(Book.iloc[i]["Amount"][1:])/float(Book.iloc[i]["Share Price"][1:])
			
			j=0
			for d in stock_hist.trade_history.index:
				if d >= Date and d <= Date:
					break
				j=j+1

			#print stock_hist.trade_history["Close"][:j-1]*prev_frac
			#temp_array[j:] = stock_hist.trade_history[day_value][j:]*Share_frac + temp_array[j:]
			temp_array[j:] = Share_frac + temp_array[j:]
	temp_inv = temp_array*stock_hist.trade_history[day_value]
	
	stock_hist.trade_history[day_value +  " Investment"] = pd.Series(temp_inv, index=stock_hist.trade_history.index)

def main():

	# How to make the data from Gsheet match the data shown below
	# test
	test = Gsheet(MAINSPREADSHEET_ID)
	raw = test.get_values()

	temp = [[c for c in r] for r in raw]

	data =  np.array(temp)
	
	for i in xrange(1, len(data[1:,0])):
		print data[i,0]
		data[i,0] = datetime.datetime.strptime(data[i,0],"%m/%d/%Y")
		print data[i,0]
	
	data = np.array([['Date','Ticker','Transaction','Amount','Share Price'],
		[datetime.datetime(2017,3,13),	'AOK',	'Purchase',	'$10.00',	'$32.90'],
		[datetime.datetime(2017,3,14),	'AOK',	'Purchase',	'$20.00',	'$32.90'],
		[datetime.datetime(2017,3,14),	'SCHD',	'Purchase',	'$10.00',	'$44.90'],
		[datetime.datetime(2017,3,16),	'MGC',	'Purchase',	'$10.00',	'$81.64'],
		[datetime.datetime(2017,3,22),	'MGC',	'Purchase',	'$10.00',	'$80.60']])

	

	print ""
	print data[1:,1:]
	print data[1:,0]
	print data[0,1:]

	Book = pd.DataFrame(data=data[1:,1:],
						index=data[1:,0],
						columns=data[0,1:])

	
	
	#print Book.iloc[0]["Ticker"]
	#test = Book.iloc[0]
	#print test["Ticker"]
	print Book.index

	# Filter all Ticker and remove repetitve 
	Investment_ticker = list(set(Book['Ticker'].tolist()))

	# Get the stock data
	# Book.index[0]+datetime.timedelta(15)
	set_data = {}
	for ticker in Investment_ticker:
		temp_ETF = stock(ticker,from_date=Book.index[0]-datetime.timedelta(15),to_date=datetime.datetime.today())
		
		# Convert all the dataa tonumber of shares
		Investment_data(temp_ETF,Book)
		
		#temp_ETF.plot_line(day_value="Close Investment")


		set_data[ticker] = temp_ETF.trade_history

	total_invest_data = pd.Panel(set_data)
	
	total_invest = total_invest_data[Investment_ticker[0]]["Close Investment"]
	
	for ticker in Investment_ticker[1:]:
		total_invest = total_invest_data[ticker]["Close Investment"] + total_invest

	#print total_invest

if __name__ == '__main__':
	main()