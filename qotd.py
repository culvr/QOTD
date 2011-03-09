#!/usr/bin/python

import socket

HOST = "localhost"
PORT = 17

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.settimeout(5.0)
s.listen(5)
print "QOTD server listening on {}:{}. Press CTRL+C to exit..\n".format(HOST, PORT)

class Quote:
	"""Generic Quote"""
	def __init__(self, msg, author="Unknown"):
		self.msg = msg
		self.author = author
	
	def __repr__(self):
		return "\"{}\"\n\n-{}\n".format(self.msg, self.author)


# Gross hardcoded quotes.
q1 = """They're the best at what they do and I'm the best at what I do.
And together it's like, it's on. Sorry, Middle America. Yeah, I said it."""

q2 = """I'm so tired of pretending like my life isn't just perfect
and just winning every second, and I'm not just perfect
and bi**hing and just delivering the goods at every frickin' turn."""

q3 = """I have a 10,000-year-old brain and the boogers of a 7-year-old.
That's how I describe myself."""

author = "Charlie Sheen"

quotes = []
quotes.append(Quote(q1, author))
quotes.append(Quote(q2, author))
quotes.append(Quote(q3, author))				


def get_quote():
	"""Generator to cycle through quotes."""
	while 1:
		for q in quotes:
			yield str(q)

quote_list = get_quote()

while True:
	try:
		conn, addr = s.accept()
		print addr
		conn.send(quote_list.next())
		conn.close()
		
	except KeyboardInterrupt:
		s.close()
		break
		
	except socket.timeout:
		pass