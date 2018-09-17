from cli import cli
import click
from __version__ import LOGO

if __name__ == "__main__":
    click.echo(LOGO)
    cli()
