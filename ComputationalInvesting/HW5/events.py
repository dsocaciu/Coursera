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


def find_bollinger(ls_symbols, d_data):
#''' Finding the event dataframe '''
    df_close = d_data['close']
    #ts_goog = df_close['GOOG']

    print "Calculating Bollinger"

    # Creating an empty dataframe
    df_mean = copy.deepcopy(df_close)
    df_mean = df_mean * np.NAN

    df_stdev = copy.deepcopy(df_close)
    df_stdev = df_stdev * np.NAN

    df_bol = copy.deepcopy(df_close)
    df_bol = df_bol * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_close.index

    df_mean=pd.rolling_mean(df_close,20)

    df_stdev = pd.rolling_std(df_close,20)

    df_bol = (df_close-df_mean)/df_stdev


    events = 0
    for s_sym in ls_symbols:


        for i in range(1, len(ldt_timestamps)-20):
            # Calculating the returns for this timestamp
            #f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            #f_symmean_today = df_mean[s_sym].ix[ldt_timestamps[i]]
            #f_symstdev_today = df_stdev[s_sym].ix[ldt_timestamps[i]]

            #bol_val = (f_symprice_today-f_symmean_today)/(f_symstdev_today)
        #print (str(ldt_timestamps[i])+"; "+str(f_symprice_today)+"; "+str(f_symmean_today)+"; "+str(f_symstdev_today)+"; "+str(bol_val))

            if df_bol[s_sym].ix[ldt_timestamps[i]] <= -2.0 and df_bol[s_sym].ix[ldt_timestamps[i-1]] >= -2.0 and df_bol['SPY'].ix[ldt_timestamps[i]] >= 1.0 :
                events+=1
                print(str(s_sym) + " : " + str(ldt_timestamps[i])+"  "+str(df_bol[s_sym].ix[ldt_timestamps[i]]) + " : " + str(ldt_timestamps[i-1]) + " " + str(df_bol[s_sym].ix[ldt_timestamps[i-1]]) + " : " + str(df_bol['SPY'].ix[ldt_timestamps[i]]))


        #    f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
        #    f_marketprice_today = ts_market.ix[ldt_timestamps[i]]
        #    f_marketprice_yest = ts_market.ix[ldt_timestamps[i - 1]]
        #    f_symreturn_today = (f_symprice_today / f_symprice_yest) - 1
        #    f_marketreturn_today = (f_marketprice_today / f_marketprice_yest) - 1
    print events


if __name__ == '__main__':
	print"Starting "
	dt_start = dt.datetime(2008, 1, 1)
	dt_end = dt.datetime(2009, 12, 31)
	ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

	dataobj = da.DataAccess('Yahoo')
	ls_symbols = dataobj.get_symbols_from_list('sp5002012')
        ls_symbols.append('SPY')
        #ls_symbols.append('GOOG')

        ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
   	ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
        d_data = dict(zip(ls_keys, ldf_data))

        for s_key in ls_keys:
       	    d_data[s_key] = d_data[s_key].fillna(method='ffill')
       	    d_data[s_key] = d_data[s_key].fillna(method='bfill')
       	    d_data[s_key] = d_data[s_key].fillna(1.0)

        find_bollinger(ls_symbols, d_data)
    	#print "Creating Study"
    	#ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
        #        s_filename='MyEventStudy.pdf', b_market_neutral=True, b_errorbars=True,
        #        s_market_sym='SPY')
