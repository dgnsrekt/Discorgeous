import click
import cli
from logo import LOGO


def main():
    click.echo(LOGO)
    cli.cli()


if __name__ == "__main__":
    main()
