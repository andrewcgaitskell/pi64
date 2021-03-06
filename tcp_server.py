
# python3

import socket

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import wget
import os
from sqlalchemy import create_engine
import psycopg2

import os

import time

engine = create_engine('postgresql://pythonuser:pythonuser@localhost:5432/data')

# Create server socket.
serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#serv_sock.settimeout(10)


# Bind server socket to loopback network interface.
serv_sock.bind(('', 5010))

# Turn server socket into listening mode.
serv_sock.listen(10)
index = 0

###
"""
try:
    while 1:
        newSocket, address = sock.accept(  )
        print "Connected from", address
        # loop serving the new client
        while 1:
            receivedData = newSocket.recv(1024)
            if not receivedData: break
            # Echo back the same data you just received
            newSocket.send(receivedData)
        newSocket.close(  )
        print "Disconnected from", address
finally:
    sock.close(  )
####
"""
def macstring(sensorbytes_in):
    mac0_string = hex(sensorbytes_in[3])[2:].zfill(2)
    mac1_string = hex(sensorbytes_in[4])[2:].zfill(2)
    mac2_string = hex(sensorbytes_in[5])[2:].zfill(2)
    mac3_string = hex(sensorbytes_in[6])[2:].zfill(2)
    mac4_string = hex(sensorbytes_in[7])[2:].zfill(2)
    mac5_string = hex(sensorbytes_in[8])[2:].zfill(2)
    full_mac = mac5_string + ":" + mac4_string + ":" + mac3_string + ":" + mac2_string + ":" + mac1_string + ":" + mac0_string
    return full_mac
##print("The square of the sum of 2 and 3 is : ", nsquare(2, 3))


while True:
    # Accept new connections in an infinite loop.
    client_sock, client_addr = serv_sock.accept()
    print('New connection from', client_addr)

    chunks = []
    while True:
        content = client_sock.recv(9)
        #print(type(content))
        if len(content) ==0:
           break

        else:
            ##print(content)
            try:
                sensorbytes = list(content)
                band = sensorbytes[0]
                sensorvalue = sensorbytes[1] * 256 + sensorbytes[2]

                #mac0_string = hex(sensorbytes[3])[2:].zfill(2)
                #mac1_string = hex(sensorbytes[4])[2:].zfill(2)
                #mac2_string = hex(sensorbytes[5])[2:].zfill(2)
                #mac3_string = hex(sensorbytes[6])[2:].zfill(2)
                #mac4_string = hex(sensorbytes[7])[2:].zfill(2)
                #mac5_string = hex(sensorbytes[8])[2:].zfill(2)

                #full_mac = mac5_string + ":" + mac4_string + ":" + mac3_string + ":" + mac2_string + ":" + mac1_string + ":" + mac0_string
                full_mac = macstring(sensorbytes)

                ##sensorvalue = int.from_bytes(sensorcontet, byteorder='big')
                #print("band:", band, " sensor value:",sensorvalue)
                index = index + 1
                sqlcmnd = f"INSERT INTO public.raw_sensordata_with_mac(index, millitime, band, value, mac)\
                VALUES ({index}, EXTRACT(EPOCH FROM (SELECT NOW())) * 1000, {band}, {sensorvalue}, '{full_mac}')"

                #sqlcmnd = 'COPY "raw_CovidTrackerGantt" FROM \''+ filename + '\' DELIMITER \',\' CSV;'
                with engine.connect().execution_options(autocommit=True) as con:
                  con.execute(sqlcmnd)
            except:
                pass
            #print(sqlcmnd)
            #time.sleep(1) # Sleep for 3 seconds
            #client_sock.sendall(b''.join(chunks))
    ##client_sock.close()
    ##print("Disconnected from", client_addr)
                
