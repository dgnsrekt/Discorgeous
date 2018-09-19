from discorgeous import Client
from datetime import datetime
import asyncio
import sys


class MinuteNotificationClient(Client):
    def __init__(self, *, ip, port, sleep_interval=60):
        super().__init__(ip=ip, port=port)
        self.sleep_interval = sleep_interval

    async def timeupdate(self, *, loop):
        while True:
            current_time = datetime.now().time()
            hour = current_time.hour
            minute = current_time.minute
            message = f"The current time is {hour} {minute}."
            await self.handler(message, loop)
            await asyncio.sleep(self.sleep_interval)

    def start(self):
        loop = asyncio.get_event_loop()
        time_coro = self.timeupdate(loop=loop)
        loop.run_until_complete(time_coro)

        try:
            loop.run_forever()
        except KeyboardInterrupt as e:
            print(e)
        finally:
            loop.close()


MNC = MinuteNotificationClient(ip="localhost", port=6666, sleep_interval=60)

try:
    MNC.start()
except KeyboardInterrupt as e:
    print(str(e))
except Exception as e:
    print(str(e))
finally:
    sys.exit()
