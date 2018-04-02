def compound_value(P0, percentage_value,time_expected):
	P = P0*(1+percentage_value)**time_expected
	return P

def active_compound_value(P0, percentage_return, time_expected):
	i = 0
	P = 0
	while i < time_expected:
		P = compound_value(P+P0,percentage_return, 1)
		i = i + 1

	return P


if __name__ == '__main__':
	# import matplotlib.pyplot as plt

	P0 = 80000
	percentage_return = 0.08
	time_expected = 10
	CV = compound_value(P0, percentage_return, time_expected)
	AC = active_compound_value(P0, percentage_return, time_expected)
	
	print "Normal compound: ", CV
	print "Return on Investment: ", (CV-P0)/P0*100, "%\n"
	print "Active compound: ", AC
	print "Return on Investment: ", (AC-P0)/P0*100, "%\n"