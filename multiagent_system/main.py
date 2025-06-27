"""Main CLI entry point for the multi-agent system."""

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
import time

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
    console.print("✅ Word guessing game implemented")
    console.print("✅ Three LLM agents ready")
    console.print("🔧 Ready for multi-agent gaming!")


@cli.command()
@click.option('--provider', default='openai', help='LLM provider (openai, bedrock, anthropic, ollama)')
@click.option('--model', default='gpt-4', help='Model ID to use')
@click.option('--auto', is_flag=True, help='Play full game automatically')
def play(provider, model, auto):
    """Start the word guessing game with three LLM agents."""
    try:
        from .game_controller import WordGuessingGame
        
        console.print(Panel.fit(
            "[bold cyan]🎮 Word Guessing Game[/bold cyan]\n"
            "[dim]Three LLM agents playing together![/dim]",
            title="🤖 Multi-Agent Game",
            border_style="cyan"
        ))
        
        console.print(f"[yellow]Using {provider} with model: {model}[/yellow]")
        
        # Initialize game with loading spinner
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Initializing LLM agents...", total=None)
            
            try:
                game = WordGuessingGame(
                    model_provider=provider,
                    model_config={"model_id": model}
                )
                progress.update(task, description="✅ Agents initialized!")
                time.sleep(1)
            except Exception as e:
                console.print(f"[red]❌ Error initializing game: {e}[/red]")
                console.print(f"[yellow]💡 Make sure you have set your API key in environment variables[/yellow]")
                if provider == "openai":
                    console.print(f"[dim]   Set OPENAI_API_KEY environment variable[/dim]")
                elif provider == "anthropic":
                    console.print(f"[dim]   Set ANTHROPIC_API_KEY environment variable[/dim]")
                elif provider == "bedrock":
                    console.print(f"[dim]   Configure AWS credentials[/dim]")
                return
        
        if auto:
            # Play full game automatically
            console.print("\n[yellow]🤖 Playing full game automatically...[/yellow]")
            result = game.play_full_game()
            
            # Display results
            table = Table(title="🎯 Game Results")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Turns Played", str(result['turns_played']))
            table.add_row("Game Completed", "✅ Yes" if result['game_completed'] else "❌ No")
            table.add_row("Final Status", result['final_status'][:100] + "..." if len(result['final_status']) > 100 else result['final_status'])
            
            console.print(table)
        
        else:
            # Interactive mode
            console.print("\n[yellow]🎮 Interactive Game Mode[/yellow]")
            console.print("Commands: [cyan]start[/cyan], [cyan]turn[/cyan], [cyan]status[/cyan], [cyan]auto[/cyan], [cyan]quit[/cyan]")
            
            while True:
                command = console.input("\n[bold]Enter command: [/bold]").strip().lower()
                
                if command == "start":
                    result = game.start_new_game()
                    console.print(f"[green]{result}[/green]")
                
                elif command == "turn":
                    if not game.game_active:
                        console.print("[red]No active game. Use 'start' first.[/red]")
                    else:
                        turn_result = game.play_turn()
                        console.print("[blue]Turn completed![/blue]")
                
                elif command == "status":
                    status = game.get_game_status()
                    console.print(Panel(status, title="📊 Game Status"))
                
                elif command == "auto":
                    if not game.game_active:
                        console.print("[red]No active game. Use 'start' first.[/red]")
                    else:
                        console.print("[yellow]Playing remaining turns automatically...[/yellow]")
                        result = game.play_full_game()
                        console.print(f"[green]Game completed in {result['turns_played']} turns![/green]")
                
                elif command == "quit":
                    console.print("[yellow]Thanks for playing![/yellow]")
                    break
                
                else:
                    console.print("[red]Unknown command. Try: start, turn, status, auto, quit[/red]")
    
    except ImportError as e:
        console.print(f"[red]❌ Import error: {e}[/red]")
        console.print("[yellow]Make sure all dependencies are installed with 'uv sync'[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Unexpected error: {e}[/red]")


@cli.command()
def agents():
    """Show information about the available agents."""
    table = Table(title="🤖 Available Agents")
    table.add_column("Agent", style="cyan", no_wrap=True)
    table.add_column("Port", style="magenta")
    table.add_column("Role", style="green")
    table.add_column("Description")
    
    table.add_row(
        "MainAgent",
        "9000",
        "Orchestrator",
        "Coordinates the game flow and manages communication between agents"
    )
    table.add_row(
        "ThinkingAgent", 
        "9001",
        "Word Selector",
        "Selects secret words and answers yes/no questions about them"
    )
    table.add_row(
        "GuessingAgent",
        "9002", 
        "Questioner",
        "Asks strategic questions and makes guesses to find the secret word"
    )
    
    console.print(table)


@cli.command()
def providers():
    """Show supported LLM providers and setup instructions."""
    table = Table(title="🔧 Supported LLM Providers")
    table.add_column("Provider", style="cyan", no_wrap=True)
    table.add_column("Environment Variable", style="yellow")
    table.add_column("Example Model", style="green")
    table.add_column("Setup Instructions")
    
    table.add_row(
        "OpenAI",
        "OPENAI_API_KEY",
        "gpt-4, gpt-3.5-turbo",
        "Get API key from https://platform.openai.com/api-keys"
    )
    table.add_row(
        "Anthropic",
        "ANTHROPIC_API_KEY", 
        "claude-3-sonnet-20240229",
        "Get API key from https://console.anthropic.com/"
    )
    table.add_row(
        "AWS Bedrock",
        "AWS credentials",
        "anthropic.claude-3-sonnet-*",
        "Configure AWS CLI or set AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY"
    )
    table.add_row(
        "Ollama",
        "None (local)",
        "llama3, mistral",
        "Install Ollama locally and run 'ollama serve'"
    )
    
    console.print(table)
    
    console.print("\n[bold]Quick Setup Examples:[/bold]")
    console.print("[cyan]# For OpenAI[/cyan]")
    console.print("export OPENAI_API_KEY='your-api-key-here'")
    console.print("uv run multiagent play --provider openai --model gpt-4")
    
    console.print("\n[cyan]# For Anthropic[/cyan]")
    console.print("export ANTHROPIC_API_KEY='your-api-key-here'")
    console.print("uv run multiagent play --provider anthropic --model claude-3-sonnet-20240229")


if __name__ == "__main__":
    cli()
