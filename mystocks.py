
import csv
import yahoo_finance

'''
loss: 8
	*This is what the CSV looks like:

	5, TTWO', 29.03
	3, 'GPRO', 51.74
	1, 'SHAK', 42.05

'''
class Stock():
	def __init__(self, shares, price, sym ):
		self.shares = shares
		self.price = price
		self.sym = sym
	def spit():
		return {'shares':self.shares, 'price':self.price, 'sym':self.sym}
	def __str__(self):
		return "{}: {}".format(self.sym, float(self.shares)*(self.price))
	def value(self):
		return float(self.shares)*float(self.price)
	def current_value(self):
		s = yahoo_finance.Share(self.sym.upper())
		return float(self.shares) * float(s.get_price())
	def status(self):
		original, current = self.value(), self.current_value()
		if current > original:
			gain = current- original
			loss = False
		else:
			loss = original- current
			gain = False
		if gain:

			return original, current, gain, True, self.sym
		else:
			return original, current, loss, False, self.sym
		
class Portfolio():
	def __init__(self, stocks = []):
		self.stocks = self.initialize_stocks(stocks)

	def initialize_stocks(self, s):
		if not s:
			return []
		stocks = [Stock(int(x[0]), float(x[2]), (x[1])) for x in s]
		return stocks 
	def value(self):
		return sum(i.value() for i in self.stocks)
	def current_value(self):
		return sum(i.current_value() for i in self.stocks)
	def status(self):

		original, current = self.value(), self.current_value()
		print "Original value: {}".format(original)
		print "Current value: {}".format(current)
		if current > original:
			gain = current- original
			loss = False
		else:
			loss = current- original
			gain = False
		if gain:
			print "\tGAIN: + {}".format(gain)
		else:
			print "\tLOSS  {}".format(loss)
	def summary(self):

		print "STOCKS\n"
		print "symbol\tstart\tcurrent\tchng."
		print "____________________________"
		for x in self.stocks:
			summ = x.status()
			if summ[3]:
				print "{}\t{}\t{}\t+{}".format(summ[4],summ[0], summ[1], summ[2])
			else:
				print "{}\t{}\t{}\t-{}".format(summ[4], summ[0], summ[1], summ[2])
		print "____________________________"

				
		print "TOTAL PORTFOLIO\n"
		self.status()
		print "____________________________"
		print


def get_summary():
	p = Portfolio([x for x in csv.reader(open('mystocks.csv','rU'))])

	p.summary()

