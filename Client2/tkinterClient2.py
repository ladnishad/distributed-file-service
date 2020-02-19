#Nishad Lad
#1001633186

import socket
import threading
import os,time
import shutil
import sys
from tkinter import *
from tkinter import messagebox
from functools import partial

window = Tk()
window.title("Client 2 Window")
window.geometry('720x480')
window.update()

UsernameLabel = Label(window, text = "Enter Username")
UsernameLabel.grid(column = 0, row = 0)

userInput = Entry(window, bd =5)
userInput.grid(column = 2, row = 0)

def connectToServer():
    username = str(userInput.get())

    s = socket.socket()

    host = '127.0.0.1'
    port = 5000

    s.connect((host,port))
    #time.sleep(2)
    s.send(bytes(username,encoding='utf-8'))
    #Set connection status label
    ConnectionStatusLabel.config(text = "Connected to server.")
    #Server directory path
    path_to_watch = "Lad_nnl3186/Server"
    #Dictionary to maintain initial state of server directory. it will contain names of files in the directory
    before = dict ([(f, None) for f in os.listdir (path_to_watch)])
    while 1:
        #New dictionary in which filename of new created file will be appended
        after = dict ([(f, None) for f in os.listdir (path_to_watch)])
        added = [f for f in after if not f in before]
        removed = [f for f in before if not f in after]

        if added:
            if os.path.isfile(str(added).replace('[','').replace(']','').replace("'","")):
                ServerStatus.config(text = "Server added file: "+str(added).replace('[','').replace(']','').replace("'","")+" which already exists in directory, no need to download.")
                before = after
            else:
                ServerStatus.config(text = "Server added file: "+str(added).replace('[','').replace(']','').replace("'",""))

                filename = str(added).replace('[','').replace(']','').replace("'","")
                s.send(bytes(filename,encoding='utf-8'))
                data = s.recv(1024)

                if data[:6] == bytes('EXISTS',encoding='utf-8'):
                    filesize = int(data[6:])

                    f = open(filename,'wb')
                    data = s.recv(1024)
                    totalRecv = len(data)
                    f.write(data)

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
