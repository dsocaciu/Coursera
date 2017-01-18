import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt;
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import sys

def mysum(x):
	return sum(x);

def simulate(sd,ed,portfolio_prices,stock_symbol):
	#print "Start Date: " + str(sd);
	#print "End Date:" + str(ed);
	#print "Symbols: " + str(stocks);
	#print "Optimal Allocations: " + str(allocations);
	ls_keys = ['open','high','close','volume','actual_close'];
	dt_timeofday = dt.timedelta(hours=16);
	ldt_timestamps = du.getNYSEdays(sd,ed,dt_timeofday);

#	print(str(ldt_timestamps));

	c_dataobj = da.DataAccess('Yahoo', cachestalltime=0);
	ldf_data = c_dataobj.get_data(ldt_timestamps,stock_symbol,ls_keys);
	d_data = dict(zip(ls_keys,ldf_data));

	#myList = [10,20,30,40,50,60,70,80,90]
	#myInt = 10
	#newList = [x / myInt for x in myList]


	myFloat = float(portfolio_prices[0])

	portfolio_normalized_price = [float(x) / myFloat for x in portfolio_prices]
	#print(portfolio_prices)
	#print(portfolio_prices[0])
	
	p_ret = np.array(portfolio_normalized_price)
	p_ret = p_ret.reshape(len(p_ret),1)
	#print(p_ret)
	portfolio_rets = p_ret.copy();

	na_prices = d_data['close'].values
	na_normalized_price = na_prices / na_prices[0,:];
	#print(na_normalized_price)
	na_rets = na_normalized_price.copy();

	port_total_daily = np.apply_along_axis(mysum,axis=1,arr=portfolio_rets);
	port_cumret = port_total_daily[len(port_total_daily)-1];
	tsu.returnize0(port_total_daily);

	total_daily = np.apply_along_axis(mysum,axis=1, arr=na_rets);
	cumret = total_daily[len(total_daily)-1];	
	tsu.returnize0(total_daily);
	
	#print(str(total_daily));
	#print(np.std(alloc_na_rets));

	port_sharpe = (np.mean(port_total_daily)*252)/(np.std(port_total_daily) * np.sqrt(252));
	sharpe =  (np.mean(total_daily)*252)/(np.std(total_daily) * np.sqrt(252));

	port_vol = np.std(port_total_daily);
	vol = np.std(total_daily);

	port_avg = np.mean(port_total_daily);
	avg = np.mean(total_daily);
	#print("Average Daily Return: " + str(((total_daily[len(total_daily)-1]-1))/251));

	print("portfolio sharpe " + str(port_sharpe) + "; cumret: " + str(port_cumret) + "; vol: " + str(port_vol) + "; avg: " + str(port_avg) )
	print("compare sharpe " + str(sharpe) + "; cumret: " + str(cumret) + "; vol: " + str(vol) + "; avg: " + str(avg) )
	

	#print(str(allocations));
	#na_rets = na_rets * allocations;
	#print str(na_rets);
	#tsu.returnize0(na_rets);
	#print str(na_rets);
 	#na_rets= na_rets * allocations;
	#print(str(np.std(na_rets)));
 
	#print(str(np.mean(na_rets)))
def portfolioOptimizer(sd,ed,stocks): 
	temp_sharpe_ratio=0.0;
	sharpe_ratio=0.0;
	volatility=0.0;
	average_ret=0.0;
	cum_ret=0.0;
	best_x=0.0;
	best_y=0.0;
	best_w=0.0;
	best_z = 0.0;
	allocation_range = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
	
	for x in allocation_range:
	#print x;
		for y in allocation_range:
		#print (" "+str(y));
			for w in allocation_range:
				for z in allocation_range:
					if x+y+w+z==1.0:
						temp_sharpe_ratio, volatility, average_ret, cum_ret = simulate(sd,ed,stocks,([x,y,w,z]));
						if temp_sharpe_ratio > sharpe_ratio:
							best_z = z;
							best_w = w; 
							best_y = y;
							best_x = x;
							sharpe_ratio = temp_sharpe_ratio;
#print i;


#print temp_sharpe_ratio;
#print volatility;
#print average_ret;
#print cum_ret;


	print "Start Date: " + str(sd);
	print "End Date:" + str(ed);
	print "Symbols: " + str(stocks);
	print "Allocations: " + stocks[0] + " : " + str(best_x) + "; " + stocks[1] + " : " + str(best_y) + "; " + stocks[2] + " : " + str(best_w) + "; " + stocks[3] + " : " + str(best_z);

	print ("Best Sharpe Ratio: " +str(sharpe_ratio));

if __name__ == '__main__':

	
	csvfile = open(sys.argv[1],'rb')

	orders_timestamps = []
	fund_prices = []
	orders = []
	compare_symbol = []


	for row in csvfile:
		col = str.split(row, ',')
		fund_price = col[3]
		#print symbol
		year = col[0]
		month = col[1]
		day = col[2]

		if fund_price not in fund_prices:
			fund_prices.append(float(fund_price))

		if dt.datetime(int(year),int(month), int(day)) not in orders_timestamps:
			orders_timestamps.append(dt.datetime(int(year),int(month), int(day),16))

	orders_timestamps.sort()

	compare_symbol.append(sys.argv[2])

	#print str(orders_timestamps)

	dt_start = orders_timestamps[0]
	dt_end = orders_timestamps[len(orders_timestamps)-1]

	print("Data Range :  " + str(dt_start) + " to " + str(dt_end)) 

	simulate(dt_start,dt_end,fund_prices,compare_symbol)