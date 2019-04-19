import edgar

Ticker = "Tesla"

some = edgar.Edgar().findCompanyName(Ticker)
print some
possible_companies = edgar.Edgar().getCikByCompanyName(some[0])
print possible_companies
#company = edgar.Company(Ticker,"21344")
#print company
