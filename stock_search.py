import json
import yahoo_finance
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta as td
import random
from mystocks import get_summary
from stock_info import get_info

'''

Search stocks, get current data, and plot historical closes on matplotlib 


script: 
	http://pastebin.com/4pui2RTe

JSON data file:
	http://pastebin.com/index.php?e=1

'''

buy_watch_list = [\

('CVX', 106),
('HAL', 43),
('IRBT', 29),
('NBG', 1.1),
('YUM',70),
('LXU', 30)


]



def get_data(location = '.'):
	with open('{}/data.json'.format(location), 'rU') as f:
		data = json.load(f)
	return data





def get_difference(d1 , d2):
	out= []
	d1 = datetime.strptime(d1, "%Y-%m-%d")
	d2 = datetime.strptime(d2, "%Y-%m-%d")
	

	delta = d2 - d1

	for i in range(delta.days + 1):
	    out.append(d1 + td(days=i))
	return out

def plot_stock(sym, start_date, end_date= str(datetime.today())[:10]):

	dates = get_difference(start_date, end_date)
	share = yahoo_finance.Share(sym)
	history = share.get_historical(start_date, end_date)
	data = zip([datetime.strptime(i['Date'], "%Y-%m-%d") for i in history], [x for x in reversed([i['Adj_Close'] for i in history])])
	x = [i for i in range(len(data))]
	y = [value for (date, value) in data]

	fig = plt.figure(facecolor='white')
	plt.hold(False)
	font = {'size'   : 7}

	plt.rc('font', **font)

	graph = fig.add_subplot(111)


	# Plot the data as a red line with round markers
	graph.plot(y)

	# Set the xtick locations to correspond to just the dates you entered.
	graph.set_xticks([0, len(data)/2, len(data)])

	# Set the xtick labels to correspond to just the dates you entered.
	labels = [data[-1], data[len(data)/2], data[0]]

	# Set the xtick locations to correspond to just the dates you entered.
	graph.set_xticklabels(
	        [date.strftime("%Y-%m-%d") for (date, value) in labels]
	        )
	plt.show()
	plt.close()


def get_stock_name(sym):
	for x in data:
		if x['Symbol'].lower() == sym.lower():
			return x['Name']
def get_stock_info(sym):

	share = yahoo_finance.Share(sym)
	PRICE, AVERAGE_50, AVERAGE_200, DAY_HIGH, DAY_LOW, PREV_CLOSE, YR_HIGH, YR_LOW, CHANGE, INFO = \
	share.get_price(), share.get_50day_moving_avg(), share.get_200day_moving_avg(), \
	share.get_days_high(), share.get_days_low(), share.get_prev_close(), share.get_year_high(), \
	share.get_year_low(), share.get_change(), share.get_info()	

	payload = dict( zip(['PRICE', 'AVERAGE_50', 'AVERAGE_200', 'DAY_HIGH', 'DAY_LOW', 'PREV_CLOSE', 'YR_HIGH', 'YR_LOW','CHANGE','INFO'], \
		 [PRICE, AVERAGE_50, AVERAGE_200, DAY_HIGH, DAY_LOW, PREV_CLOSE, YR_HIGH, YR_LOW, CHANGE, INFO]))

	for x in data:
		if x['Symbol'] == sym.upper():
			meta = x
			break

	payload.update(meta)
	return payload

def search_company_name(company):
	out = []

	matches = [(x['Symbol'], x['Name']) for x in data if company.lower() in x['Name'].lower()]
	return matches


def search_company_symbol(company):
	out = []
	matches = [(x['Symbol'], x['Name']) for x in data if company.lower() in x['Symbol'].lower()]
	return matches


def main():
	print "Please enter a command...."
	commands = [\
	'search_name [company name] \n\t\t-searches comapnies by the name', \
	'search [company symbol]\n\t\t-searches comapnies by the symbol', \
	'graph [symbol] [yyyy-mm-dd <start date>] [yyyy-mm-dd<end_date> <optional, defaults to today>]\n\t\t -graphs a companies close price',\
	'info [symbol] \n\t\t -prints out the current stock info',
	'more [symbol] \n\t\t -prints out company description and earnings stats',\
	'commands \n\t\t-prints this command list',\
	'random \n\t\t-prints a random stocks info',\
	'mystocks \n\t\t-prints summary of portfolio']
	for x in commands:
		print "\t{}".format(x)
	while True:
		try:
			c = raw_input('Enter a command: ')
			print
			c = c.split(" ")
			if c[0] == 'search_name':
				try:
					for x in (search_company_name(c[1])):
						print x
				except Exception as e:
					print "Error: {}".format(e)
					print "No results or error in your command, please try again"
					pass
			elif c[0] == 'search':
				try:
					for x in  search_company_symbol(c[1]):
						print x
				except Exception as e:
					print "Error: {}".format(e)
					print "No results or error in your command, please try again"
					pass
			elif c[0] == 'graph':
				try:
					if len(c) ==4:
						plot_stock(c[1], c[2], c[3])
					else:
						plot_stock(c[1], c[2])

				except Exception as e:
					print "Error: {}".format(e)
					print "No results or error in your command, please try again"
					pass

					plot_stock(c[1], c[2])
			elif c[0] == 'info':
				try:
					info = get_stock_info(c[1])

					print "({})- {}".format(info['INFO']['symbol'], get_stock_name(info['INFO']['symbol']))
					for k,v in info.items():
						if k not in ['INFO']:
							print '\t',k, v
				except Exception as e:
					print "Error: {}".format(e)
					print "No results or error in your command, please try again"
					pass

			elif c[0] == 'commands':
				for x in commands:
					print "\t{}".format(x)
			elif c[0] == 'random':
				symbols = [x['Symbol'] for x in data]
				r = random.choice(symbols)
				info = get_stock_info(r)

				print "({})- {}".format(info['INFO']['symbol'], get_stock_name(info['INFO']['symbol']))
				for k,v in info.items():
					if k not in ['INFO']:
						print '\t',k, v
				if len(c) ==1:

					plot_stock(r, '2014-06-01')
				else:
					plot_stock(r, c[1])


			elif c[0] == 'watch':
				for stock in buy_watch_list:
					share = yahoo_finance.Share(stock[0])
					if float(share.get_price()) <= float(stock[1]):
						print "BUY {} @ {}".format(stock[0], share.get_price())


			elif c[0] == "mystocks":
				get_summary()
			elif c[0] == 'more':
				moreinfo = get_info(c[1])
				print "COMPANY INFO"
				print moreinfo['description']
				print
				print 'Stats'
				for k, v in moreinfo.items():
					if not k == "description":
						print k, v
			else:
				print "invalid command please try again"
			print



		except Exception as e:
			print "Error: {}".format(e)
			print "something fucked up"
data = get_data()
main()