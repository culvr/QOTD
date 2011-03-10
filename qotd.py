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


class QOTD(object):
    """Quote of the Day Server"""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.quotes = self.load_quotes()

    @property
    def next_quote(self):
        return self.quotes.next()
    
        
    def load_quotes(self):
        """Load quotes from csv. Returns an array of quotes."""
        
        try:
            with open(self.filepath, 'r') as f:
                reader = csv.DictReader(f, ('author', 'quote'), delimiter="|")
                quotes = [Quote(**line) for line in reader]
                
        except IOError:
            sys.exit("Could not open file: {}".format(self.filepath))
                
        def quote_generator():
            while 1:
                for q in quotes:
                    yield str(q)
                    
        return quote_generator()
    
    
    def run(self, host="localhost", port=17):
        """Server runloop"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.settimeout(5.0)
        s.listen(5)
        print "QOTD server listening on {}:{}. Press CTRL+C to exit..\n".format(host, port)
        
        while True:
            try:
                conn, addr = s.accept()
                print addr
                conn.send(self.next_quote)
                conn.close()

            except KeyboardInterrupt:
                s.close()
                break

            except socket.timeout:
                pass
        
    

if __name__ == "__main__":
    
    server = QOTD("quotes.txt")
    server.run()
    