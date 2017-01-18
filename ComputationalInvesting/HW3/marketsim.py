#!/usr/bin/python

import sys
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




if __name__ == '__main__':

	csvfile = open(sys.argv[2],'rb')

	print(sys.argv[2])

	orders_timestamps = []
	symbols = []
	orders = []

	portfolio = sys.argv[1]

	float_port = float(portfolio)

	float_fund = float(0)

	valuesfile = open(sys.argv[3], 'w')

	valuescsv = csv.writer(valuesfile)

	#print csvfile.name

	print "portfolio value: " + str(float_port)

	#print len(csvfile)
	for row in csvfile:
		print(row)
		col = str.split(row, ',')
		symbol = col[3]
		#print symbol
		year = col[0]
		month = col[1]
		day = col[2]

		if symbol not in symbols:
			symbols.append(symbol)

		
		orders_timestamps.append(dt.datetime(int(year),int(month), int(day),16))

	orders_timestamps.sort()

	print str(orders_timestamps)

	dt_start = orders_timestamps[0]
	dt_end = orders_timestamps[len(orders_timestamps)-1]

	print("Data Range :  " + str(dt_start) + " to " + str(dt_end)) 
	

	ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

	dataobj = da.DataAccess('Yahoo')
	ls_symbols = symbols
	ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
	ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
	ld_data = dict(zip(ls_keys, ldf_data))

	df_close = ld_data['close']

	#ldt_timestamps = df_close.index

	
	#df_trades = pd.DataFrame(index=ldt_timestamps, columns=ls_symbols)

	#df_trades = pd.DataFrame()

	#for s_sym in ls_symbols:
	#	for i in range(1, len(orders_timestamps)):
	#		f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
			#print str(s_sym) + " " + str(ldt_timestamps[i]) + " "  + str(f_symprice_today)



	df_trades = copy.deepcopy(df_close)
	df_trades = df_trades * 0

	df_holdings = copy.deepcopy(df_trades)
	df_holdings = df_holdings * 0

	df_fund = copy.deepcopy(df_holdings)
	df_fund = df_fund * 0

	total_fund = []

	cost = copy.deepcopy(df_fund)
	cost = cost * 0

	df_cash = copy.deepcopy(cost)
	df_cash = df_cash * 0


	df_values = copy.deepcopy(df_cash)
	df_values = df_values * 0

	csvfile = open(sys.argv[2],'rb')
	for row in csvfile:
		col = str.split(row, ',')
		#print str(row)
		symbol = col[3]
		#print symbol
		year = col[0]
		month = col[1]
		day = col[2]

		date = dt.datetime(int(year),int(month), int(day),int(16))


		if col[4] == 'Buy':
			#print str(col[2])
			#print str(df_trades[symbol])
			
			df_trades[symbol].ix[date] +=  int(col[5])
		elif col[4] == 'Sell':
			#print str(col[2])
			#print str(df_trades[symbol])
			df_trades[symbol].ix[date] -= int(col[5])

	#for d in orders_timestamps:
	#	print str(d)

	
	for d in range(0, len(ldt_timestamps)):
		#value = 0
		for s_sym in ls_symbols:
		#print str(orders_timestamps[d])
#f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]

			#if d == 0 :
			#holdings = trade
				#print s_sym
			#print("Trade Date : " + str(ldt_timestamps[d].year) + " "+s_sym +  " " +str(df_close[s_sym].ix[ldt_timestamps[d]]))
			if df_trades[s_sym].ix[ldt_timestamps[d]] > 0:
				print("Buy - Minus Cash " + str(s_sym) + " " + str(df_trades[s_sym].ix[ldt_timestamps[d]]))
				print(str(df_trades[s_sym].ix[ldt_timestamps[d]] * df_close[s_sym].ix[ldt_timestamps[d]]))
				float_port = float_port - (df_trades[s_sym].ix[ldt_timestamps[d]] * df_close[s_sym].ix[ldt_timestamps[d]])
				

				
				

			elif df_trades[s_sym].ix[ldt_timestamps[d]] < 0:
				print("Sell - Plus Cash " + str(s_sym) + " " + str(df_trades[s_sym].ix[ldt_timestamps[d]]))
				print(str(df_trades[s_sym].ix[ldt_timestamps[d]] * df_close[s_sym].ix[ldt_timestamps[d]]))
				float_port = float_port - (df_trades[s_sym].ix[ldt_timestamps[d]] * df_close[s_sym].ix[ldt_timestamps[d]])
				if d > 0:
					df_holdings[s_sym].ix[ldt_timestamps[d]] = df_holdings[s_sym].ix[ldt_timestamps[d-1]] + df_trades[s_sym].ix[ldt_timestamps[d]]
				else:
					df_holdings[s_sym].ix[ldt_timestamps[d]] = df_trades[s_sym].ix[ldt_timestamps[d]]

			if d > 0:
				df_holdings[s_sym].ix[ldt_timestamps[d]] = df_holdings[s_sym].ix[ldt_timestamps[d-1]] + df_trades[s_sym].ix[ldt_timestamps[d]]
			else:
				df_holdings[s_sym].ix[ldt_timestamps[d]] = df_trades[s_sym].ix[ldt_timestamps[d]]

			#		float_port = float_port + (df_trades[s_sym].ix[ldt_timestamps[d]] * df_close[s_sym].ix[ldt_timestamps[d]])
			#print("Holdings: " + str(df_holdings[s_sym].ix[ldt_timestamps[d]]))
			df_fund[s_sym].ix[ldt_timestamps[d]] = df_holdings[s_sym].ix[ldt_timestamps[d]] *  df_close[s_sym].ix[ldt_timestamps[d]]
			#print ("Cash: " + str(float_port))
			#print("Fund " + str(df_fund[s_sym].ix[ldt_timestamps[d]]))

		array = []
		float_fund = 0.0

		array.append(ldt_timestamps[d].year)
		array.append(ldt_timestamps[d].month)
		array.append(ldt_timestamps[d].day)
		for s_sym in ls_symbols:
			float_fund += df_fund[s_sym].ix[ldt_timestamps[d]]
		array.append(float_port + float_fund)
		#print(array)
		valuescsv.writerow(array)
			
			#	df_holdings[s_sym].ix[ldt_timestamps[d]] = df_trades[s_sym].ix[ldt_timestamps[d]]
			#	print("df_holdings[s_sym].ix[ldt_timestamps[d]]: " + str(s_sym) + " " +str(ldt_timestamps[d]) + "  " + str(df_holdings[s_sym].ix[ldt_timestamps[d]]))
valuesfile.close()
			#else:

			#	if df_trades[s_sym].ix[ldt_timestamps[d]] > 0:
			#		print("Buy - Minus Cash " + str(d))
			#		float_port = float_port - ((df_trades[s_sym].ix[ldt_timestamps[d-1]] - df_trades[s_sym].ix[ldt_timestamps[d]]) * df_close[s_sym].ix[ldt_timestamps[d]])
			#	elif df_trades[s_sym].ix[ldt_timestamps[d]] < 0:
			#		print("Sell - Plus Cash " + str(d))
			#		float_port = float_port + ((df_trades[s_sym].ix[ldt_timestamps[d-1]] - df_trades[s_sym].ix[ldt_timestamps[d]]) * df_close[s_sym].ix[ldt_timestamps[d]])

#				df_holdings[s_sym].ix[ldt_timestamps[d]] = df_holdings[s_sym].ix[ldt_timestamps[d-1]] + df_trades[s_sym].ix[ldt_timestamps[d]]
#				print("df_holdings[s_sym].ix[ldt_timestamps[d]]: " + str(s_sym) + " " +str(ldt_timestamps[d]) + "  " + str(df_holdings[s_sym].ix[ldt_timestamps[d-1]] + df_trades[s_sym].ix[ldt_timestamps[d]]))
			

#			df_fund[s_sym].ix[ldt_timestamps[d]] = df_holdings[s_sym].ix[ldt_timestamps[d]] *  df_close[s_sym].ix[ldt_timestamps[d]]
#			print ( "fund = holdings " + str(df_holdings[s_sym].ix[ldt_timestamps[d]]) + " * last " + str(df_close[s_sym].ix[ldt_timestamps[d]]) + " = " + str(df_fund[s_sym].ix[ldt_timestamps[d]]) )



			

#			print ldt_timestamps[d]
			
			#print("cash " + str(float_port))
			#print("fund " +  str(df_fund[s_sym].ix[ldt_timestamps[d]]))
			#print("total " + str(float_port+df_fund[s_sym].ix[ldt_timestamps[d]]))

			#df_values[s_sym].ix[ldt_timestamps[d]] = df_fund[s_sym].ix[ldt_timestamps[d]] + cost[s_sym].ix[ldt_timestamps[d]]

			
			#float_port = df_values[s_sym].ix[ldt_timestamps[d]]
		


