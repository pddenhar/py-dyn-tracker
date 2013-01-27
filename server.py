import sqlite3
import pickle
import socket
import atexit

conn = sqlite3.connect('server.db')

c = conn.cursor()

# Set up the server:
server = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
server.bind(( '', 8467))
server.listen(3)

def shutoff():
    print "closing DB"
    conn.close()

atexit.register(shutoff)

def handleConn(channel, details):
    print "Connect from " + str(details[0])
    conData = pickle.loads(channel.recv(1024))
    print conData
    channel.close()

while 1:
    channel, details = server.accept()
    handleConn(channel, details)
