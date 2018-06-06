from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

import threading
import sys

if sys.version_info[0] == 2:
    import thread as _thread
elif sys.version_info[0] == 3:
    import _thread
else:
    # hopefully
    import _thread


class WsPublisher(threading.Thread):
    def __init__(self, remind=True):
        super(WsPublisher, self).__init__()
        self.remind = bool(remind)
        self.last_message = None
        self.clients = {}

    def run(self):
        while True:
            line = sys.stdin.readline()
            if not line:
                break

            line = line.rstrip()
            self.last_message = line
            for client in self.clients:
                self.clients[client].sendMessage(u'{}'.format(line))
        _thread.interrupt_main()

    def add_client(self, client):
        self.clients[id(client)] = client
        if self.remind and self.last_message is not None:
            client.sendMessage(u'{}'.format(self.last_message))

    def rm_client(self, client):
        del self.clients[id(client)]


ws_publisher = WsPublisher()


class SubscriptionHandler(WebSocket):
    def handleMessage(self):
        pass

    def handleConnected(self):
        ws_publisher.add_client(self)
        print(self.address, 'connected')

    def handleClose(self):
        ws_publisher.rm_client(self)
        print(self.address, 'closed')


ws_publisher.start()
server = SimpleWebSocketServer('', 8484, SubscriptionHandler)

try:
    server.serveforever()
except KeyboardInterrupt:
    print("EOF")
