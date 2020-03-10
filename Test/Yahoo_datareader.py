import requests
import json

def webRaw(url):
	rq = requests.get(url)
	return rq.json()
	
stock = 'KO'

# Profile
url_pf = 'https://financialmodelingprep.com/api/v3/company/profile/' + stock

# income statement
url_is = 'https://financialmodelingprep.com/api/v3/financials/income-statement/' + stock #+ '?period=quarter'

# balance sheet
url_bs = 'https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/' + stock + '?period=quarter'

# cash flow
url_cf = 'https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/' + stock + '?period=quarter'

# Financial Ratios
#url_Fr

# Enterprise Value

print(webRaw(url_pf))

'''
###  Request data
web_is = requests.get(url_is)

income_statement = web_is.json()
#print(income_statement['financials'])

for i in income_statement['financials']:
	print(i['date'])
'''
