import sys
import matplotlib.pyplot as plt

sys.path.append('../Functions and Libs/')
import investing as INLIB

def main():
	P0 = [30, 800]
	rate_per_day = [1,5]
	month_income = 800

	time_in_day = 20

	[Total, ROI, P,r] = INLIB.optimize_day_return(P0, rate_per_day, time_in_day, month_income, Lr=10)

	print r
	plt.plot(P,ROI)
	plt.title("Return on investment in %i days"%time_in_day)
	#plt.legend(True)
	plt.grid(True)
	plt.show()

if __name__ == '__main__':
	main()