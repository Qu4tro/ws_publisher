from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

import _thread
import threading
import sys


class WsPublisher(threading.Thread):
    def __init__(self, remind=True):
        super(WsPublisher, self).__init__()
        self.remind = bool(remind)
        self.last_message = None
        self.clients = {}

    def run(self):
        for line in sys.stdin:
            line = line.rstrip()
            self.last_message = line
            for client in self.clients:
                self.clients[client].sendMessage(line)
        _thread.interrupt_main()

    def add_client(self, client):
        self.clients[id(client)] = client
        if self.remind and self.last_message is not None:
            client.sendMessage(self.last_message)

    def rm_client(self, client):
        del self.clients[id(client)]


ws_publisher = WsPublisher()


class SubscriptionHandler(WebSocket):
    def handleMessage(self):
        ...

    def handleConnected(self):
        ws_publisher.add_client(self)
        print(self.address, 'connected')

    def handleClose(self):
        ws_publisher.rm_client(self)
        print(self.address, 'closed')


ws_publisher.start()
server = SimpleWebSocketServer('', 8000, SubscriptionHandler)

try:
    server.serveforever()
except KeyboardInterrupt:
    print("EOF")
