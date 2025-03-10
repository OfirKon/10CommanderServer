import logging

from reactor import Reactor
from server import Server
from lobby_manager import LobbyManager

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    LobbyManager()
    server = Server()
    try:
        reactor = Reactor()
        reactor.add(server)
        logger.info("Running")
        reactor.run()
    finally:
        server.close()

if __name__ == "__main__":
    main()
