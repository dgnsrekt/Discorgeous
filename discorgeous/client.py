import asyncio
from time import sleep
import structlog


class Client:
    def __init__(self, *, ip, port):
        self.ip = ip
        self.port = int(port)
        self.logger = structlog.get_logger(__name__).bind(ip=self.ip).bind(port=self.port)
        self.ack = False

    async def handler(self, message, loop):
        reader, writer = await asyncio.open_connection(self.ip, self.port, loop=loop)
        self.logger.info("Sending:", message=message)
        writer.write(message.encode())

        data = await reader.read(4096)
        if data.decode() == "ACK!":
            self.ack = True

        self.logger.info("Closing Socket...", ack=self.ack)
        writer.close()

    def send(self, *, message):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.handler(message, loop))
        except ConnectionRefusedError as e:
            self.logger.error(str(e))
        finally:
            loop.close()
        return self.ack
