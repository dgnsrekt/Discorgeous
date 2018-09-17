SONG = """This was a triumph!
I'm making a note here Huge success!

It's hard to overstate my satisfaction.

At Fomo Driven Development We do what we must
because we can for the good of all of us.
Except the ones who are dead.

But there's no sense crying over every mistake.
You just keep on trying 'til you run out of cake.
And the science gets done.
And you make a neat gun for the people who are still alive.

I'm not even angry... I'm being so sincere right now.
Even though you broke my heart, and killed me.

And tore me to pieces.
And threw every piece into a fire.
As they burned it hurt because I was so happy for you!

Now, these points of data make a beautiful line.
And we're out of beta.
We're releasing on time!
So I'm GLaD I got burned!
Think of all the things we learned!
for the people who are still alive.

Go ahead and leave me...
I think I'd prefer to stay inside...
Maybe you'll find someone else to help you.
Maybe Black Mesa?
That was a joke. Ha Ha. Fat Chance!

Anyway this cake is great!
It's so delicious and moist!

Look at me: still talking
when there's science to do!
When I look out there,
it makes me glad I'm not you.

I've experiments to run.
There is research to be done.
On the people who are still alive.
And believe me I am still alive.
I'm doing science and I'm still alive.
I feel fantastic and I'm still alive.
While you're dying I'll be still alive.
And when you're dead I will be still alive

Still alive.

Still alive.

website: https://www.fomodd.io
telegram = twitter = @dgnsrekt
""".split(
    "\n"
)


import asyncio
from client import Client
from time import sleep
import sys


class Song(Client):
    def __init__(self, *, ip, port):
        super().__init__(ip=ip, port=port)

    async def play(self, *, loop):
        for message in SONG:
            if len(message) > 0 and message != " ":
                await self.handler(message, loop)

    def start(self):
        loop = asyncio.get_event_loop()
        repl_coro = self.play(loop=loop)
        loop.run_until_complete(repl_coro)

        try:
            loop.run_forever()
        except KeyboardInterrupt as e:
            print(e)
        finally:
            loop.close()
