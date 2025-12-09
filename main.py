# main.py

from core.kalshi_client import KalshiClient
from core.market_parser import normalize_market
from core.ai_engine import generate_ai_probability
from core.opportunity_detector import identify_opportunity
from models.historical_learning import save_prediction

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich import box

console = Console()


def render_market_panel(parsed, ai_prob, decision):
    """Displays a styled panel for a single market."""
    table = Table.grid(expand=True)
    table.add_column(justify="left", style="cyan")
    table.add_column(justify="right", style="white")

    yes_price = parsed.get("yes_bid", 0)
    table.add_row("Kalshi YES Bid", f"{yes_price}¢")
    table.add_row("AI Fair Probability", f"{ai_prob*100:.2f}%")
    table.add_row("Recommendation", f"[bold green]{decision}[/bold green]")

    panel = Panel(
        table,
        title=f"[bold white]{parsed.get('title', 'No Title')}[/bold white]",
        expand=True,
        border_style="bright_blue",
        box=box.ROUNDED,
    )
    console.print(panel)


def analyze_market(raw_market):
    """Normalizes, predicts, scores, logs, and renders a single market."""
    parsed = normalize_market(raw_market)
    if not parsed:
        return

    yes_price = parsed.get("yes_bid")
    if yes_price is None:
        console.print(
            Panel(
                f"[yellow]Skipping market (no price data):[/yellow]\n{parsed.get('title')}",
                box=box.ROUNDED,
                border_style="yellow",
            )
        )
        return

    # Generate AI probability using NLP + model
    ai_prob = generate_ai_probability(parsed["title"], parsed)

    # Determine if AI sees an opportunity
    decision = identify_opportunity(ai_prob, parsed)

    # Save to learning history
    save_prediction({
        "question": parsed["title"],
        "prediction": ai_prob,
        "market_price": yes_price / 100,
        "action": decision,
    })

    render_market_panel(parsed, ai_prob, decision)


def main():
    console.print(Panel("[bold bright_blue]Connecting to Kalshi API…[/bold bright_blue]", box=box.ROUNDED))
    client = KalshiClient()

    # Step 1 — Fetch markets
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Fetching markets…", total=None)
        response = client.list_markets()
        markets = response.get("markets", [])

    console.print(Panel(f"[green]Fetched {len(markets)} markets[/green]", box=box.ROUNDED))

    # Step 2 — Analyze markets
    with Progress(
        TextColumn("[bold blue]Analyzing Markets[/bold blue]"),
        SpinnerColumn(),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        expand=True,
    ) as prog:

        task = prog.add_task("Processing…", total=10)

        for market in markets[:10]:  # Limit for demo
            try:
                analyze_market(market)

            except Exception as e:
                console.print(f"[red]Error analyzing market {market.get('ticker')}:[/red] {e}")

            prog.update(task, advance=1)


if __name__ == "__main__":
    main()
