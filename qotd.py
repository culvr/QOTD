#!/usr/local/bin/python2.7
import csv
import socket
import sys


class Quote:
	"""Generic Quote"""
	def __init__(self, quote, author):
		self.quote = quote
		self.author = author
	
	def __repr__(self):
		return "\"{}\"\n\n-{}\n".format(self.quote, self.author)


def load_csv_quotes(path):
	"""Load quotes from csv. Returns an array of quotes."""
	
	try:
		f = open(path, 'r')
		reader = csv.DictReader(f, ('author', 'quote'), delimiter="|")
		
	except IOError, e:
		sys.exit("Unable to open file: {}.".format(e.message))
	
	except csv.Error, e:
		sys.exit(e.message)
	
	return [Quote(**line) for line in reader]
	
	

def quote_cycle(quotes):
	"""Generator to cycle through quotes."""
	while 1:
		for q in quotes:
			yield str(q)

if __name__ == "__main__":
	
	HOST = "localhost"
	PORT = 17
	FILEPATH = "quotes.txt"

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.bind((HOST, PORT))
	s.settimeout(5.0)
	s.listen(5)
	print "QOTD server listening on {}:{}. Press CTRL+C to exit..\n".format(HOST, PORT)
	
	quotes = load_csv_quotes(FILEPATH)
	cycle = quote_cycle(quotes)
	
	while True:
		try:
			conn, addr = s.accept()
			print addr
			conn.send(cycle.next())
			conn.close()
		
		except KeyboardInterrupt:
			s.close()
			break
		
		except socket.timeout:
			pass