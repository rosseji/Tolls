import SocketServer
import re

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        while True:
            data = self.request.recv(4096).strip()
            if not data:
                break
            print "{} wrote:".format(self.client_address[0])
            print data
            if re.search('[a-zA-Z]', data) == False:
                dataList = [int(x) for x in data.split(',')]
                print dataList
            #else:
                #nameList = data
                #print nameList
            # resend the data to test connection
            self.request.sendall("Connection is working good job Ben")

if __name__ == "__main__":
    #thanks Mitchell!
    HOST, PORT = "137.154.224.245", 4628
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()