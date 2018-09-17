import click
import structlog
import sys
from multiprocessing import Process
from time import sleep

from client import Client
from server import Server

from configuration import GeneralConfiguration, ClientConfiguration, ServerConfiguration

from log import configure_logs
from repl import Repl

logger = structlog.get_logger(__name__)
configure_logs(log_level="INFO")

general_configuration = GeneralConfiguration()
client_configuration = ClientConfiguration()
server_configuration = ServerConfiguration()
#
# for k, v in client_config.items():
#     print(k)
#     print(v)
#

#
# def run_config(configurations, *, section):
#     for name, config in configurations.items():
#         logger.info("Fetching configuration... ", section=section, name=config)
#


@click.group()
def cli():
    pass


@cli.command()
@click.option("--ip", default="127.0.0.1", help="IP address")
@click.argument("port")
@click.argument("channel")
@click.argument("token")
def server(ip, port, channel, token):
    logger.info("Running server... ", ip=ip, port=port, channel=channel, token=token[:5])
    click.echo("Running server...")
    server = Server(ip=ip, port=port, channel_id=channel, bot_token=token)
    server.run()


@cli.command()
@click.option("--config", help="runs configuration by name", type=(str), multiple=True)
def server_config(config):
    server_processes = []
    for c in config:
        ip = server_configuration[c]["IP"]
        port = server_configuration[c]["PORT"]
        token = server_configuration[c]["VOICE_TOKEN"]
        channel = server_configuration[c]["CHANNEL_ID"]

        server = Server(ip=ip, port=port, channel_id=channel, bot_token=token)
        server_processes.append(Process(target=server.run))

        logger.info(
            "Creating server process... ", ip=ip, port=port, channel=channel, token=token[:5]
        )
        click.echo("Creating server process...")

    for p in server_processes:
        p.start()
        logger.info(
            "Starting server process... ", ip=ip, port=port, channel=channel, token=token[:5]
        )

    for p in server_processes:
        p.join()
        logger.info(
            "Joining server process... ", ip=ip, port=port, channel=channel, token=token[:5]
        )


@cli.command()
@click.option("--ip", default="127.0.0.1", help="IP address")
@click.option("--port", default="5000", help="Port")
@click.option("--message", help="message to send", default="hello", type=(str))
def client(ip, port, message):
    logger.info("Running client... ", ip=ip, port=port)
    click.echo("Running client...")

    client = Client(ip=ip, port=port)
    ack = client.send(message=message)

    if ack:
        logger.info("Client succesfully send message... ", ip=ip, port=port, ack=ack)
    else:
        logger.info("Client did not send message... ", ip=ip, port=port, ack=ack)


@cli.command()
@click.option("--config", help="runs configuration by name", type=(str), multiple=True)
@click.option("--message", help="message to send", default="hello", type=(str))
def client_config(config, message):
    client_processes = []
    for c in config:
        ip = client_configuration[c]["IP"]
        port = client_configuration[c]["PORT"]

        logger.info("Running client... ", ip=ip, port=port)
        click.echo("Running client...")

        client = Client(ip=ip, port=port)
        client_processes.append(Process(target=client.send, kwargs={"message": message}))

    for p in client_processes:
        p.start()

    for p in client_processes:
        p.join()


@cli.command()
@click.option("--ip", default="127.0.0.1", help="IP address")
@click.option("--port", default="5000", help="Port")
def repl(ip, port):
    logger.info("Running repl... ", ip=ip, port=port)
    click.echo("Running repl...")

    repl = Repl(ip=ip, port=port)
    try:
        repl.start()
    except KeyboardInterrupt as e:
        click.echo(str(e))
    finally:
        sys.exit()
