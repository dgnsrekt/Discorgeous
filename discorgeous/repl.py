import asyncio
from client import Client
from prompt_toolkit import prompt
from time import sleep
import sys


class Repl(Client):
    def __init__(self, *, ip, port):
        super().__init__(ip=ip, port=port)

    async def repl(self, *, loop):
        print("CTRL-C to exit")
        while True:
            message = prompt(":>")
            if len(message) > 0 and message != " ":
                await self.handler(message, loop)

    def start(self):
        loop = asyncio.get_event_loop()
        repl_coro = self.repl(loop=loop)
        loop.run_until_complete(repl_coro)

        try:
            loop.run_forever()
        except KeyboardInterrupt as e:
            print(e)
        finally:
            loop.close()
