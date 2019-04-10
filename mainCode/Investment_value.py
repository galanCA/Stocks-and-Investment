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
	temp_array = np.zeros(len(stock_hist.trade_history.index) )
	for i in xrange(0,len(Book)):
		prev_frac = 0
		if Book.iloc[i]["Ticker"] in ticker:
			if "Sale" in Book.iloc[i]["Transaction"]:
				#print Book.iloc[i].name
				#continue
				Date = Book.iloc[i].name

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

				#print stock_hist.trade_history["Close"][j]
				Share_frac = -float(sub(r'[^\d.]', '', Book.iloc[i]["Amount"][1:]))/stock_hist.trade_history["Close"][j]#close price that day
			
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
	#print len(temp_inv)
	
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
		
		# Add the stock to the panel
		#temp_ETF.plot_line(day_value="Close")
		set_data[ticker] = temp_ETF.trade_history



	# Check the size of data. Must be equal at all times
	for ticker in Investment_ticker:
 		date_index = set_data[ticker].index
		L = len(set_data[ticker])

		try:
			if L < prev_L:
				for idx, val in enumerate(prev_dateI):
					if val > date_index[0]:
						i = idx
						break
				temp_col = list(set_data[ticker].columns.values)
				temp_prev_data =  pd.DataFrame(data=np.zeros((len(prev_dateI[:i-1]), len(temp_col) )), index=prev_dateI[:i-1], columns=temp_col)
				set_data[ticker] =  temp_prev_data.append(set_data[ticker])

				continue
		except UnboundLocalError:
			pass 

		prev_L = L
		prev_dateI = date_index


	# Convert data to Pandas
	total_invest_data = pd.Panel(set_data)
	
	# set up total_invest data structure
	total_invest = total_invest_data[Investment_ticker[0]]["Close Investment"]
	for ticker in Investment_ticker[1:]:
		total_invest = total_invest_data[ticker]["Close Investment"] + total_invest

	# Sum all the money invested
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
	plt.legend(labels=["Investment","Principal"])
	plt.setp( plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
	plt.grid()
	#plt.show()

	# Create Month to month ROI and year to year
	#print Book.index
	#print Principal 	
	#print total_invest 

	month_principal = []
	month_date = []
	for i, d in enumerate(Book.index):
		try:
			if d.month > prev_date.month and d.year == prev_date.year or d.year != prev_date.year:
				# all shenanigans
				#print i, d, d.month
				#print Principal[i]
				if d.day == 1:
					k = i
					#print "Month", d.month, Book.index[i] ,Principal[i]
				else:
					k= i-1
					#print "Prev month", d.month,Book.index[i-1], Principal[i-1]

				if d.month > prev_date.month+1:
					dummy = prev_date.month+1
					while dummy < d.month:
						#print datetime.datetime(d.year,dummy,1), Principal[k]
						month_date.append(datetime.datetime(d.year,dummy,1))
						month_principal.append(Principal[k])
						#print "miss month", dummy, Principal[k]
						dummy = dummy+1

				#Principal[k] 
				#print datetime.datetime(d.year,d.month,1), Principal[k]
				month_date.append(datetime.datetime(d.year,d.month,1))
				month_principal.append(Principal[k])
			prev_date = d
		except UnboundLocalError:
			prev_date = d
			continue

	# if the month already pass it and not investment has being made then it updates to the current month 
	if datetime.datetime.today().month > Book.index[-1].month: 
		print Book.index[-1],Principal[-1]
		d_dummy = Book.index[-1]
		month_date.append(datetime.datetime(d_dummy.year,d_dummy.month+1,1))
		month_principal.append(Principal[-1])


	# Investment
	total_invest_month = []
	j = 0 
	for index, d in enumerate(total_invest.index):
		if j >= len(month_date):
			break	
		if month_date[j].month == d.month and month_date[j].year == d.year:
			#print d, index, total_invest[index]  
			j = j + 1
			total_invest_month.append(total_invest[index])
	
	percent_month = []
	ROI = []
	for i in xrange(0,len(month_date)):
		#print total_invest_month[i], month_principal[i]
		percent_month.append((total_invest_month[i] - month_principal[i])/month_principal[i]*100.0)
		ROI.append(total_invest_month[i] - month_principal[i])
	
	#percent_month=100.0*(total_invest_month - month_principal)/month_principal

	weekFormatter = DateFormatter("%b %d '%y")#%H:%M:%S
	fig, ax = plt.subplots()
	fig.subplots_adjust(bottom=0.2)
	ax.xaxis.set_major_formatter(weekFormatter)
	plt.plot(month_date,ROI)
	#fig.subplots_adjust()
	ax.xaxis_date()
	ax.autoscale_view()
	plt.title("Total")
	

	#plt.legend(labels=["Investment","Principal"])
	plt.setp( plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
	plt.grid()

	ax2 = ax.twinx()
	ax2.plot(month_date,percent_month,'g*-')

	plt.show()


if __name__ == '__main__':
	main()