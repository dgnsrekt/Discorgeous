import asyncio
import discord
import functools
from gtts import gTTS
from gtts.tts import gTTSError
from io import BytesIO
import logging
import string
import structlog
from tempfile import TemporaryFile
from tenacity import retry, wait_exponential, retry_if_exception_type

logging.basicConfig(level=logging.DEBUG)  # TODO: Remove


class Server:
    def __init__(self, *, ip, port, channel_id, bot_token):
        self.ip = ip
        self.port = int(port)
        self.channel_id = channel_id
        self.bot_token = bot_token
        self.logger = structlog.getLogger(__name__)

        self.loop = asyncio.get_event_loop()
        self.message_queue = asyncio.Queue(loop=self.loop)
        self.audio_queue = asyncio.Queue(loop=self.loop, maxsize=128)
        self.client = discord.Client(loop=self.loop)

    def clean_message(self, message):
        message = message.replace("\n", "").replace("\r", "")
        if len(message) > 0:
            if message != " ":
                return message
        else:
            return "Recieved incomplete message."

    @retry(retry=retry_if_exception_type(gTTSError), wait=wait_exponential(multiplier=1, max=60))
    async def fetch_gtts_message(self):
        while True:
            message = await self.message_queue.get()
            byte_stream = BytesIO()
            try:
                self.logger.info("Downloading GTTS audio.", message=message)
                text_to_speech = gTTS(message, "en-au")
                text_to_speech.write_to_fp(byte_stream)
            except AssertionError:
                message = "Recieved incomplete message."
                self.logger.info("Downloading GTTS audio.", message=message)
                text_to_speech = gTTS(message, "en-au")
                text_to_speech.write_to_fp(byte_stream)

            byte_stream.seek(0)

            while self.audio_queue.full():
                await asyncio.sleep(0.01)
            else:
                await self.audio_queue.put(byte_stream)

    async def handler(self, reader, writer):
        data = await reader.read(4096)
        message = self.clean_message(data.decode())
        address = writer.get_extra_info("peername")
        self.logger.info("Recieved", address=address, data=data, data_length=len(data))
        writer.write(b"ACK!")

        await self.message_queue.put(message)
        self.logger.info("Message added to queue", address=address, message=message)
        self.logger.info("Closing Socket", address=address)
        writer.close()

    async def on_ready(self):
        await self.client.wait_until_ready()
        channel = self.client.get_channel(self.channel_id)
        server = channel.server
        voice = await self.client.join_voice_channel(channel)

        while True:

            if self.client.is_voice_connected(server) == True:
                byte_stream = await self.audio_queue.get()
                with TemporaryFile() as file:
                    file.write(byte_stream.read())
                    file.seek(0)

                    player = voice.create_ffmpeg_player(file, pipe=True)
                    player.start()

                    while player.is_playing():
                        await asyncio.sleep(0.01)
                    else:
                        byte_stream.close()
            else:
                self.logger.info("Reconnecting to voice channel.")
                voice = await self.client.join_voice_channel(channel)

    def run(self):
        self.loop.create_task(self.on_ready())

        server_coro = asyncio.start_server(
            functools.partial(self.handler), self.ip, self.port, loop=self.loop
        )

        client_bot_coro = self.client.start(self.bot_token)
        gtts_coro = self.fetch_gtts_message()

        self.loop.run_until_complete(asyncio.gather(client_bot_coro, server_coro, gtts_coro))

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass

        self.loop.close()
