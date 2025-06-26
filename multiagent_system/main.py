"""Main CLI entry point for the multi-agent system."""

import click
from rich.console import Console
from rich.panel import Panel

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Multi-Agent System CLI using Strands Agents."""
    pass


@cli.command()
def hello():
    """Display a hello world message."""
    console.print(
        Panel.fit(
            "[bold green]Hello from Multi-Agent System![/bold green]\n"
            "[dim]Built with Strands Agents framework[/dim]",
            title="🤖 Multi-Agent System",
            border_style="green"
        )
    )


@cli.command()
def status():
    """Show system status."""
    console.print("📊 [bold blue]System Status[/bold blue]")
    console.print("✅ Project initialized")
    console.print("⏳ Multi-agent functionality: Coming soon...")
    console.print("🔧 Ready for development")


if __name__ == "__main__":
    cli()
