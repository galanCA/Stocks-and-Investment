from stock import stock
import os
import matplotlib.pyplot as plt

# Load file
file_path = "C:/Users/cesar/Documents/Finances/Stocks-and-Investment/mainCode/Portafolio.txt"
fid = open(file_path,"r");
text = fid.readlines()
fid.close()

# extract information
tickers = []
number_of_shares = []
average_price = []
for line in text:
	if "#" in line:
		continue
	tempLine = line.split("\n")
	temp = tempLine[0].split(":")
	tickers.append(temp[0])
	average_price.append(float(temp[1]))
	number_of_shares.append(float(temp[2]))
	print "You own", temp[2], "shares of", temp[0], "@", temp[1]

#
plot_handels = []
total_percentage = []

Company = []
gain_loss_percentage = []
gain_loss = []
for i in xrange(0,len(tickers)):
	print "Loading data from ", tickers[i]
	Company.append(stock(tickers[i]))
	value, value_percentage = Company[i].plot_returns(number_of_shares[i],average_price[i])
	gain_loss_percentage.append(value_percentage)
	gain_loss.append(value*number_of_shares[i])
	#print tickers[i], gain_loss[i]

total_returns = gain_loss[0]
for GL in gain_loss:
	total_returns = total_returns +  GL 

#print "returns", total_returns #gain_loss_percentage[0] + gain_loss_percentage[1]
total_returns = total_returns - gain_loss[0]
print "after minus", total_returns 

fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)

ax.plot(total_returns.index.values,total_returns)

ax.grid(True)
plt.show()
	
'''
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
	'''
'''
#plt.legend(plot_handels, tickers)
plt.grid(True)
plt.show()

#print "lenght of total percent return: ", len(total_percentage)

plt.plot(scraped_data.historic["date"], total_returns)
plt.grid(True)
plt.show()
'''