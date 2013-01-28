import ConfigParser
import os
import pickle
import socket
import time

config = ConfigParser.RawConfigParser()
config.readfp(open("client.conf"))

server = config.get('client','server')
update_frequency = int(config.get('client','update_frequency'))
hostname = ""
if(config.has_option('client',"hostname")):
    hostname = config.get('client','hostname')
else:
    hostname = socket.gethostname() 

def sendIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server,8467))
    ip = s.getsockname()[0]
    #print(ip)
    pickledData = pickle.dumps([ip, hostname])
    
    s.send(pickledData)
    
    s.close()

while(1):
    try:
        sendIP()
    except:
        print "Could not connect to server, will try again in " + str(update_frequency) + " seconds."
    time.sleep(update_frequency)
