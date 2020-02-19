# distributed-file-service

A distributed file service consisting of a server process and three clients. Each client process connects to the server over a socket. The server handles all three clients concurrently. Clients designate a directory on their system to serve as their shared directory. Any file placed into that directory is automatically uploaded to the server. Once the server receives the new file, it sends that file to the remaining clients. Clients place the received file into their shared directory.

There are paths to directories of either server or the client, please change the path to whatever location you’ve saved the files to.

1. Run Server/tkinterServer.py
2. Run Client1/tkinterClient.py -> Enter username, click connect.
3. Run Client2/tkinterClient2.py -> Enter username, click connect.
4. Run Client3/tkinterClient3.py -> Enter username, click connect.

Copy any file in the Server folder. Check for file in the Clients folders.
