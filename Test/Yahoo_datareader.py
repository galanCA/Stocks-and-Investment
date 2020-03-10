import requests
import json

stock = 'KO'

# income statement
url_is = 'https://financialmodelingprep.com/api/v3/financials/income-statement' + stock + '?period=quarter'

# balance sheet
url_bs = 'https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/' + stock + '?period=quarter'

# cash flow
url_cf = 'https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/' + stock + '?period=quarter'

# Financial Ratios
#url_Fr

# Enterprise Value




###  Request data
web_is = requests.get(url_is)

income_statement = web_is.json()
print(income_statement)