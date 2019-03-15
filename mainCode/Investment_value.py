# Add new path
import sys
sys.path.append('C:\\Users\\Cesar Workdesk\\Documents\\Projects\\Lab-inventory\\mainCode\\')

# Build/Import libraries
from google_sheet_class import Gsheet
from stock import stock
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import  DateFormatter, WeekdayLocator, HourLocator, \
     DayLocator, MONDAY, SecondLocator
from re import sub
from decimal import Decimal


# Constants
MAINSPREADSHEET_ID = '1wUBzSk-RY2fQC2Rri06v-ZJ6oHjwmhIIgBYVxncaUms'

# test
#history_investment = Gsheet(MAINSPREADSHEET_ID)

def Investment_data(stock_hist, Book, day_value="Close"):
	ticker  = stock_hist.ticker
	#print len(stock_hist.trade_history.index)
	temp_array = np.zeros(len(stock_hist.trade_history.index) )
	for i in xrange(0,len(Book)):
		prev_frac = 0
		if Book.iloc[i]["Ticker"] in ticker:
			#print Book.iloc[i]["Transaction"]
			if "Sale" in Book.iloc[i]["Transaction"]:
				continue
				#print Book.iloc[i]["Transaction"]
				Share_frac = -float(sub(r'[^\d.]', '', Book.iloc[i]["Amount"][1:]))/float(sub(r'[^\d.]', '', Book.iloc[i]["Share Price"][1:]))
			elif "Purchase" in Book.iloc[i]["Transaction"]:
				Date = Book.iloc[i].name

				Share_frac = float(sub(r'[^\d.]', '', Book.iloc[i]["Amount"][1:]))/float(sub(r'[^\d.]', '', Book.iloc[i]["Share Price"][1:]))	
				j=0
				for d in stock_hist.trade_history.index:
					if d >= Date and d <= Date:
						break
					j=j+1
				if len(stock_hist.trade_history.index) == j:
					j = 0
					for d in stock_hist.trade_history.index:
						if (d >= Date+ datetime.timedelta(1) and d <= Date+ datetime.timedelta(1)) or (d >= Date+ datetime.timedelta(2) and d <= Date+ datetime.timedelta(2)):
							break
						j=j+1

			temp_array[j:] = Share_frac + temp_array[j:]

	temp_inv = temp_array*stock_hist.trade_history[day_value]
	
	stock_hist.trade_history[day_value +  " Investment"] = pd.Series(temp_inv, index=stock_hist.trade_history.index)

def main():

	# Extract the data from g sheets
	test = Gsheet(MAINSPREADSHEET_ID)
	raw = test.get_values()

	# convert the data to list 
	temp = [[c.encode() for c in r] for r in raw]

	# convert all the string date into datetime class
	for i in xrange(1, len(temp)):
		temp[i][0] = datetime.datetime.strptime(temp[i][0],"%m/%d/%Y")

	# convert list into numpy
	data =  np.array(temp)#.astype(str)

	# Convert numpy into pandas
	Book = pd.DataFrame(data=data[1:,1:],
						index=data[1:,0],
						columns=data[0,1:])

	# Filter all Ticker and remove repetitve 
	Investment_ticker = list(set(Book['Ticker'].tolist()))

	# Get the stock data
	# Book.index[0]+datetime.timedelta(15)
	#print Investment_ticker
	set_data = {}
	print "Loading stock history"
	for ticker in Investment_ticker:
		print ticker
		temp_ETF = stock(ticker,from_date=Book.index[0],to_date=datetime.datetime.today())
		

		# Convert all the dataa tonumber of shares
		Investment_data(temp_ETF,Book)
		
		#temp_ETF.plot_line(day_value="Close")
		set_data[ticker] = temp_ETF.trade_history
		#print temp_ETF.trade_history


	total_invest_data = pd.Panel(set_data)
	
	# set up total_invest data structure
	#print total_invest_data[Investment_ticker[2]]["Close Investment"]
	total_invest = total_invest_data[Investment_ticker[0]]["Close Investment"]
	#print total_invest
	for ticker in Investment_ticker[1:]:
		#print total_invest_data[ticker]["Close Investment"]
		total_invest = total_invest_data[ticker]["Close Investment"] + total_invest

	#print total_invest

	# Sum all the money invested
	#print Book.index
	Principal = []
	for i in xrange(0,len(Book.index)):

		if "Purchase" in Book.iloc[i]["Transaction"]:
			if i == 0:
				Principal.append(float(Book.iloc[i]["Amount"].split("$")[1]))
				continue
			Principal.append(float(Book.iloc[i]["Amount"].split("$")[1])+Principal[i-1])

		elif "Sale" in Book.iloc[i]["Transaction"]:
			if i == 0:
				Principal.append(float(Book.iloc[i]["Amount"].split("$")[1]))
				continue
			Principal.append(Principal[i-1]-float(Book.iloc[i]["Amount"].split("$")[1]))


	#Principal.append(Principal[-1])
	
	weekFormatter = DateFormatter("%b %d '%y")#%H:%M:%S
	fig, ax = plt.subplots()
	fig.subplots_adjust(bottom=0.2)
	ax.xaxis.set_major_formatter(weekFormatter)
	plt.plot(total_invest,'g', Book.index, Principal,'-k')
	#plt.plot(Book.index,Principal)
	#fig.subplots_adjust()
	ax.xaxis_date()
	ax.autoscale_view()
	plt.title("Total")
	plt.setp( plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
	plt.grid()
	plt.show()


if __name__ == '__main__':
	main()