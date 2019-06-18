
import signal
import socket
import threading
import sys
import ssl
# import http.client
from BlockDomain import Send403Message
from BlockWord import Send403Word
from BlockHour import Send403Hour
from Cache import cache_sites_write
from Cache import cache_sites_open

class ServerProxy():

    def __init__(self, HOST, PORT):

        # Shutdown on Ctrl+C
        signal.signal(signal.SIGINT, self.shutdown) 

        # Create a TCP socket
        self.main_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Re-use the socket
        self.main_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind the socket to a public host, and a port   
        self.main_server.bind((HOST,PORT))

        self.main_server.listen(10) # become a server socket
        self.__clients = {}

        while True:

            # Establish the connection
            (clientSocket, client_address) = self.main_server.accept() 

            print("Connection established with {0} ".format(client_address))

            #Create Thread for each established connection
            thread_proxy = threading.Thread(   name=client_address, 
                                    target = self.proxy, 
                                    args=(clientSocket, client_address))
            thread_proxy.setDaemon(True)
            thread_proxy.start()
        
        self.serverSocket.close()

    def proxy(self,conn,address):
        # get the request from browser
        request = conn.recv(2048)

        try:
            request_in_string = request.decode('utf_8')
        except UnicodeDecodeError:
            print("UnicodeDecodeError: 'utf-8' codec can't decode byte 0xf6 in position 370: invalid start byte")

        # parse the first line
        first_line = request_in_string.split('\n')[0]
        print("FIRST LINE")
        print(first_line)

        #get http type
        http_line_first = first_line.split(' ')[0]

        if first_line == "":
            print("\x1b[1;31mNOTHING IN REQUEST - @first_line\x1b[0;0m")
        else:

            # get url
            url = first_line.split(' ')[1]

            # cache_sites_open(url)

            http_pos = url.find("://") # find pos of ://

            if (http_pos==-1):
                temp = url
            else:
                temp = url[(http_pos+3):] # get the rest of url

            port_pos = temp.find(":") # find the port pos (if any)

            # find end of web server
            webserver_pos = temp.find("/")
            if webserver_pos == -1:
                webserver_pos = len(temp)

            webserver = ""
            port = -1
            if (port_pos==-1 or webserver_pos < port_pos): 

                # default port 
                port = 80 
                webserver = temp[:webserver_pos]

            else: # specific port 
                port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
                webserver = temp[:port_pos]
            
            x = cache_sites_open(webserver)

            msg =[]
            #verify if url is blocked
            msg = Send403Message(webserver)

            #block by url
            if msg != "OK":
                if http_line_first != 'CONNECT':
                    #Working
                    for line in msg:
                        conn.sendall(line.encode())
                    msg = []
                    conn.close()
                else:
                    #TODO treatment for https
                    print("-----HTTPS HERE-----")
                    conn.sendall(b"HTTP/1.1 200 OK\nAccept:text/html\nConnection: close\r\n\r\n")
                    reply = conn.recv(2048)
                    conn.sendall(b'<!DOCTYPE html>\n<html>\n<body>\n<h1>hello world</h1>\n</body>\n</html>\r\n\r\n')
                    conn.close()

            msg =[]
            word_block=[]

            #block by word
            word_block = Send403Word(first_line)

            if word_block != "OK":
                if http_line_first != 'CONNECT':
                    for line in word_block:
                        conn.sendall(line.encode())
                    word_block = []
                    conn.close()
                else:
                    #TODO treatment for https
                    # conn.sendall(b"HTTP/1.1 200 OK\nAccept:text/html\nConnection: close\r\n\r\n")
                    # reply = conn.recv(2048)
                    conn.sendall(b'<!DOCTYPE html>\n<html>\n<body>\n<h1>hello world</h1>\n</body>\n</html>\r\n\r\n')
                    conn.close()
            word_block = []
            hour_block = []

            #TODO block by hour
            hour_block = Send403Hour(address[0])
            if hour_block != "OK":
                if http_line_first != 'CONNECT':
                    for line in hour_block:
                        conn.sendall(line.encode())
                    hour_block = []
                    conn.close()
                else:
                    #TODO treatment for https
                    print("-----HTTPS HERE-----")
                    conn.sendall(b"HTTP/1.1 200 OK\nAccept:text/html\nConnection: close\r\n\r\n")
                    reply = conn.recv(2048)
                    conn.sendall(b'<!DOCTYPE html>\n<html>\n<body>\n<h1>hello world</h1>\n</body>\n</html>\r\n\r\n')
                    conn.close()
            hour_block = []
            #send to internet, get page, send to user the rendered page

            #cache, if not working delete
            if x != "NOT":
                for i in x:
                    conn.send(x.encode())
            
            if(http_line_first == 'CONNECT'):

                #If its and HTTPS page and needs tunneling
                HOST = webserver
                PORT = 443

                MySock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                MySock.settimeout(2000)
                # MySock = ssl.wrap_socket(MySock, ssl_version=ssl.PROTOCOL_TLSv1_2)
                try:
                    MySock.connect((HOST,PORT))
                except:
                    print("\x1b[1;31mNODE NAME ERROR - @MySock \x1b[0;0m")
                
                reply = "HTTP/1.0 200 Connection established\r\n"
                # reply += "Proxy-agent: Pyx\r\n"
                reply += "\r\n"
                try:
                    conn.sendall( reply.encode() )
                except OSError:
                    print("\x1b[1;31mBAD FILE DESCRIPTOR - errno9 \x1b[0;0m")
                
                conn.setblocking(0)
                MySock.setblocking(0)

                while True:
                    try:
                        request = conn.recv(1024)
                        MySock.sendall( request )
                    except socket.error as err:
                        pass
                    try:
                        reply = MySock.recv(1024)
                        conn.sendall( reply )
                    except socket.error as err:
                        pass
                conn.close()
                MySock.close()

            else:
                #Normal http page
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                client_socket.settimeout(2000)
                try:
                    client_socket.connect((webserver, port))
                except:
                    print("\x1b[1;31mNODE NAME ERROR - @client_socket \x1b[0;0m")

                try:
                    client_socket.sendall(request)
                except BrokenPipeError:
                    print("\x1b[1;31mBROKEN PIPE ERROR \x1b[0;0m")
                
                while 1:
                    # receive data from web server
                    try:
                        data = client_socket.recv(2048)
                    except ConnectionResetError:
                        print("\x1b[1;31mCONNECTION RESET BY PEER - errno54 \x1b[0;0m")
                    
                    #write to cache/http
                    cache_sites_write(webserver,str(data))
                    
                    if (len(data) > 0):
                        try:
                            conn.send(data) # send to browser/client
                        except BrokenPipeError:
                            print("\x1b[1;31mBROKEN PIPE ERROR \x1b[0;0m")
                        except OSError:
                            print("\x1b[1;31mBAD FILE DESCRIPTOR - errno9 \x1b[0;0m")
                    else:
                        break
            
                conn.close()
                client_socket.close()
    
    #shutdown program
    def shutdown(self,signum, frame):
        print('\nShutdown called with signal', signum)
        sys.exit(1)
