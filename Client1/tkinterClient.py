import socket
import threading
import os,time
import shutil
import sys
from tkinter import *
from tkinter import messagebox
from functools import partial

#Creating window
window = Tk()
window.title("Client 1 Window")
window.geometry('720x480')
window.update()

#Label for username
UsernameLabel = Label(window, text = "Enter Username")
UsernameLabel.grid(column = 0, row = 0)

#Entry field to input username
userInput = Entry(window, bd =5)
userInput.grid(column = 2, row = 0)

#Function to connect to server
def connectToServer():
    #Get entered username
    username = str(userInput.get())

    #Create socket object
    s = socket.socket()

    host = '127.0.0.1'
    port = 5000

    #Connection request to server
    s.connect((host,port))
    #Send username to Server
    s.send(bytes(username,encoding='utf-8'))

    #Set connection status label
    ConnectionStatusLabel.config(text = "Connected to server.")

    #Server directory path
    path_to_watch = "path/Server"
    #Dictionary to maintain initial state of server directory. it will contain names of files in the directory
    before = dict ([(f, None) for f in os.listdir (path_to_watch)])
    while 1:
        #New dictionary in which filename of new created file will be appended
        after = dict ([(f, None) for f in os.listdir (path_to_watch)])
        #If there is an extra element in after than before, then new file was created in Server
        added = [f for f in after if not f in before]
        #Else if there is an element in before which is not in after, it means a file was removed from server`
        removed = [f for f in before if not f in after]

        #if a file was added
        if added:
            #if the file exists already in the client's directory, don't download
            if os.path.isfile(str(added).replace('[','').replace(']','').replace("'","")):
                ServerStatus.config(text = "Server added file: "+str(added).replace('[','').replace(']','').replace("'","")+" which already exists in directory, no need to download.")
                #Update before
                before = after
            #Else download file
            else:
                ServerStatus.config(text = "Server added file: "+str(added).replace('[','').replace(']','').replace("'",""))

                filename = str(added).replace('[','').replace(']','').replace("'","")
                #Send the filename to the server
                s.send(bytes(filename,encoding='utf-8'))
                #Get info if file exists in server
                data = s.recv(1024)
                #If exists, start downloading
                if data[:6] == bytes('EXISTS',encoding='utf-8'):
                    filesize = int(data[6:])
                    #Create a new file of the filename
                    f = open(filename,'wb')
                    #Receive file data from server
                    data = s.recv(1024)
                    totalRecv = len(data)
                    #Write the data to the file
                    f.write(data)
                    #if filesize > 1024 run the while loop
                    while totalRecv < filesize:
                        data = s.recv(1024)
                        totalRecv += len(data)
                        f.write(data)
                        DownloadStatusLabel.config(text = "{0:.2f}".format((totalRecv/float(filesize))*100)+"% done")

                    DownloadStatusLabel.config(text = "Download complete")
                else:
                    DownloadStatusLabel.config(text = "File can't be found. Download failed.")

                s.close()

        else:
            ServerStatus.config(text = "No change yet but files might have been removed.")

def startThread():
    threading.Thread(target = connectToServer).start()

submit = Button(window, text ="Connect",command = startThread)
submit.grid(column = 4, row = 0)

ConnectionStatusLabel = Label(window, text = "Waiting to connect.")
ConnectionStatusLabel.grid(column = 0, row = 2)

ServerStatusLabel = Label(window, text = "Server directory status")
ServerStatusLabel.grid(column = 0, row = 4)

ServerStatus = Label(window, text = "")
ServerStatus.grid(column = 0, row = 6)

DownloadStatusLabel = Label(window, text = "")
DownloadStatusLabel.grid(column = 0, row = 8)

window.mainloop()
