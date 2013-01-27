import sqlite3
import pickle
import socket
import atexit

conn = sqlite3.connect('server.db')

c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS updates (update_time TEXT, id INTEGER PRIMARY KEY, IP text, hostname TEXT)''')

# Set up the server:
server = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
server.bind(( '', 8467))
server.listen(3)

def shutoff():
    print "closing DB"
    conn.close()

atexit.register(shutoff)

def handleConn(channel, details):
    #print "Connect from " + str(details[0])
    conData = pickle.loads(channel.recv(1024))
    t = (conData[0], conData[1])
    print t
    c.execute("INSERT INTO updates (update_time, IP, hostname) VALUES (datetime(), ?, ?);",t)
    conn.commit()
    channel.close()

while 1:
    channel, details = server.accept()
    handleConn(channel, details)
