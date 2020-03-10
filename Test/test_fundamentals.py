from yahoofinancials import YahooFinancials



ticker = 'KO'
YF = YahooFinancials(ticker)

balance_sheet_data_qt = YF.get_financial_stmts('annual', 'balance')
income_statement_data_qt = YF.get_financial_stmts('annual', 'income')
cash_statement_data_qt = YF.get_financial_stmts('annual', 'cash')
all_statement_data_qt =  YF.get_financial_stmts('annual', ['income', 'cash', 'balance'])
apple_earnings_data = YF.get_stock_earnings_data()
outstanding_share = YF.get_num_shares_outstanding()
market_cap = YF.get_market_cap()
#apple_net_income = YF.get_net_income()

#historical_stock_prices = YF.get_historical_price_data('2008-08-15', '2018-09-15', 'daily')

print ("Balance", balance_sheet_data_qt)
print ("income statement", income_statement_data_qt)
print ("cash statement", cash_statement_data_qt)
print ("earnings", apple_earnings_data)
print ("outstanding shares", outstanding_share)
print ("market cap", market_cap)
#print ("net income", apple_net_income)
#print( "Div", historical_stock_prices[ticker]['eventsData']['dividends'])

#print (YF.get_total_revenue())
#print (YF.get_50day_moving_avg())

print (income_statement_data_qt)
print (all_statement_data_qt)


#for div in historical_stock_prices[ticker]['eventsData']['dividends']:
#	print (div,historical_stock_prices[ticker]['eventsData']['dividends'][div])
