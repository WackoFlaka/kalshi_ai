# main.py

from core.kalshi_client import KalshiClient
from core.market_parser import parse_kalshi_market
from core.ai_engine import generate_ai_probability
from core.opportunity_detector import identify_opportunity
from models.historical_learning import save_prediction

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich import box

console = Console()


def render_market_panel(parsed, outcome, ai_prob, decision):
    table = Table.grid(expand=True)
    table.add_column(justify="left", style="cyan")
    table.add_column(justify="right", style="white")

    table.add_row("Kalshi YES Price", f"{outcome.yes_price}¢")
    table.add_row("AI Fair Probability", f"{ai_prob*100:.2f}%")
    table.add_row("Recommendation", f"[bold green]{decision}[/bold green]")

    panel = Panel(
        table,
        title=f"[bold white]{parsed.title}[/bold white]",
        expand=True,
        border_style="bright_blue",
        box=box.ROUNDED,
    )
    console.print(panel)


def analyze_market(market_json, contracts_json):
    parsed = parse_kalshi_market(market_json, contracts_json)
    outcome = parsed.outcomes[0]

    if outcome.yes_price is None:
        console.print(
            Panel(
                f"[yellow]Skipping market (no price data):[/yellow]\n{parsed.title}",
                box=box.ROUNDED,
                border_style="yellow"
            )
        )
        return

    ai_prob = generate_ai_probability(parsed.title, parsed)
    decision = identify_opportunity(ai_prob, outcome)

    # Save history entry
    save_prediction({
        "question": parsed.title,
        "prediction": ai_prob,
        "market_price": outcome.yes_price / 100,
        "action": decision
    })

    render_market_panel(parsed, outcome, ai_prob, decision)


def main():
    console.print(Panel("[bold bright_blue]Connecting to Kalshi API…[/bold bright_blue]", box=box.ROUNDED))

    client = KalshiClient()

    # Loading spinner for API fetch
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Fetching markets…", total=None)
        markets = client.list_markets().get("markets", [])

    console.print(Panel(f"[green]Fetched {len(markets)} markets[/green]", box=box.ROUNDED))

    # Progress bar for analyzing markets
    with Progress(
        TextColumn("[bold blue]Analyzing Markets[/bold blue]"),
        SpinnerColumn(),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        expand=True,
    ) as prog:

        task = prog.add_task("Processing…", total=10)

        for m in markets[:10]:
            try:
                market_id = m["id"]
                full_market = client.get_market(market_id)
                contracts = client.get_contracts(market_id)

                analyze_market(full_market, contracts)

            except Exception as e:
                console.print(f"[red]Error analyzing market {m.get('id')}: {e}[/red]")

            prog.update(task, advance=1)


if __name__ == "__main__":
    main()
