# solguard.py
import requests
import sys
from typing import List, Dict
from rich.console import Console
from rich.table import Table
import subprocess
import json
from dotenv import load_dotenv

load_dotenv()
console = Console()

RUGSCORE_URL = "https://api.rugcheck.xyz/v1/tokens/{}/report/summary"

HEADERS = {
    "accept": "application/json",
    "User-Agent": "SolGuard/1.0"
}

def fetch_tokens(wallet_address: str) -> List[Dict]:
    try:
        result = subprocess.run(
            ['node', 'get_tokens.js', wallet_address],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            console.print(f"[red]Error fetching tokens from Node.js script:[/red] {result.stderr}")
            sys.exit(1)
        
        return json.loads(result.stdout)
    except Exception as e:
        console.print(f"[red]Error fetching tokens:[/red] {e}")
        sys.exit(1)

def check_token_rugscore(mint: str) -> Dict:
    try:
        url = RUGSCORE_URL.format(mint)
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "mint": mint,
            "score_normalised": "N/A",
            "summary": { "risk": "Unknown" },
            "liquidity_usd": 0,
            "error": str(e)
        }

# def print_report(token_data: List[Dict]):
#     table = Table(title="SolGuard Token Risk Report", header_style="bold magenta")
#     table.add_column("Symbol", justify="left")
#     table.add_column("Risk", justify="center")
#     table.add_column("Score", justify="center")
#     table.add_column("Status", justify="left")

#     for token in token_data:
#         symbol = token.get("tokenSymbol", "???")
#         rug = token.get("rugscore", {})

#         risk = rug.get("risks.name", "Unknown")
#         score = rug.get("score_normalised", "N/A")

#         if isinstance(score, float):
#             score = round(score)

    

#         if risk == "High":
#             status = "[red]❌ High Risk[/red]"
#         elif risk == "Medium":
#             status = "[yellow]⚠️ Medium Risk[/yellow]"
#         elif risk == "Low":
#             status = "[green]✅ Safe[/green]"
#         else:
#             status = "[grey]❓ Unknown[/grey]"

#         table.add_row(symbol, risk, str(score), status)

#     console.print(table)

def print_report(token_data: List[Dict]):
    table = Table(title="SolGuard Token Risk Report", header_style="bold magenta")
    table.add_column("Symbol", justify="left")
    table.add_column("Risk", justify="center")
    table.add_column("Score", justify="center")
    table.add_column("Status", justify="left")

    for token in token_data:
        symbol = token.get("tokenSymbol", "???")
        rug = token.get("rugscore", {})
        risks = rug.get("risks", [])
        score = rug.get("score_normalised", "N/A")

        if isinstance(score, float):
            score = round(score)

        # Handle multiple risks or no risks
        if not risks:
            risk_names = "No risks detected"
            status = "[green]✅ Safe[/green]"
        else:
            risk_names = "\n".join([risk.get("name", "Unknown risk") for risk in risks])
            
            # Use the first risk's level for status (or combine them if needed)
            first_risk_level = risks[0].get("level", "unknown").lower()
            if first_risk_level == "high":
                status = "[red]❌ High Risk[/red]"
            elif first_risk_level == "warn" or first_risk_level == "medium":
                status = "[yellow]⚠️ Warning[/yellow]"
            elif first_risk_level == "low":
                status = "[green]✅ Safe[/green]"
            else:
                status = f"[grey]❓ {first_risk_level.capitalize()}[/grey]"

        table.add_row(symbol, risk_names, str(score), status)

    console.print(table)

def main():
    console.print("[bold cyan]🛡️ SolGuard CLI v1[/bold cyan]")
    wallet = input("🔍 Enter your Solana wallet address: ").strip()

    console.print(f"\n[blue]📦 Fetching tokens for:[/blue] {wallet}")
    tokens = fetch_tokens(wallet)

    if not tokens:
        console.print("[yellow]No SPL tokens found in this wallet.[/yellow]")
        return

    token_report = []

    for idx, token in enumerate(tokens, start=1):
        mint = token.get("mintAddress") or token.get("tokenAddress")
        console.print(f"[grey]🔎 ({idx}/{len(tokens)}) Checking token: {mint}[/grey]")
        rugscore = check_token_rugscore(mint)
        token["rugscore"] = rugscore
        token_report.append(token)


    print_report(token_report)

if __name__ == "__main__":
    main()
