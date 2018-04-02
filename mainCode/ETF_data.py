from stock import stock
import os
import matplotlib.pyplot as plt

file_path = "C:/Users/cesar/Documents/Fiannces/Investing Stock/ticker_ETF.init"
#fid = open("C:\Users\cesar\Documents\Fiannces\Investing Stock\\ticker_ETF.init","r")
fid = open("ticker_ETF.txt","r");
text = fid.readlines()
fid.close()

tickers = []
invested = []
average_price = []
for line in text:
	tempLine = line.split("\n")
	temp = tempLine[0].split(":")
	tickers.append(temp[0])
	invested.append(float(temp[1]))
	average_price.append(float(temp[2]))

plot_handels = []
total_percentage = []
total_returns = []
for i in xrange(0,len(tickers)):
	print "Loading data from ", tickers[i]
	scraped_data = stock(tickers[i])
	
	return_investment = []
	percent_return = []
	
	for j in xrange(0,len(scraped_data.historic["date"])):
		[return_investment, percent_return] = scraped_data.investment_return(average_price[i])

		if not i:
			total_percentage.append(percent_return[j])
			total_returns.append(return_investment[j])
		else:
			total_percentage[j] = total_percentage[j] + percent_return[j]
			total_returns[j] = total_returns[j] + return_investment[j]

	plot_handels.append(plt.plot(scraped_data.historic["date"],  return_investment, label=tickers[i]))

#plt.legend(plot_handels, tickers)
plt.grid(True)
plt.show()

#print "lenght of total percent return: ", len(total_percentage)

plt.plot(scraped_data.historic["date"], total_returns)
plt.grid(True)
plt.show()
	