from __future__ import (absolute_import,division,print_function,unicode_literals)

import backtrader as bt
from datetime import datetime 
import pandas as pd
import numpy as np
import backtrader.indicators as btind
import talib as ta


class FirstStrategy(bt.Strategy):

	params = (
		('exitbars' , 5),
		)

	def log(self,text):
		print(text)


	def __init__(self):
		self.dataclose = self.datas[0].close

		self.hilodiff = self.datas[0].high - self.datas[0].low


		self.ema15 = bt.indicators.ExponentialMovingAverage(self.dataclose[0], period = 15)
		self.ema31 = bt.indicators.ExponentialMovingAverage(self.dataclose[0] , period = 31)

			

	def notify_order(self,order):

		if self.order in [self.Submitted, self.Accepted]:
			return

		if self.order in [self.Completed]:
			if order.isbuy():
				self.log("BUY EXECUTED: " + str(order.executed.price))

			elif order.issell():
				self.log("SELL EXECUTED: " + str(order.executed.price))

			self.bar_executed = len(self)

		elif self.order in [self.Canceled, self.Margin, self.Rejected]:

			self.log('ORDER CANCELED')



	def next(self):


		self.log("Close: " + str(self.dataclose[0]))

		print('EMA 15: ' , self.ema15[0])
		print('EMA 31: ', self.ema31[0])

		if not self.position:  

			print('THERE IS NO POSITION ON')
			
			if self.ema15[0] > self.ema31[0]:

					self.order = self.buy()

					self.log(str(self.datas[0].datetime.date[0]) + "BUY ORDER DONE; " + str(self.dataclose[0]))
						
		else:
			
			print('THERE IS A POSITION ON')

			if self.ema15[0] < self.ema[31]: 
				print("ENTERING EXIT LOOP")
				self.close()
				self.log("SELL ORDER DONE: " + str(self.dataclose[0]))
				self.candletracker = 0

    

if __name__ == "__main__":

	cerebro = bt.Cerebro()

	cerebro.addstrategy(FirstStrategy) 

	datapath = 'Data/Niftyfutures-5m.csv'

	data = bt.feeds.GenericCSVData (
		dataname = datapath,
		fromdate = datetime(2012,1,1),
		todate = datetime(2015,1,1),
		datetime = 0,
		timeframe = bt.TimeFrame.Minutes, 
		compression = 1,
		dtformat = ('%Y-%m-%d %H:%M:%S'), 
		open = 1,
		high = 2,
		low = 3,
		close = 4,
		volume = None,
		openinterest = None,
		reverse = False,
		header = 0
		)

	cerebro.adddata(data)

	cerebro.addsizer(bt.sizers.FixedSize, stake=1)

	#cerebro.broker.setcommission(commission = 0.002) 

	cerebro.broker.setcash(1000000)

	print("Starting Portfolio Value : ", cerebro.broker.getvalue())

	cerebro.run()

	print("Final Portfolio Value: ", cerebro.broker.getvalue())


