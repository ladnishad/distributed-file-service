import socket
import threading
import os,time
import shutil
import sys
from tkinter import *
from tkinter import messagebox

window = Tk()
window.title("Server Window")
window.geometry('720x480')
window.update()

serverStatusLabel = Label(window, text = "Starting the server.")
serverStatusLabel.grid(column = 0, row = 0)

client1StatusLabel = Label(window, text = "Waiting for client to connect")
client1StatusLabel.grid(column = 0, row = 2)

client1ChangeLabel = Label(window, text = "No change yet.")
client1ChangeLabel.grid(column = 2, row = 2)

client2StatusLabel = Label(window, text = "Waiting for client to connect")
client2StatusLabel.grid(column = 0, row = 4)

client2ChangeLabel = Label(window, text = "No change yet.")
client2ChangeLabel.grid(column = 2, row = 4)

client3StatusLabel = Label(window, text = "Waiting for client to connect")
client3StatusLabel.grid(column = 0, row = 6)

client3ChangeLabel = Label(window, text = "No change yet.")
client3ChangeLabel.grid(column = 2, row = 6)

clientDirectoryStatus = Label(window, text = "No directories to watch")
clientDirectoryStatus.grid(column = 0, row = 8)

serverDownloadStatus1 = Label(window, text = "Nothing new downloaded from Client 1")
serverDownloadStatus1.grid(column = 0, row = 10)

serverDownloadStatus2 = Label(window, text = "Nothing new downloaded from Client 2")
serverDownloadStatus2.grid(column = 0, row = 11)

serverDownloadStatus3 = Label(window, text = "Nothing new downloaded from Client 3")
serverDownloadStatus3.grid(column = 0, row = 12)

#Function to send file to client
def getFileForClientOne(name,sock):
    #Storing the filename
    username = str(sock.recv(1024),'utf-8')
    client1StatusLabel.config(text = str(username).replace("'","")+" connected")
    window.update()

    filename = str(sock.recv(1024),'utf-8')
    #To check if the file still exists in the server directory
    if os.path.isfile(filename):
        sock.send(bytes("EXISTS "+str(os.path.getsize(filename)),encoding='utf-8'))
        #Reading bytes of file
        with open(filename, 'rb') as f:
            #Reading 1024 bytes and storing in bytesToSend
            bytesToSend = f.read(1024)
            #Sending the stored bytes through socket
            sock.send(bytesToSend)
            #Repeating the process till no bytes left as some files can be more than 1024 Bytes
            while bytesToSend != "":
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
    else:
        #If the file no longer exists, send error.
        sock.send(bytes("ERR",encoding='utf-8'))
    #Closing the socket
    sock.close()

def getFileForClientTwo(name,sock):
    #Storing the filename
    username = str(sock.recv(1024),'utf-8')
    #arr.append(str(sock.recv(1024),'utf-8'))

    client2StatusLabel.config(text = str(username).replace("'","")+" connected")
    window.update()

    filename = str(sock.recv(1024),'utf-8')
    #To check if the file still exists in the server directory
    if os.path.isfile(filename):
        sock.send(bytes("EXISTS "+str(os.path.getsize(filename)),encoding='utf-8'))
        #Reading bytes of file
        with open(filename, 'rb') as f:
            #Reading 1024 bytes and storing in bytesToSend
            bytesToSend = f.read(1024)
            #Sending the stored bytes through socket
            sock.send(bytesToSend)
            #Repeating the process till no bytes left as some files can be more than 1024 Bytes
            while bytesToSend != "":
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
    else:
        #If the file no longer exists, send error.
        sock.send(bytes("ERR",encoding='utf-8'))
    #Closing the socket
    sock.close()


def getFileForClientThree(name,sock):
    #Storing the filename
    username = str(sock.recv(1024),'utf-8')
    #arr.append(str(sock.recv(1024),'utf-8'))

    client3StatusLabel.config(text = str(username).replace("'","")+" connected")
    window.update()

    filename = str(sock.recv(1024),'utf-8')
    #To check if the file still exists in the server directory
    if os.path.isfile(filename):
        sock.send(bytes("EXISTS "+str(os.path.getsize(filename)),encoding='utf-8'))
        #Reading bytes of file
        with open(filename, 'rb') as f:
            #Reading 1024 bytes and storing in bytesToSend
            bytesToSend = f.read(1024)
            #Sending the stored bytes through socket
            sock.send(bytesToSend)
            #Repeating the process till no bytes left as some files can be more than 1024 Bytes
            while bytesToSend != "":
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
    else:
        #If the file no longer exists, send error.
        sock.send(bytes("ERR",encoding='utf-8'))
    #Closing the socket
    sock.close()

def client1Process(s):
    c, addr = s.accept()
    #Creating thread for the client
    t = threading.Thread(target = getFileForClientOne, args = ("retrThread", c))
    #Starting the thread
    t.start()

    clientDirectoryStatus.config(text = "Watching client directories for new files.")
    path_to_watch = "path/Client1"

    #Constant list to maintain file names in the directory of first client in the initial stage
    before = dict ([(f, None) for f in os.listdir (path_to_watch)])

    while 1:
      #Variable List : File names are added or removed from this list if a file is added or removed in client1's directory
      after = dict ([(f, None) for f in os.listdir (path_to_watch)])
      #Iterating over after and before. If a filename is present in after but not in before, that means it is a newly added file.
      added = [f for f in after if not f in before]
      #Iterating over after and before. If a filename is present in before but not in after, that means the file is removed.
      removed = [f for f in before if not f in after]

      if added:
          client1ChangeLabel.config(text = "Added "+str(added).replace('[','').replace(']','').replace("'",""))

          #Cleaning the filename
          clientFileName = str(added).replace('[','').replace(']','').replace("'","")

          sourceFile = 'path/Client1/'+clientFileName
          dest = 'path/Server'
          if os.path.isfile(str(added).replace('[','').replace(']','').replace("'","")):
              before = after
          else:
            try:
                shutil.copy(sourceFile,dest)
                serverDownloadStatus1.config(text = "File named "+str(added).replace('[','').replace(']','').replace("'","")+" uploaded by a client.")

            except IOError as e:
                serverDownloadStatus1.config(text = "File download failed. Error: %s" % e)

            except:
                serverDownloadStatus1.config(text = "Unexpected error occurred.")

      #If file is removed,
      if removed:
          #Display client name and name of file
          print("Client <" + str(addr) + "> removed "+str(removed))

      #before set to after to reflect file removal
      before = after

def client2Process(s):

    d, addr2 = s.accept()
    #Creating thread for the client
    t1 = threading.Thread(target = getFileForClientTwo, args = ("retrThread1", d))
    #Starting the thread
    t1.start()

    path_to_watch2 = "path/Client2"

    #Constant list to maintain file names in the directory of first client in the initial stage
    before1 = dict ([(f, None) for f in os.listdir (path_to_watch2)])

    while 1:
      #Variable List : File names are added or removed from this list if a file is added or removed in client1's directory
      after1 = dict ([(f, None) for f in os.listdir (path_to_watch2)])
      #Iterating over after and before. If a filename is present in after but not in before, that means it is a newly added file.
      added1 = [f for f in after1 if not f in before1]
      #Iterating over after and before. If a filename is present in before but not in after, that means the file is removed.
      removed1 = [f for f in before1 if not f in after1]

      if added1:
          client2ChangeLabel.config(text = "Added "+str(added1).replace('[','').replace(']','').replace("'",""))

          #Cleaning the filename
          clientFileName1 = str(added1).replace('[','').replace(']','').replace("'","")

          sourceFile1 = 'path/Client2/'+clientFileName1
          dest1 = 'path/Server'
          if os.path.isfile(str(added1).replace('[','').replace(']','').replace("'","")):
              before1 = after1
          else:
            try:
                shutil.copy(sourceFile1,dest1)
                serverDownloadStatus2.config(text = "File named "+str(added1).replace('[','').replace(']','').replace("'","")+" uploaded by a client.")

            except IOError as e:
                serverDownloadStatus2.config(text = "File download failed. Error: %s" % e)

            except:
                serverDownloadStatus2.config(text = "Unexpected error occurred.")

      #If file is removed,
      if removed1:
          #Display client name and name of file
          print("Client at <" + str(addr2) + "> removed "+str(removed1))

      #before set to after to reflect file removal
      before1 = after1


def client3Process(s):

    e, addr3 = s.accept()
    #Creating thread for the client
    t2 = threading.Thread(target = getFileForClientThree, args = ("retrThread2", e))
    #Starting the thread
    t2.start()

    path_to_watch3 = "path/Client3"

    #Constant list to maintain file names in the directory of first client in the initial stage
    before2 = dict ([(f, None) for f in os.listdir (path_to_watch3)])

    while 1:
      #Variable List : File names are added or removed from this list if a file is added or removed in client1's directory
      after2 = dict ([(f, None) for f in os.listdir (path_to_watch3)])
      #Iterating over after and before. If a filename is present in after but not in before, that means it is a newly added file.
      added2 = [f for f in after2 if not f in before2]
      #Iterating over after and before. If a filename is present in before but not in after, that means the file is removed.
      removed2 = [f for f in before2 if not f in after2]

      if added2:
          client3ChangeLabel.config(text = "Added "+str(added2).replace('[','').replace(']','').replace("'",""))

          #Cleaning the filename
          clientFileName2 = str(added2).replace('[','').replace(']','').replace("'","")

          sourceFile2 = 'path/Client3/'+clientFileName2
          dest2 = 'path/Server'
          if os.path.isfile(str(added2).replace('[','').replace(']','').replace("'","")):
              before2 = after2
          else:
            try:
                shutil.copy(sourceFile2,dest2)
                serverDownloadStatus3.config(text = "File named "+str(added2).replace('[','').replace(']','').replace("'","")+" uploaded by a client.")

            except IOError as e:
                serverDownloadStatus3.config(text = "File download failed. Error: %s" % e)

            except:
                serverDownloadStatus3.config(text = "Unexpected error occurred.")

      #If file is removed,
      if removed2:
          #Display client name and name of file
          print("Client at <" + str(addr3) + "> removed "+str(removed2))

      #before set to after to reflect file removal
      before2 = after2


def Main():
    #Server IP and port number
    host = '127.0.0.1'
    port = 5000
    #Creating socket
    s = socket.socket()
    s.bind((host,port))

    serverStatusLabel.config(text = "Server started")
    window.update()
    #Listening to only maximum 3 connections
    s.listen(3)

    #While the connection is up
    while True:
        threading.Thread(target = client1Process,args = (s,)).start()
        threading.Thread(target = client2Process,args = (s,)).start()
        threading.Thread(target = client3Process,args = (s,)).start()
    #Closing the Socket
    s.close()

if __name__ == '__main__':
    #Calling the main function
    threading.Thread(target = Main).start()
    window.mainloop()
