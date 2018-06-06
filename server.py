from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

from publisher import ws_publisher


class SubscriptionHandler(WebSocket):
    def handleMessage(self):
        pass

    def handleConnected(self):
        ws_publisher.add_client(self)
        print(self.address, 'connected')

    def handleClose(self):
        ws_publisher.rm_client(self)
        print(self.address, 'closed')


ws_server = SimpleWebSocketServer('', 8484, SubscriptionHandler)
