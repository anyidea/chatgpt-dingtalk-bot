"""Console script for chatbot."""

import click


@click.command()
def main():
    """Main entrypoint."""
    click.echo("chatgpt-dingtalk-bot")
    click.echo("=" * len("chatgpt-dingtalk-bot"))
    click.echo("A dingtalk chatbot powered by chatGPT.")


if __name__ == "__main__":
    main()  # pragma: no cover
