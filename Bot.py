from web3 import Web3
from dotenv import load_dotenv
import os
import time

# .env-Datei laden
load_dotenv()

# Web3-Provider-URL und Verbindung erstellen
provider_url = os.getenv('WEB3_PROVIDER_URL')
w3 = Web3(Web3.HTTPProvider(provider_url))

# Kontoadresse und privaten Schlüssel aus der Umgebungsvariablen laden
private_key = os.getenv('PRIVATE_KEY')
account = w3.eth.account.from_key(private_key)
my_address = account.address

# PancakeSwap Router-Adresse und iSwap-Adresse aus der Umgebungsvariable laden
pancakeswap_router_address = Web3.toChecksumAddress(os.getenv('PANCAKESWAP_ROUTER_ADDRESS'))
iswap_address = Web3.toChecksumAddress(os.getenv('ISWAP_ADDRESS'))

# PancakeSwap Router-Abi laden
pancakeswap_router_abi = [
    # ABI-Definitionen hier einfügen
]

# iSwap-Abi laden
iswap_abi = [
    # ABI-Definitionen hier einfügen
]

# PancakeSwap Router-Vertragsinstanz erstellen
pancakeswap_router = w3.eth.contract(address=pancakeswap_router_address, abi=pancakeswap_router_abi)

# iSwap-Vertragsinstanz erstellen
iswap_contract = w3.eth.contract(address=iswap_address, abi=iswap_abi)

# Arbitrage-Funktion
def execute_arbitrage():
    # Arbitrage-Handelsalgorithmus
    # CHT-Token-Balance abrufen
    cht_token_balance = get_token_balance(cht_token_address)

    # Preis auf PancakeSwap abrufen
    pancakeswap_price = get_token_price(pancakeswap_router, cht_token_address)

    # Preis auf iSwap abrufen
    iswap_price = get_token_price(iswap_contract, cht_token_address)

    # Kursabweichung berechnen
    price_difference = pancakeswap_price - iswap_price
    price_difference_percentage = (price_difference / iswap_price) * 100

    if price_difference_percentage > 1:
        # Berechnung des optimalen Tauschbetrags und Mindestausgabebetrags auf PancakeSwap
        amount_in = cht_token_balance // 2
        amount_out_min = amount_in * 0.99  # 1% Abweichung

        # Pfad für den Handel festlegen (CHT-Token zu BNB)
        path = [cht_token_address, wbnb_address]

        # Transaktionsdetails festlegen
        deadline = int(time.time()) + 300  # 5 Minuten
        to = my_address

        try:
            # CHT-Token auf PancakeSwap kaufen
            tx_hash = pancakeswap_router.functions.swapExactTokensForTokens(
                amount_in, amount_out_min, path, to, deadline
            ).buildTransaction({'from': my_address, 'gas': 200000, 'gasPrice': w3.toWei('5', 'gwei')})
            signed_tx = w3.eth.account.sign_transaction(tx_hash, private_key=private_key)
            tx_receipt = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

            # Transaktionsbestätigung abwarten
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_receipt)

            if tx_receipt.status:
                # Erfolgreich ausgeführte Transaktion anzeigen
                print(f"Transaktion erfolgreich! Kauf von CHT-Token auf PancakeSwap: {amount_in} CHT")
            else:
                # Transaktion fehlgeschlagen
                print("Transaktion fehlgeschlagen.")

        except Exception as e:
            # Fehler beim Ausführen der Transaktion
            print(f"Fehler beim Ausführen der Transaktion: {str(e)}")

    else:
        # Keine Arbitrage-Möglichkeit vorhanden
        print("Keine Arbitrage-Möglichkeit vorhanden.")

# Funktion zum Abrufen des Token-Guthabens
def get_token_balance(token_address):
    token_contract = w3.eth.contract(address=token_address, abi=token_abi)
    token_balance = token_contract.functions.balanceOf(my_address).call()
    return token_balance

# Funktion zum Abrufen des Token-Preises
def get_token_price(exchange_contract, token_address):
    token_price = exchange_contract.functions.getTokenPrice(token_address).call()
    return token_price

# Hauptfunktion
def main():
    while True:
        try:
            execute_arbitrage()
        except Exception as e:
            print(f"Fehler beim Ausführen des Programms: {str(e)}")
        
        # Pause von 10 Sekunden vor der nächsten Überprüfung
        time.sleep(10)

# Programm ausführen
if __name__ == '__main__':
    main()
