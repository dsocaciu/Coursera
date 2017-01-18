'''
(c) 2011, 2012 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see
http://wiki.quantsoftware.org/index.php?title=QSTK_License
for license details.

Created on January, 23, 2013

@author: Sourabh Bajaj
@contact: sourabhbajaj@gatech.edu
@summary: Event Profiler Tutorial
'''


import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep

import csv

"""
Accepts a list of symbols along with start and end date
Returns the Event Matrix which is a pandas Datamatrix
Event matrix has the following structure :
    |IBM |GOOG|XOM |MSFT| GS | JP |
(d1)|nan |nan | 1  |nan |nan | 1  |
(d2)|nan | 1  |nan |nan |nan |nan |
(d3)| 1  |nan | 1  |nan | 1  |nan |
(d4)|nan |  1 |nan | 1  |nan |nan |
...................................
...................................
Also, d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)
"""


def find_events(ls_symbols, d_data):
#''' Finding the event dataframe '''
    df_close = d_data['actual_close']
    ts_market = df_close['SPY']

    print "Finding Events"
    valuesfile = open("orders.csv", 'w')

    valuescsv = csv.writer(valuesfile)

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_close.index

    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            # Calculating the returns for this timestamp
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
            f_marketprice_today = ts_market.ix[ldt_timestamps[i]]
            f_marketprice_yest = ts_market.ix[ldt_timestamps[i - 1]]
            f_symreturn_today = (f_symprice_today / f_symprice_yest) - 1
            f_marketreturn_today = (f_marketprice_today / f_marketprice_yest) - 1

            # Event is found if the symbol is down more then 3% while the
            # market is up more then 2%
            if f_symprice_yest >= 7.0 and f_symprice_today <  7.0:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1
                buyarray = []
                buyarray.append(ldt_timestamps[i].year)
                buyarray.append(ldt_timestamps[i].month)
                buyarray.append(ldt_timestamps[i].day)
                buyarray.append(s_sym)
                buyarray.append("Buy")
                buyarray.append(100)
                #print(array)
                valuescsv.writerow(buyarray)

                sellarray = []
                if i+5>=len(ldt_timestamps):
                    sellarray.append(ldt_timestamps[len(ldt_timestamps)-1].year)
                    sellarray.append(ldt_timestamps[len(ldt_timestamps)-1].month)
                    sellarray.append(ldt_timestamps[len(ldt_timestamps)-1].day)
                    sellarray.append(s_sym)
                    sellarray.append("Sell")
                    sellarray.append(100)
                else:
                    #print(str(len(ldt_timestamps))+": "+str(i) + " : " + str(ldt_timestamps[i]))
                    sellarray.append(ldt_timestamps[i+5].year)
                    sellarray.append(ldt_timestamps[i+5].month)
                    sellarray.append(ldt_timestamps[i+5].day)
                    sellarray.append(s_sym)
                    sellarray.append("Sell")
                    sellarray.append(100)   
                #print(array)
                valuescsv.writerow(sellarray)


                #print(str(ldt_timestamps[i].year)+","+str(ldt_timestamps[i].month)+","+str(ldt_timestamps[i].day)+","+s_sym+",Buy,"+str(100))
                #print(str(ldt_timestamps[i+5].year)+","+str(ldt_timestamps[i+5].month)+","+str(ldt_timestamps[i+5].day)+","+s_sym+",Sell,"+str(100))
    valuesfile.close()
    return df_events


if __name__ == '__main__':
	print"Starting "
	dt_start = dt.datetime(2008, 1, 1)
	dt_end = dt.datetime(2009, 12, 31)
	ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

	dataobj = da.DataAccess('Yahoo')
	ls_symbols = dataobj.get_symbols_from_list('sp5002012')
    	ls_symbols.append('SPY')

    	ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
   	ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    	d_data = dict(zip(ls_keys, ldf_data))

    	for s_key in ls_keys:
        	d_data[s_key] = d_data[s_key].fillna(method='ffill')
        	d_data[s_key] = d_data[s_key].fillna(method='bfill')
        	d_data[s_key] = d_data[s_key].fillna(1.0)

    	df_events = find_events(ls_symbols, d_data)
    	print "Creating Study"
    	ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                s_filename='MyEventStudy.pdf', b_market_neutral=True, b_errorbars=True,
                s_market_sym='SPY')
