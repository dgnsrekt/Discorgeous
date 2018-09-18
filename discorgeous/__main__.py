import click
from discorgeous.cli import cli
from discorgeous.logo import LOGO


def main():
    click.echo(LOGO)
    cli()


if __name__ == "__main__":
    main()
