import numpy as np 

def linspace(start_value,end_value,Number_l=1):
	P0 = float(start_value)
	Pd = float(end_value)
	N = float(Number_l)
	delta = (Pd-P0)/N

	#print "Starting while"
	array = []
	while P0 < Pd:
		array.append(P0)
		P0 = P0 + delta
		#print P0

	return array


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

def optimize_day_return(P0, rate, time_expected, month_income, Lp = 100, Lr= 100):

	if len(P0) == 2:
		#print "P0 Here"
		P = linspace(P0[0],P0[1], Lp)
	else:
		return None

	if len(rate) == 2:
		#print "r here"
		r = linspace(rate[0], rate[1], Lr)
	else:
		return None

	value_return = np.zeros((Lp,Lr))
	ROI = np.zeros((Lp,Lr))

	for i in xrange(0,Lp):
		for j in xrange(0,Lr):
			#print "i,j: ", i,j, " \tP,r:", P[i], r[j]
			value_return[i][j] = compound_value(P[i], r[j]/100, time_expected)
			ROI[i][j] = value_return[i][j] - P[i]


	return value_return, ROI,  P,r

if __name__ == '__main__':
	# import matplotlib.pyplot as plt

	#P0 = 360
	#percentage_return = 0.08
	#time_expected = 10
	#CV = compound_value(P0, percentage_return, time_expected)
	#AC = active_compound_value(P0, percentage_return, time_expected)
	
	#print "Normal compound: ", CV
	#print "Return on Investment: ", (CV-P0)/P0*100, "%\n"
	#print "Active compound: ", AC
	#print "Return on Investment: ", (AC-P0)/P0*100, "%\n"

	################## 
	print linspace(0,5,5)