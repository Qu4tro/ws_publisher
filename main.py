# import argparse

from server import ws_server
from publisher import ws_publisher


ws_publisher.start()
try:
    ws_server.serveforever()
except KeyboardInterrupt:
    print("EOF")
