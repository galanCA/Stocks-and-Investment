from edgar import Company, TXTML,XBRLElement,XBRL, Edgar


db = Edgar()
comp_name = 'TESLA, INC.'

company = Company(comp_name, db.all_companies_dict[comp_name])







'''
company = Company("Oracle Corp", "0001341439")
tree = company.get_all_filings(filing_type = "10-K")
docs = Company.get_documents(tree, no_of_documents=5)
print (docs)

text = TXTML.parse_full_10K(docs[0])
#print (text)
#company = edgar.Company(Ticker,"21344")
#print company


company = Company("Oracle Corp", "0001341439")
results = company.get_data_files_from_10K("EX-101.INS", isxml=True)
xbrl = XBRL(results[0])
element = XBRLElement(xbrl.relevant_children_parsed[15]).to_dict()#// returns a dictionary of name, value, and schemaRef
print(element)
'''