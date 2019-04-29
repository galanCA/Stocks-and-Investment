import edgar


company = edgar.Company("Oracle Corp", "0001341439")
tree = company.getAllFilings(filingType = "10-K")
docs = edgar.getDocuments(tree, noOfDocuments=5)
print docs
#company = edgar.Company(Ticker,"21344")
#print company
