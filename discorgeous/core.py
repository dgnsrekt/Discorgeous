import click
from .cli import cli
from .logo import LOGO


def main():
    click.echo(LOGO)
    cli()


if __name__ == "__main__":
    main()
