1. Design mySQL database structure: Able to store daily, hourly, weekly data. Easy to dynamically update 
	everyday/hour/week according to selected stock list.  Need to use TuShare package.  

2. Have the code to update stock list. Have a column to flag "active" and "inactive" stock (using active_flag=1/0). 
	"active" means every run of daily/hourly/weekly data pulling needs to pull data for this stock.

3. Make sure data pulling module can integrate with indicator calculation module, and to update mySQL database with the 
	newest data points

3. Write a module to send e-mail alert and to update a table to flag "buy/sell/hold" signal. The table can be stored 
	locally or on server

4. Prepare back test module. 

5. Search github or other forum to get a code to plot candle stick chart with MA lines (均线) on top of it. 

6. 我用以下代码跑出来的５分钟的数据，无法作日期的比较。能否帮我看一下语法。错误出现在最后一行命令

		import tushare as ts
		import numpy as np
		import pandas as pd
		import datetime
		from __future__ import division
		import matplotlib
		import matplotlib.pyplot as plt
		plt.style.use("ggplot")
		import scipy.stats as stats
		%matplotlib inline

		df_h=ts.get_hist_data(code='000725',ktype='5',start='2018-03-15')
		df_h.reset_index(inplace=True)

		df_h['date']=pd.to_datetime(df_h['date'])
		df_h['date_only']=df_h['date'].dt.date

		sample=df_h[df_h['date_only']<datetime.date('2018-03-20',"%Y-%m-%d")]
		错误提示
		---------------------------------------------------------------------------
		TypeError                                 Traceback (most recent call last)
		<ipython-input-58-d6882cb544f7> in <module>()
		----> 1 sample=df_h[df_h['date_only']<datetime.date('2018-03-20',"%Y-%m-%d")]

		TypeError: an integer is required

========================================================================
[update at 2018-04-22]
========================================================================
以下是从实现角度总结的decision，还有一些问题："***实现及问题***"

股票状态总共两种：EMPTY，HOLD
	初始化股票数据的时候，状态为EMPTY，发出BUY的信号后，状态为HOLD，发出SELL的信号后状态为EMPTY

做decision的逻辑如下

1. 如果股票状态为HOLD：
	（1）某一个小时的收盘价的MA5<MA10
		***日期T，60分K线中的一条数据***
	（2）前一个小时的收盘价MA5>MA10
		***日期T，60分K线中的上一条数据***
	     [answer/comment]日期可能为T, 也可能为T-1。 注意这里是按照交易日，非自然日
	（3）前一日收盘价均线 （MA5-MA10）< 上前一交易日日收盘价均线(MA5-MA10)
		***日期T-1，日k线数据和日期T-2日K线数据比较***
	
	上述三个条件同时满足：SIGNAL = SELL
2. 如果股票状态为EMPTY：
	（1）过去两周走势跟大盘的对比
			10日均线的斜率对比
			***上周，周K线MA10 > 上上周,周K线MA10***
			上一日收盘价和14个交易日前收盘价的对比
			***日K数据，价格满足什么条件？？***
			[answer] (日线T-1收盘价- (T-14)收盘价)/(T-14)收盘价>(大盘T-1收盘点-(T-14)收盘点)/(大盘T-14)收盘点。 注意这里的T-1
			T-14 是按照交易日，并非自然日
			上涨天数占过去14个交易日的比例(按照收盘价来算, ts.get_hist_data() 里面有一列 p_change 就可以直接用来计算正负号
			***日K数据，具体如何计算？？***
			[answer] 本支股票在T-14到T-1 p_change>0 的天数 大于 大盘 T-14到T-1 p_change>0 的天数
			满足2个或以上则认为比大盘走势强

	（2）10日均线的斜率为正
			***跟（1）中的一样？***
	（3）5日均线从下开始上穿10日均线：上一日收盘MA5>MA10, 上上交易日收盘 MA5<MA10
			***日K线？***
	（4）过去５个交易日成交量(Volume 那一列）　斜率为正
	     [answer]用收盘价计算：[(T-1)+(T-2)] -[(T-4)+(T-5)] >0
			***日K线？斜率为正的计算公式是啥？***

	以上四点同时满足：SIGNAL = HOLD

3. 更新数据：
		股票代码 名字 决策 买入价 卖出价 日期
		当有buy或者sell的信号时，更新数据


PS： 计算decision的时候需要60分K线，日K，周K数据，所以还是需要先把数据周期性的存储到mysql中去，然后通过读mysql数据计算，然后更新mysql数据
[comment] 不能先把mySQL数据读到缓存(临时的dataframe) ， 作计算，然后再存回mySQL吗？


1. Design mySQL database structure: Able to store daily, hourly, weekly data. Easy to dynamically update 
	everyday/hour/week according to selected stock list.  Need to use TuShare package.  

2. Have the code to update stock list. Have a column to flag "active" and "inactive" stock (using active_flag=1/0). 
	"active" means every run of daily/hourly/weekly data pulling needs to pull data for this stock.

3. Make sure data pulling module can integrate with indicator calculation module, and to update mySQL database with the 
	newest data points

3. Write a module to send e-mail alert and to update a table to flag "buy/sell/hold" signal. The table can be stored 
	locally or on server

4. Prepare back test module. 

5. Search github or other forum to get a code to plot candle stick chart with MA lines (均线) on top of it. 

6. 我用以下代码跑出来的５分钟的数据，无法作日期的比较。能否帮我看一下语法。错误出现在最后一行命令

		import tushare as ts
		import numpy as np
		import pandas as pd
		import datetime
		from __future__ import division
		import matplotlib
		import matplotlib.pyplot as plt
		plt.style.use("ggplot")
		import scipy.stats as stats
		%matplotlib inline

		df_h=ts.get_hist_data(code='000725',ktype='5',start='2018-03-15')
		df_h.reset_index(inplace=True)

		df_h['date']=pd.to_datetime(df_h['date'])
		df_h['date_only']=df_h['date'].dt.date

		sample=df_h[df_h['date_only']<datetime.date('2018-03-20',"%Y-%m-%d")]
		错误提示
		---------------------------------------------------------------------------
		TypeError                                 Traceback (most recent call last)
		<ipython-input-58-d6882cb544f7> in <module>()
		----> 1 sample=df_h[df_h['date_only']<datetime.date('2018-03-20',"%Y-%m-%d")]

		TypeError: an integer is required

========================================================================
[update at 2018-04-22]
========================================================================
以下是从实现角度总结的decision，还有一些问题："***实现及问题***"

股票状态总共两种：EMPTY，HOLD
	初始化股票数据的时候，状态为EMPTY，发出BUY的信号后，状态为HOLD，发出SELL的信号后状态为EMPTY

做decision的逻辑如下

1. 如果股票状态为HOLD：
	（1）某一个小时的收盘价的MA5<MA10
		***日期T，60分K线中的一条数据***
	（2）前一个小时的收盘价MA5>MA10
		***日期T，60分K线中的上一条数据***
	     [answer/comment]日期可能为T, 也可能为T-1。 注意这里是按照交易日，非自然日
	（3）前一日收盘价均线 （MA5-MA10）< 上前一交易日日收盘价均线(MA5-MA10)
		***日期T-1，日k线数据和日期T-2日K线数据比较***
	
	上述三个条件同时满足：SIGNAL = SELL
2. 如果股票状态为EMPTY：
	（1）过去两周走势跟大盘的对比
			10日均线的斜率对比
			***上周，周K线MA10 > 上上周,周K线MA10***
			上一日收盘价和14个交易日前收盘价的对比
			***日K数据，价格满足什么条件？？***
			[answer] (日线T-1收盘价- (T-14)收盘价)/(T-14)收盘价>(大盘T-1收盘点-(T-14)收盘点)/(大盘T-14)收盘点。 注意这里的T-1
			T-14 是按照交易日，并非自然日
			上涨天数占过去14个交易日的比例(按照收盘价来算, ts.get_hist_data() 里面有一列 p_change 就可以直接用来计算正负号
			***日K数据，具体如何计算？？***
			[answer] 本支股票在T-14到T-1 p_change>0 的天数 大于 大盘 T-14到T-1 p_change>0 的天数
			满足2个或以上则认为比大盘走势强

	（2）10日均线的斜率为正
			***跟（1）中的一样？***
	（3）5日均线从下开始上穿10日均线：上一日收盘MA5>MA10, 上上交易日收盘 MA5<MA10
			***日K线？***
	（4）过去５个交易日成交量(Volume 那一列）　斜率为正
	     [answer]用收盘价计算：[(T-1)+(T-2)] -[(T-4)+(T-5)] >0
			***日K线？斜率为正的计算公式是啥？***

	以上四点同时满足：SIGNAL = HOLD

3. 更新数据：
		股票代码 名字 决策 买入价 卖出价 日期
		当有buy或者sell的信号时，更新数据


PS： 计算decision的时候需要60分K线，日K，周K数据，所以还是需要先把数据周期性的存储到mysql中去，然后通过读mysql数据计算，然后更新mysql数据
[comment] 不能先把mySQL数据读到缓存(临时的dataframe) ， 作计算，然后再存回mySQL吗？


任务运行流程：
1. 每天开盘前把存在mySQL表格里的历史数据先取出来(只取stoclklist里面的）放在python缓存里。 日线和60分钟线向前取130个点，周线向前取104个点。
   这几个数字(130,130,104)最好能做成可调的参数。之前计算的indicator 和 decision也是在这个表格里。
   
2. Schedule 每个交易日每个小时运行一次，目的是得到60分钟k线。每次只取最新一个点，append 到 1 里面的60分钟线的表里面。 
   只跑stocklist里面的股票。运行时间定在每个半点往后10分钟， 也就是 10:40am, 11:40am, 2:40pm,3:40pm. 每个新的点出来以后，
   用最新生成的表格(步骤1 + 最新的点)来计算最新这个点的indicator, 然后用decision module 来做决定，更新decision那个 column。 
   可以先暂时用上面的decision logic. 我后续再针对60分钟线做优化。
   
3. 每个交易日结束以后 (4:00pm)运行一次日线， 同样只跑stocklist里面的股票。计算indicator 和 decision的步骤跟上面一样

4. 2 和 3 每次运行完都存回mySQL. 我现在的构想是第2步每天需要存4次mySQL，是为了防止如果缓存出问题丢失计算结果。你可以想想怎么优化这步，
   既留有冗余， 又不会每天读和存4次。
5. 每天update两个decision table. 一个是根据60分钟线做的决定，一个是根据日线做的决定。 这两个decision table都需要以下几个column: 
   股票代码， 日期，时间(60日线的时间可以round to 最近的半点， 比如9:30am, 10:30am. 日线的时间可以统一用3:30pm),
   decision(buy, hold, sell)







