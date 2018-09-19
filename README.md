# Discorgeous
Discord + GTTS = a discord bot that sends google text to speech voice messages to discord voice channels.


[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
```
    ____   _
   / __ \ (_)_____ _____ ____   _____ ____ _ ___   ____   __  __ _____
  / / / // // ___// ___// __ \ / ___// __ `// _ \ / __ \ / / / // ___/
 / /_/ // /(__  )/ /__ / /_/ // /   / /_/ //  __// /_/ // /_/ /(__  )
/_____//_//____/ \___/ \____//_/    \__, / \___/ \____/ \__,_//____/
                                   /____/

Usage: discorgeous [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  client      Send a single message to server.
  client-ssh  ssh client not implemented.
  repl        Repl messages to server.
  server      Runs the discord bot server.
  tester      Sends test song to server.
```
### REQUIRES

On Linux environments, installing discord.py[voice] requires getting the following dependencies:
```
apt install libffi-dev libnacl-dev
```

### QUICK START

#### Install
```
git clone https://github.com/dgnsrekt/Discorgeous.git
cd Discorgeous
pip3 install -e .
```
#### Run Single Server
```
discorgeous server --single --port 5555 --token {discord_bot_token} --channel {discord_channel_id}
```
#### Run REPL Client
```
discorgeous repl --port 5555
```
#### Run Test Song
```
discorgeous tester --port 5555
```
#### Run Muliple Servers
First edit the server_config.toml file in the Discorgeous/config folder.
Add as many servers as you like.
```
[ServerOne] <- Whatever name you want.
CHANNEL_ID = "000000000000000000" <- {discord_channel_id}
VOICE_TOKEN = "00000000000000000000000000000000000000000000000000000000000" <- {discord_bot_token}
IP = "0.0.0.0"
PORT = "6666" <- Make sure each server has a different port.

[ServerTwo] <- Whatever name you want.
CHANNEL_ID = "111111111111111111" <- {discord_channel_id}
VOICE_TOKEN = "11111111111111111111111111111111111111111111111111111111111" <- {discord_bot_token}
IP = "0.0.0.0"
PORT = "5555" <- Make sure each server has a different port.
```
Run server with configuration section name
```
discorgeous server --config ServerOne --config ServerTwo
```
Run in seperate tmux instances
```
discorgeous server --config ServerOne --config ServerTwo --tmux
```
### Example Client Script
The MinuteNotificationClient sends a current time message to a discorgeous server every minute.
```
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

```

### TODO
* Client over SSH
* Documentation
* Tests
* Config files in user/relative path
* Clean and update Requirements
* Link to discord voice bot token creation guide
* Add port check to server config to make sure all ports are unique.

### Contact
* Twitter = Telegram = @dgnsrekt
* Email = dgnsrekt@pm.me

### License
This code is licensed under the MIT License.
