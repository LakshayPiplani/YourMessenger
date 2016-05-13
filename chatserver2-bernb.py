New BSD License

Copyright (c) 2007–2016 The scikit-learn developers.
All rights reserved.


Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

  a. Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.
  b. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.
  c. Neither the name of the Scikit-learn Developers  nor the names of
     its contributors may be used to endorse or promote products
     derived from this software without specific prior written
     permission. 


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.

Copyright (c) 2016 Lakshay Piplani

This file is part of YourMessenger.

YourMessenger is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

YourMessenger is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with YourMessenger.  If not, see <http://www.gnu.org/licenses/>.


import socket, select
import sys
from time import time

import myProcess
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score
import numpy
 

def broadcast_data (sock, message):
    
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                
                socket.close()
                CONNECTION_LIST.remove(socket)

features_train, features_test, labels_train, labels_test = myProcess.preprocess()
clf = BernoulliNB()
to = time()
clf.fit(features_train, labels_train)
print "training time: ", round(time() - to, 3), "s"
t1 = time()
pred = clf.predict(features_test)
print "testing time: ", round(time() - t1, 3), "s"
print accuracy_score(labels_test, pred)

"""def beforeClose(CONNECTION_LIST):
    print 'closing down sockets'
    for sock in CONNECTION_LIST:
        sock.close()

import atexit"""


if __name__ == "__main__":
     
    
    CONNECTION_LIST = []
    RECV_BUFFER = 4096 
    PORT = 5000
    NAMES = {}
    #atexit.register(beforeClose, CONNECTION_LIST) 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
 
    
    CONNECTION_LIST.append(server_socket)
 
    print "Chat server started on port " + str(PORT)
 
    while 1:
        
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                uname = sockfd.recv(RECV_BUFFER)
                CONNECTION_LIST.append(sockfd)
                print "Client {0}, {1} connected".format(str(addr), uname)
                #print "addr is ", addr, " ", type(addr) 
                #print "sock.getpeername is ", sockfd.getpeername(), " ", type(sockfd.getpeername())
                NAMES[addr] = uname
                broadcast_data(sockfd, "+++DONTCLASSIFY%s entered room+++" % uname)
             
            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        if 'ATTN' in data:
                            msg = data[data.find('ATTN')+4 : ]
                            flag = myProcess.add(msg)
                            if flag == True:
                                print '{0} added to dataset'.format(msg)
                            
                        else:
                            """f = (clf.predict(myProcess.predict(data)) == [1])
                            if f == True:
                                label = "SPAM "
                            else:
                                label = ""
                            
                            broadcast_data(sock, "\r" + '<' + NAMES[sock.getpeername()] + '> ' + label + data) #!CHANGE"""
                            prob = clf.predict_proba((myProcess.predict(data)))
                            #print numpy.shape(prob), " ", prob, " ", type(prob)
                            broadcast_data(sock, NAMES[sock.getpeername()] + '+++' + data + '+++' + str(prob[0][1]))  # sending prob of spam               
                 
                except:
                    #print sys.exc_info()
                    broadcast_data(sock, "+++DONTCLASSIFY%s is offline+++" % NAMES[sock.getpeername()])
                    print "Client {0}, {1} is offline".format(str(sock.getpeername()), NAMES[sock.getpeername()]) #!!CHANGE
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
     
    server_socket.close()



    
