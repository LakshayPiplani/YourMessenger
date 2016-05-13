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


import socket, select, string, sys
from PyQt4 import QtGui
import logindesign2
import chatdesign
from PyQt4.QtCore import QThread, SIGNAL
from sklearn.naive_bayes import BernoulliNB
import cPickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectPercentile, f_classif
from datetime import datetime
import numpy
import string


class ListWidgetItemWithDate(QtGui.QListWidgetItem):
    def __init__(self, parent = None):
        super(ListWidgetItemWithDate, self).__init__(parent)
        self.dt = 'date not yet set'
        self.setDate()
    def setDate(self):
        self.dt = datetime.today()
    def getDate(self):
        return self.dt

class LoginDialog(QtGui.QDialog, logindesign2.Ui_Dialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)
        self.setupUi(self)

class ChatAppWindow(QtGui.QMainWindow, chatdesign.Ui_MainWindow):
    def __init__(self, uname, parent=None):
        super(ChatAppWindow, self).__init__(parent)
        self.setupUi(self)
        self.uname = uname

        self.newHam = 0
        self.newSpam = 0
        
        self.pushButton.clicked.connect(self.sendText)
        self.pushButton_2.clicked.connect(self.sendCorrectBack)
        self.connect(self.tabWidget, SIGNAL("currentChanged(int)"), self.changeTabText)

        self.host = 'localhost'
        self.port = 5000
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(2)
        self.connectServer()

    def changeTabText(self, i):
        if i == self.tabWidget.indexOf(self.spamTab):
            self.tabWidget.setTabText( i, "Spam Inbox")
            self.newSpam = 0
        else:
            self.tabWidget.setTabText( i, "Conversation")
            self.newHam = 0

    def connectServer(self):
        try :
            self.s.connect((self.host, self.port))
        except :
            #print 'Unable to connect'
            #sys.exit() #show a dialog
            print sys.exc_info()
            QtGui.QMessageBox.information(self, "unable to connect!", "unable to connect!")
        self.s.send(self.uname)
        self.get_thread = GetFromServer(self.s)
        self.connect(self.get_thread, SIGNAL("add_text(PyQt_PyObject)"), self.add_text)
        self.get_thread.start()


    def sendCorrectBack(self):
        curListWidget = self.tabWidget.currentWidget().findChild(QtGui.QListWidget)
        curItem = curListWidget.currentItem()
        txt = str(curItem.text())
        
        if 'SPAM' in txt:
            i = txt.find('SPAM')
            lab = 'ham'
            msg = txt[i+5: ]
            self.s.send('ATTNham ' + msg)
            itemObj = curListWidget.takeItem (curListWidget.row(curItem) )
            otherListWidget = self.tabWidget.widget( self.tabWidget.indexOf(self.hamTab) ).findChild(QtGui.QListWidget) #.addItem(txt[ : txt.find('SPAM') ] + txt[txt.find('SPAM')+len('SPAM') + 1 :] )
            itemObj.setText( txt[ : txt.find('SPAM') ] + txt[txt.find('SPAM')+len('SPAM') + 1 :] )

            otherListWidget.addItem(itemObj)
            del itemObj

        else:   
            i = txt.find('>')
            lab = 'spam'
            msg = txt[i+2: ]  # change!
            self.s.send('ATTNspam ' + msg) 
            itemObj = curListWidget.takeItem (curListWidget.row(curItem) )
            otherListWidget = self.tabWidget.widget( self.tabWidget.indexOf(self.spamTab) ).findChild(QtGui.QListWidget)#.addItem(txt[ : txt.find('>')+1 ] + " SPAM" + txt[txt.find('>')+ 1 :] ) 
            itemObj.setText( txt[ : txt.find('>')+1 ] + " SPAM" + txt[txt.find('>')+ 1 :] )
            otherListWidget.addItem(itemObj)

            del itemObj

        self.get_thread2 = updateDataset(msg, lab)   
        self.get_thread2.start()                

    def add_text(self, args):
        curPageWidget = self.tabWidget.currentWidget()
        if args[1] == 'spam':
            print 'message is spam'
            itemObj = ListWidgetItemWithDate()
            itemObj.setText(args[0])
            self.listWidget_Spam.addItem(itemObj)
            if curPageWidget != self.listWidget_Spam.parent():
                self.newSpam += 1
                self.tabWidget.setTabText( self.tabWidget.indexOf(self.spamTab), "Spam Inbox (" + str(self.newSpam) + ")" )
        elif args[1] == 'ham':
            print 'message is ham'
            itemObj = ListWidgetItemWithDate()
            itemObj.setText(args[0])
            self.listWidget.addItem(itemObj)
            if curPageWidget != self.listWidget.parent():
                self.newHam += 1
                self.tabWidget.setTabText( self.tabWidget.indexOf(self.hamTab), "Conversation (" + str(self.newHam) + ")" )
        # add logic for disabling send button
        

    def sendText(self):
        txt = str(self.lineEdit.text())
        self.add_text( ('<YOU at '+ datetime.today().strftime("%d/%m/%y %H:%M") + ' > ' + txt, 'ham') ) # add You >>
        self.lineEdit.clear()
        self.s.send(txt) # add <you>
        

            
class GetFromServer(QThread):
    def __init__(self, sock):
        QThread.__init__(self)
        self.s = sock
        self.clf = BernoulliNB()
        self.vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words='english')
        #self.selector = SelectPercentile(f_classif, percentile=50)
        self.flag = 0

    def run(self):
        self.processModel()
        while 1:
            try:
                data = self.s.recv(4096)
                if not data :
                    self.emit(SIGNAL('add_text(PyQt_PyObject)'), 'Disconnected from chat server')
                    self.terminate()
                else :
                    print data
                    name, msg, probServer = data.split('+++')
                    print 'name, msg, probServer is {0}, {1}, {2}'.format(name, msg, probServer)
                    if 'DONTCLASSIFY' in msg:
                        label = ""
                        msg = msg[msg.find('DONTCLASSIFY') + len('DONTCLASSIFY') : ]
                        spamORham = 'ham'
                    elif self.flag == 1:
                        probServer = float(probServer)
                        l = []
                        l.append(msg)
                        textSparseVec = self.vectorizer.transform(l).toarray()
                        #textTrans = self.selector.transform(textSparseVec).toarray()
                        probClient = self.clf.predict_proba(textSparseVec)[0][1]
                        p = 0.6*(probClient)+ 0.4*(probServer)
                        print 'client prob is ', self.clf.predict_proba(textSparseVec)
                        print 'combined prob is ', p
                        if p >= 0.5:
                            label = "SPAM "
                            spamORham = 'spam'
                        else:
                            label = ""
                            spamORham = 'ham'
                        name = '<' + name + " at " + datetime.today().strftime("%d/%m/%y %H:%M") + ' > '
                    else:
                        print 'server prob is ', probServer
                        if float(probServer) >= 0.5:
                            print 'probServer is >= 0.5'
                            label = "SPAM "
                            spamORham = 'spam'
                        else:
                            label = ""
                            spamORham = 'ham'
                        name = '<' + name + " at " + datetime.today().strftime("%d/%m/%y %H:%M") + ' > '

                    self.emit( SIGNAL('add_text(PyQt_PyObject)'), (str(name + label + msg), spamORham) )
            #except IndexError:
                #print sys.exc_info()
            except:
                pass

    def processModel(self):
        f = open('clientTxt.pkl', 'r')
        emails = cPickle.load(f)
        f.close()

        f = open('clientLab.pkl', 'r')
        labels = cPickle.load(f)
        f.close()

        twoClasses = (0 in labels) and (1 in labels)

        if len(emails) >= 5 and twoClasses:
            
            self.flag = 1
            try:
                features_train_transformed = self.vectorizer.fit_transform(emails).toarray() #If all traning messages are same, after pruning, no terms remain
                #Value Error is thrown
            

            
            #self.selector.fit(features_train_transformed, labels)
            #features_train_transformed = self.selector.transform(features_train_transformed).toarray()

                self.clf.fit(features_train_transformed, labels)
            except ValueError:
                print sys.exc_info()
                self.flag = 0

class updateDataset(QThread):
    def __init__(self, txt, lab):
        QThread.__init__(self)
        self.txt = txt
        self.lab = lab

    def run(self):
        f1 = open('clientTxt.pkl' , 'r')
        emails = cPickle.load(f1)
        f1.close()
        words = self.txt.split()
        words_proc = [ word.strip(string.punctuation).lower() for word in words ]

        cnt = 0
        for x in words_proc:
            if x == "":
                cnt += 1
        for i in range(0, cnt):
            words_proc.remove('')
        text = string.join(words_proc)
        
        if emails.count(text) < (0.4 * len(emails)):
            
            emails.append(text)
            f1 = open('clientTxt.pkl' , 'w')
            cPickle.dump(emails, f1)
            f1.close()

            f2 = open('clientLab.pkl', 'r')
            labels = cPickle.load(f2)
            f2.close()
            if (self.lab == 'ham'):
                labels.append(0)
            else:
                labels.append(1)
            f2 = open('clientLab.pkl', 'w')
            cPickle.dump(labels, f2)
            f2.close()



        




if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    login = LoginDialog()
    if not login.exec_(): # 'reject': user pressed 'Cancel', so quit
        sys.exit(-1)      

    # 'accept': continue
    main = ChatAppWindow(str(login.userName.text()))
   
    main.show()

    app.exec_()


