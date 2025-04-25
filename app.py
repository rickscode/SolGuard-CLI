# import requests
# import sys
# from typing import List, Dict
# from rich.console import Console
# from rich.table import Table
# import subprocess

# console = Console()

# # RugScore API URL template
# RUGSCORE_URL = "https://api.rugcheck.xyz/v1/tokens/{}/report/summary"

# HEADERS = {
#     "accept": "application/json",
#     "User-Agent": "SolGuard/1.0"
# }

# print("Debug: Starting SolGuard...")

# def fetch_tokens(wallet_address: str) -> List[Dict]:
#     """Fetch SPL tokens from a Solana wallet via Node.js script"""
#     try:
#         print("Fetching tokens from wallet...")
#         result = subprocess.run(['ts-node', 'get_tokens.ts', wallet_address], capture_output=True, text=True)
        
#         if result.returncode != 0:
#             console.print(f"[red]Error fetching tokens from Node.js script:[/red] {result.stderr}")
#             sys.exit(1)
        
#         return eval(result.stdout)  # Convert the output string into a list of tokens (make sure it's a valid format)
#     except Exception as e:
#         console.print(f"[red]Error fetching tokens:[/red] {e}")
#         sys.exit(1)

# def check_token_rugscore(mint: str) -> Dict:
#     """Call RugScore API for a token"""
#     try:
#         print(f"Checking token {mint} on RugScore...")
#         url = RUGSCORE_URL.format(mint)
#         response = requests.get(url, headers=HEADERS)
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         return {
#             "mint": mint,
#             "score": "N/A",
#             "risk": "Unknown",
#             "liquidity_usd": 0,
#             "error": str(e)
#         }

# def print_report(token_data: List[Dict]):
#     """Prints a CLI table of token risks"""
#     table = Table(title="SolGuard Token Risk Report", header_style="bold magenta")
#     table.add_column("Symbol", justify="left")
#     table.add_column("Risk", justify="center")
#     table.add_column("Score", justify="center")
#     table.add_column("Liquidity", justify="right")
#     table.add_column("Status", justify="left")

#     for token in token_data:
#         symbol = token.get("tokenSymbol", "???")
#         mint = token.get("tokenAddress")
#         rug = token.get("rugscore", {})

#         risk = rug.get("risk", "Unknown")
#         score = rug.get("score", "N/A")
#         liquidity = rug.get("liquidity_usd", 0)

#         if isinstance(score, float):
#             score = round(score)

#         if liquidity is not None:
#             liquidity = f"${liquidity:,.0f}"
#         else:
#             liquidity = "$0"

#         if risk == "High" or rug.get("liquidity_usd", 0) == 0:
#             status = "[red]❌ High Risk[/red]"
#         elif risk == "Medium":
#             status = "[yellow]⚠️ Medium Risk[/yellow]"
#         elif risk == "Low":
#             status = "[green]✅ Safe[/green]"
#         else:
#             status = "[grey]❓ Unknown[/grey]"

#         table.add_row(symbol, risk, str(score), liquidity, status)

#     console.print(table)

# def main():
#     print("Debug: Inside main()...")
#     console.print("[bold cyan]🛡️ SolGuard CLI v1[/bold cyan]")
#     wallet = input("🔍 Enter your Solana wallet address: ").strip()

#     console.print(f"\n[blue]📦 Fetching tokens for:[/blue] {wallet}")
#     tokens = fetch_tokens(wallet)

#     if not tokens:
#         console.print("[yellow]No SPL tokens found in this wallet.[/yellow]")
#         return

#     token_report = []

#     for token in tokens:
#         mint = token.get("tokenAddress")
#         rugscore = check_token_rugscore(mint)
#         token["rugscore"] = rugscore
#         token_report.append(token)

#     print_report(token_report)

# if __name__ == "__main__":
#     print("Debug: Starting the script...")
#     main()

import requests
import sys
from typing import List, Dict
from rich.console import Console
from rich.table import Table
import subprocess

console = Console()

# RugScore API URL template
RUGSCORE_URL = "https://api.rugcheck.xyz/v1/tokens/{}/report/summary"

HEADERS = {
    "accept": "application/json",
    "User-Agent": "SolGuard/1.0"
}

print("Debug: Starting SolGuard...")

def fetch_tokens(wallet_address: str) -> List[Dict]:
    """Fetch SPL tokens from a Solana wallet via Node.js script"""
    try:
        print("Fetching tokens from wallet...")
        result = subprocess.run(['ts-node', 'get_tokens.ts', wallet_address], capture_output=True, text=True)
        
        if result.returncode != 0:
            console.print(f"[red]Error fetching tokens from Node.js script:[/red] {result.stderr}")
            sys.exit(1)
        
        return eval(result.stdout)  # Convert the output string into a list of tokens (make sure it's a valid format)
    except Exception as e:
        console.print(f"[red]Error fetching tokens:[/red] {e}")
        sys.exit(1)

def check_token_rugscore(mint: str) -> Dict:
    """Call RugScore API for a token"""
    try:
        print(f"Checking token {mint} on RugScore...")
        url = RUGSCORE_URL.format(mint)
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "mint": mint,
            "score": "N/A",
            "risk": "Unknown",
            "liquidity_usd": 0,
            "error": str(e)
        }

def print_report(token_data: List[Dict]):
    """Prints a CLI table of token risks"""
    table = Table(title="SolGuard Token Risk Report", header_style="bold magenta")
    table.add_column("Symbol", justify="left")
    table.add_column("Risk", justify="center")
    table.add_column("Score", justify="center")
    table.add_column("Liquidity", justify="right")
    table.add_column("Status", justify="left")

    for token in token_data:
        symbol = token.get("tokenSymbol", "???")
        mint = token.get("tokenAddress")
        rug = token.get("rugscore", {})

        risk = rug.get("risk", "Unknown")
        score = rug.get("score", "N/A")
        liquidity = rug.get("liquidity_usd", 0)

        if isinstance(score, float):
            score = round(score)

        if liquidity is not None:
            liquidity = f"${liquidity:,.0f}"
        else:
            liquidity = "$0"

        if risk == "High" or rug.get("liquidity_usd", 0) == 0:
            status = "[red]❌ High Risk[/red]"
        elif risk == "Medium":
            status = "[yellow]⚠️ Medium Risk[/yellow]"
        elif risk == "Low":
            status = "[green]✅ Safe[/green]"
        else:
            status = "[grey]❓ Unknown[/grey]"

        table.add_row(symbol, risk, str(score), liquidity, status)

    console.print(table)

def main():
    print("Debug: Inside main()...")
    console.print("[bold cyan]🛡️ SolGuard CLI v1[/bold cyan]")
    wallet = input("🔍 Enter your Solana wallet address: ").strip()

    console.print(f"\n[blue]📦 Fetching tokens for:[/blue] {wallet}")
    tokens = fetch_tokens(wallet)

    if not tokens:
        console.print("[yellow]No SPL tokens found in this wallet.[/yellow]")
        return

    token_report = []

    for token in tokens:
        mint = token.get("tokenAddress")
        rugscore = check_token_rugscore(mint)
        token["rugscore"] = rugscore
        token_report.append(token)

    print_report(token_report)

if __name__ == "__main__":
    print("Debug: Starting the script...")
    main()
