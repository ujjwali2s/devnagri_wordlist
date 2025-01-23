import os
import json
from bson import ObjectId
import asyncio
import time
from web3 import Web3
from eth_account import Account
from mnemonic import Mnemonic
from rich.console import Console
from rich.progress import Progress
from pymongo import MongoClient
import requests
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins

# Console for rich output
console = Console()

# API Keys and Configuration
ETHSCAN_API_KEY = "EPIRY3UVKX9H5G7VNITFDUBWCJUMU9QUEJ"
BSCSCAN_API_KEY = "WHX4VAY9NTK33I5NZHNCGMYBK568CEVMSK"
MONGO_URI = "mongodb+srv://anirudhgoud74:c6oCzwzdHpUKf975@anirudhdatabase.gmm75.mongodb.net/"
RESULTS_DIR = "evm/"
RESULTS_FILE = os.path.join(RESULTS_DIR, "results.json")
FOUND_FILE = os.path.join(RESULTS_DIR, "found.json")

# Ensure the results directory exists
os.makedirs(RESULTS_DIR, exist_ok=True)

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client["evm_scanner"]
    wallets_collection = db["wallets"]
    found_wallets_collection = db["found_wallets"]
    console.print("[bold green]Connected to MongoDB[/bold green]")
except Exception as e:
    console.print(f"[bold red]Failed to connect to MongoDB: {e}[/bold red]")
    exit(1)

# Show instructions
def show_instructions():
    console.print("[bold green]---EVM Wallet Scanner:---[/bold green]", style="bold")
    console.print("[bold red]Software Developed by Deadly[/bold red]\n")
    console.print("This software generates random seed phrases and scans associated wallet addresses for balances on Ethereum, Polygon, BSC, and Bitcoin.\n")
    console.print(f"Results are stored in [bold cyan]{RESULTS_FILE}[/bold cyan].")
    console.print(f"Wallets with non-zero balances are stored in [bold cyan]{FOUND_FILE}[/bold cyan].\n")
    console.print("[bold red]The program runs continuously.[/bold red] Press [bold yellow]Ctrl+C[/bold yellow] to stop it.")

# Generate random seed phrases
def generate_seed_phrases(count):
    mnemon = Mnemonic("english")
    return [mnemon.generate(strength=128) for _ in range(count)]

# Generate wallets from seed phrases
def generate_wallets(seed_phrases):
    Account.enable_unaudited_hdwallet_features()
    wallets = []
    for phrase in seed_phrases:
        account = Account.from_mnemonic(phrase)
        wallets.append((account.address, phrase))
    return wallets

# Generate a Bitcoin address from a seed phrase
def generate_btc_address(seed_phrase):
    seed_bytes = Bip39SeedGenerator(seed_phrase).Generate()
    bip44_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
    btc_address = bip44_ctx.PublicKey().ToAddress()
    return btc_address

# Fetch BTC balance using the provided API
async def fetch_balance_btc(address):
    url = f"https://api.blockchain.info/haskoin-store/btc/address/{address}/balance"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("confirmed", 0) / 1e8  # Convert Satoshis to BTC
    return 0

# Fetch BSC balance
async def fetch_balance_bsc(address):
    url = "https://api.bscscan.com/api"
    params = {"module": "account", "action": "balance", "address": address, "apikey": BSCSCAN_API_KEY}
    response = requests.get(url, params=params)
    balance = response.json().get('result')
    return int(balance) / 1e18 if balance else 0

# Fetch Ethereum balance
async def fetch_balance_eth(address):
    url = "https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "balance",
        "address": address,
        "tag": "latest",
        "apikey": ETHSCAN_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        balance = response.json().get("result")
        if balance:
            return int(balance) / 1e18  # Convert Wei to Ether
    return 0

# Custom JSON encoder for MongoDB ObjectId
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to string
        return super().default(obj)

# Scan wallets for balances
async def scan_wallets(wallets):
    results = []
    found = []

    with Progress() as progress:
        task = progress.add_task("[green]Scanning wallets...", total=len(wallets))

        for address, phrase in wallets:
            eth_balance = await fetch_balance_eth(address)
            bsc_balance = await fetch_balance_bsc(address)
            btc_address = generate_btc_address(phrase)  # Generate BTC address
            btc_balance = await fetch_balance_btc(btc_address)  # Fetch BTC balance

            wallet_data = {
                "address": address,
                "phrase": phrase,
                "btc_address": btc_address,
                "balances": {
                    "ethereum": eth_balance,
                    "bsc": bsc_balance,
                    "bitcoin": btc_balance,
                },
            }

            results.append(wallet_data)

            # Check if any balance is greater than 0
            if any(balance > 0 for balance in wallet_data["balances"].values()):
                found.append(wallet_data)

            progress.advance(task)

    return results, found

# Save results
def save_results(results, file_path, mongodb_collection=None, found_wallets_collection=None, found_wallets=None):
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        with open(file_path, 'w') as file:
            json.dump([], file)

    with open(file_path, 'r+') as file:
        try:
            existing_data = json.load(file)
        except json.JSONDecodeError:
            existing_data = []

        existing_data.extend(results)
        file.seek(0)
        json.dump(existing_data, file, indent=4, cls=CustomJSONEncoder)

    console.print(f"[bold green]Results saved to {file_path}[/bold green]")

    if mongodb_collection is not None:
        save_to_mongodb(results, mongodb_collection)

    if found_wallets_collection is not None and found_wallets is not None:
        save_to_mongodb(found_wallets, found_wallets_collection)

# Save results to MongoDB
def save_to_mongodb(results, mongodb_collection):
    try:
        mongodb_collection.insert_many(results)
        console.print("[bold green]Results saved to MongoDB[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error saving to MongoDB: {e}[/bold red]")

# Main function
def main():
    show_instructions()
    try:
        while True:
            console.print("\n[bold]Generating seed phrases...[/bold]")
            seed_phrases = generate_seed_phrases(2)

            console.print("Generating wallets...")
            wallets = generate_wallets(seed_phrases)

            console.print("Scanning wallets for balances...")
            results, found = asyncio.run(scan_wallets(wallets))

            console.print("Scan complete.")
            console.print(json.dumps(results, indent=4))

            save_results(results, RESULTS_FILE, mongodb_collection=wallets_collection, found_wallets_collection=found_wallets_collection, found_wallets=found)

            console.print("[bold yellow]Waiting for 2 seconds before the next iteration...[/bold yellow]\n")
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("[bold red]Program interrupted. Exiting...[/bold red]")

if __name__ == "__main__":
    main()
