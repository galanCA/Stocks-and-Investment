from yahoofinancials import YahooFinancials

'''
Goal is to extract 
	Valuations measures
		Market Cap
		Enterprise Value
		Trailing P/E
		Foward P/E
		PEG Ratio
		Price/Sales
		Price/Book
		Enterprise Value/Revenue
		Enterprise Value/EBITDA
		ROTS

	Financials
		Profit Margin
		Operating Margin
		Return on Assets
		Return on Equity
		Revenue
		Revenue Per share
		Quaterly Revenue Growth
		Gross Profit
		EBITDA
		Net Income Avi to Common
		Dilute EPS
		Quaterly Earnings Growth
		Total Cash
		Total Cash Per Share
		Total Debt
		Total Debt/Equity
		Current Ratio
		Book Value per share
		Operating Cash Flow
		Levered Free Cash Flow

	Trading informations
		Beta
		50-Day Moving Average
		200 DayMoving Average
		Avg Vol (3Month)
		Shares Outstanding
		Float
		% Held by Insiders
		% Held by institutions
		Shares Shorts
		Short Ratio
		Short% of Float
		Shares Shorts (Prior Month)


'''

ticker = 'KO'
YF = YahooFinancials(ticker)

balance_sheet_data_qt = YF.get_financial_stmts('annual', 'balance')
income_statement_data_qt = YF.get_financial_stmts('annual', 'income')
cash_statement_data_qt = YF.get_financial_stmts('annual', 'cash')
all_statement_data_qt =  YF.get_financial_stmts('annual', ['income', 'cash', 'balance'])
apple_earnings_data = YF.get_stock_earnings_data()
outstanding_share = YF.get_num_shares_outstanding()
#apple_net_income = YF.get_net_income()
#$historical_stock_prices = YF.get_historical_price_data('2008-09-15', '2018-09-15', 'weekly')

print "Balance", balance_sheet_data_qt
print "income statement", income_statement_data_qt
print "cash statement", cash_statement_data_qt
print "earnings", apple_earnings_data
print outstanding_share
#print "net income", apple_net_income
#print "Prices", historical_stock_prices

#print YF.get_total_revenue()
#print YF.get_50day_moving_avg()

#print income_statement_data_qt
#print all_statement_data_qt

