import click
import structlog

logger = structlog.get_logger(__name__)


def run_config(configurations, *, section):
    for config in configurations:
        logger.info("Fetching configuration... ", section=section, name=config)


@click.group()
def cli():
    pass


@cli.command()
@click.option("--ip", default="127.0.0.1", help="IP address")
@click.option("--config", help="runs configuration by name", type=(str), multiple=True)
@click.option("--tmux", help="runs each instance in a tmux window.", is_flag=True)
@click.argument("port")
def server(ip, port, config, tmux):
    logger.info("Running server... ", ip=ip, port=port)
    click.echo("Running server...")
    if config:
        run_config(config, section="server")

    if tmux:
        click.echo("Running in tmux...")


@cli.command()
@click.option("--ip", default="127.0.0.1", help="IP address")
@click.option("--config", help="runs configuration by name", type=(str), multiple=True)
@click.argument("port")
def client(ip, port, config):
    logger.info("Running client... ", ip=ip, port=port)
    click.echo("Running client...")
    if config:
        run_config(config, section="client")


@cli.command()
@click.option("--ip", default="127.0.0.1", help="IP address")
@click.option("--config", help="runs configuration by name", type=(str), multiple=True)
@click.argument("port")
def repl(ip, port, config):
    logger.info("Running repl... ", ip=ip, port=port)
    click.echo("Running repl...")
    if config:
        run_config(config, section="client")
