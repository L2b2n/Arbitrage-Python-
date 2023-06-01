from web3 import Web3
from dotenv import dotenv_values
import datetime

# Laden der Umgebungsvariablen aus der .env-Datei
config = dotenv_values(".env")

# Verbindung zur Binance Smart Chain herstellen
w3 = Web3(Web3.HTTPProvider(config['WEB3_PROVIDER_URL']))

# Smart Contract-Adresse und ABI
contract_address = Web3.toChecksumAddress(config['CONTRACT_ADDRESS'])
contract_abi = config['CONTRACT_ABI']

# Konto zum Ausführen der Transaktionen
account = w3.eth.account.privateKeyToAccount(config['PRIVATE_KEY'])

# Kontraktinstanz erstellen
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Arbitrage-Handel ausführen
def execute_arbitrage():
    try:
        # Überprüfen der Preise auf beiden Plattformen
        pancakeswap_price = get_price_from_pancakeswap()
        iswap_price = get_price_from_iswap()
        
        # Überprüfen der Kursabweichung von mindestens 1%
        if (pancakeswap_price > iswap_price) and (pancakeswap_price - iswap_price) >= (pancakeswap_price * 0.01):
            sell_tokens_on_pancakeswap()
            buy_tokens_on_iswap()
        elif (iswap_price > pancakeswap_price) and (iswap_price - pancakeswap_price) >= (iswap_price * 0.01):
            sell_tokens_on_iswap()
            buy_tokens_on_pancakeswap()
        else:
            print("Keine ausreichende Kursabweichung für Arbitrage vorhanden.")
    except Exception as e:
        print(f"Fehler beim Ausführen des Arbitrage-Handels: {str(e)}")

# Preis von PancakeSwap abrufen
def get_price_from_pancakeswap():
    try:
        pancakeswap_router = Web3.toChecksumAddress(config['PANCAKESWAP_ROUTER_ADDRESS'])
        cht_token = Web3.toChecksumAddress(config['CHT_TOKEN_ADDRESS'])

        amount_out = contract.functions.getPriceFromPancakeSwap().call({'from': account.address})
        return amount_out[-1]
    except Exception as e:
        raise Exception(f"Fehler beim Abrufen des Preises von PancakeSwap: {str(e)}")

# Preis von iSwap abrufen
def get_price_from_iswap():
    try:
        iswap_router = Web3.toChecksumAddress(config['ISWAP_ROUTER_ADDRESS'])
        cht_token = Web3.toChecksumAddress(config['CHT_TOKEN_ADDRESS'])

        amount_out = contract.functions.getPriceFromiSwap().call({'from': account.address})
        return amount_out[-1]
    except Exception as e:
        raise Exception(f"Fehler beim Abrufen des Preises von iSwap: {str(e)}")

# CHT-Token auf PancakeSwap verkaufen
def sell_tokens_on_pancakeswap():
    try:
        pancakeswap_router = Web3.toChecksumAddress(config['PANCAKESWAP_ROUTER_ADDRESS'])
        cht_token = Web3.toChecksumAddress(config['CHT_TOKEN_ADDRESS'])

        tx_hash = contract.functions.sellTokensOnPancakeSwap().transact({'from': account.address})
        w3.eth.waitForTransactionReceipt(tx_hash)

        print(f"CHT-Token auf PancakeSwap verkauft. Transaktionshash: {tx_hash.hex()}")
    except Exception as e:
        raise Exception(f"Fehler beim Verkaufen von CHT-Token auf PancakeSwap: {str(e)}")

# CHT-Token auf iSwap verkaufen
def sell_tokens_on_iswap():
    try:
        iswap_router = Web3.toChecksumAddress(config['ISWAP_ROUTER_ADDRESS'])
        cht_token = Web3.toChecksumAddress(config['CHT_TOKEN_ADDRESS'])

        tx_hash = contract.functions.sellTokensOniSwap().transact({'from': account.address})
        w3.eth.waitForTransactionReceipt(tx_hash)

        print(f"CHT-Token auf iSwap verkauft. Transaktionshash: {tx_hash.hex()}")
    except Exception as e:
        raise Exception(f"Fehler beim Verkaufen von CHT-Token auf iSwap: {str(e)}")

# CHT-Token auf PancakeSwap kaufen
def buy_tokens_on_pancakeswap():
    try:
        pancakeswap_router = Web3.toChecksumAddress(config['PANCAKESWAP_ROUTER_ADDRESS'])
        cht_token = Web3.toChecksumAddress(config['CHT_TOKEN_ADDRESS'])

        tx_hash = contract.functions.buyTokensOnPancakeSwap().transact({'from': account.address})
        w3.eth.waitForTransactionReceipt(tx_hash)

        print(f"CHT-Token auf PancakeSwap gekauft. Transaktionshash: {tx_hash.hex()}")
    except Exception as e:
        raise Exception(f"Fehler beim Kaufen von CHT-Token auf PancakeSwap: {str(e)}")

# CHT-Token auf iSwap kaufen
def buy_tokens_on_iswap():
    try:
        iswap_router = Web3.toChecksumAddress(config['ISWAP_ROUTER_ADDRESS'])
        cht_token = Web3.toChecksumAddress(config['CHT_TOKEN_ADDRESS'])

        tx_hash = contract.functions.buyTokensOniSwap().transact({'from': account.address})
        w3.eth.waitForTransactionReceipt(tx_hash)

        print(f"CHT-Token auf iSwap gekauft. Transaktionshash: {tx_hash.hex()}")
    except Exception as e:
        raise Exception(f"Fehler beim Kaufen von CHT-Token auf iSwap: {str(e)}")

# Hauptfunktion
def main():
    try:
        execute_arbitrage()
    except Exception as e:
        print(f"Fehler beim Ausführen des Programms: {str(e)}")

# Programm ausführen
if __name__ == '__main__':
    main()
