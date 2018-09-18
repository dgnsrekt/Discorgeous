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
On Linux environments, installing voice requires getting the following dependencies:
```
apt install libffi-dev libnacl-dev
```

### QUICK START
----
#### Install
```
git clone https://github.com/dgnsrekt/Discorgeous.git
cd Discorgeous
pip3 install -e .
```
### Run Single Server
```
discorgeous server --normal --port 5555 --token {discord_bot_token} --channel {discord_channel_id}
```
#### Run Repl Client
```
discorgeous repl --port 5555
```
#### Run Test Song
```
discorgeous tester --port 5555
```
#### Run Muliple Servers
First edit the server_config.toml file in the Discorgeous/config folder.
```
[ServerOne] <- What ever name you want
CHANNEL_ID = "000000000000000000" <- {discord_channel_id}
VOICE_TOKEN = "00000000000000000000000000000000000000000000000000000000000" <- {discord_bot_token}
IP = "0.0.0.0"
PORT = "6666"
```
Run server with configuration section name
```
discorgeous server --config ServerOne --config ServerTwo
```
Run in seperate tmux instances
```
discorgeous server --config ServerOne --config ServerTwo --tmux
```


### TODO
* Client over SSH
* DOCs
* config files in relative path
* Requirements.

### Contact
* Twitter = Telegram = @dgnsrekt
* Email = dgnsrekt@pm.me

### License
This code is licensed under the MIT License.
