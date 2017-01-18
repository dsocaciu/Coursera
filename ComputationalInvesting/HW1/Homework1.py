import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt;
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#import scipy.optimize as spo


def mysum(x):
	return sum(x);

def simulate(sd,ed,stocks,allocations):
	#print "Start Date: " + str(sd);
	#print "End Date:" + str(ed);
	#print "Symbols: " + str(stocks);
	#print "Optimal Allocations: " + str(allocations);
	ls_keys = ['open','high','close','volume','actual_close'];
	dt_timeofday = dt.timedelta(hours=16);
	ldt_timestamps = du.getNYSEdays(sd,ed,dt_timeofday);

#	print(str(ldt_timestamps));

	c_dataobj = da.DataAccess('Yahoo', cachestalltime=0);
	ldf_data = c_dataobj.get_data(ldt_timestamps,stocks,ls_keys);
	d_data = dict(zip(ls_keys,ldf_data));

	na_prices = d_data['close'].values
	#print str(na_prices);
	#print str(na_prices[0,:]*allocations);	
	na_normalized_price = na_prices / na_prices[0,:];
	#na_normalized_price = na_normalized_price * allocations;
	na_rets = na_normalized_price.copy();
	alloc_na_rets  = (allocations*na_rets);

	total_daily = np.apply_along_axis(mysum,axis=1, arr=alloc_na_rets);
	cumret = total_daily[len(total_daily)-1];	
	#total_daily[:,2]
	tsu.returnize0(total_daily);
	
	#print(str(total_daily));
	#print(np.std(alloc_na_rets));

	sharpe =  (np.mean(total_daily)*252)/(np.std(total_daily) * np.sqrt(252));

	vol = np.std(total_daily);
	avg = np.mean(total_daily);
	#print("Average Daily Return: " + str(((total_daily[len(total_daily)-1]-1))/251));

	return (sharpe,vol, avg, cumret)
	

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
	print "Allocations: " + str(stocks[0]) + " : " + str(best_x) + "; " + str(stocks[1]) + " : " + str(best_y) + "; " + str(stocks[2]) + " : " + str(best_w) + "; " + str(stocks[3]) + " : " + str(best_z);

	print ("Best Sharpe Ratio: " +str(sharpe_ratio));

#Sharpe Ratio
#1-portfolioOptimizer(dt.datetime(2011,1,1),dt.datetime(2011,12,31),(['AAPL','GOOG','IBM','MSFT']));
#2-portfolioOptimizer(dt.datetime(2010,1,1),dt.datetime(2010,12,31),(['BRCM','ADBE','AMD','ADI']));
#3-portfolioOptimizer(dt.datetime(2011,1,1),dt.datetime(2011,12,31),(['BRCM','TXN','AMD','ADI']));
#4-portfolioOptimizer(dt.datetime(2010,1,1),dt.datetime(2010,12,31),(['BRCM','TXN','IBM','HNZ']));
#5-portfolioOptimizer(dt.datetime(2010,1,1),dt.datetime(2010,12,31),(['C','GS','IBM','HNZ']));

#Asset Allocation
portfolioOptimizer(dt.datetime(2011,1,1),dt.datetime(2011,12,31),(['AAPL','GOOG','IBM','MSFT']));
#7-portfolioOptimizer(dt.datetime(2011,1,1),dt.datetime(2011,12,31),(['BRCM','ADBE','AMD','ADI']));
#8-portfolioOptimizer(dt.datetime(2011,1,1),dt.datetime(2011,12,31),(['BRCM','TXN','AMD','ADI']));
#9-portfolioOptimizer(dt.datetime(2010,1,1),dt.datetime(2010,12,31),(['BRCM','TXN','IBM','HNZ']));
#10-portfolioOptimizer(dt.datetime(2010,1,1),dt.datetime(2010,12,31),(['C','GS','IBM','HNZ']));