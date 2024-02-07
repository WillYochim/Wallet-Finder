import requests

class TokenScanner:
    def __init__(self, etherscan_api_key, ethplorer_api_key):
        self.APIKEY_ETHERSCAN = etherscan_api_key
        self.APIKEY_ETHPLORER = ethplorer_api_key

    def response(self, url):
        response = requests.get(url)
        return response.json()

    def get_token_balance(self, wallet_address, token_address):
        url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={token_address}&address={wallet_address}&tag=latest&apikey={self.APIKEY_ETHERSCAN}"
        content = self.response(url)
        value = content.get("result")
        #Full Decimal Value:
        #value = value[0:len(value) - 18] + "." + value[len(value) - 18: len(value)]
        
        #Value without decimal
        value = value[0:len(value) - 18]
        if(value == ''):
            value = 0
        return value

    def get_holder_addresses(self, token_address, number_of_wallets):
        url = f"https://api.ethplorer.io/getTopTokenHolders/{token_address}?apiKey={self.APIKEY_ETHPLORER}&limit={number_of_wallets}"
        holders_result = self.response(url)
        holder_wallets = holders_result['holders']
        return [wallet['address'] for wallet in holder_wallets]

    def get_possible_wallets(self, token_list, number_to_check):
        verified_wallets = []
        main_token_address = token_list[0]
        compare_array = token_list[1:]

        check_list = self.get_holder_addresses(main_token_address, number_to_check)

        for holder in check_list:
            balances = [float(self.get_token_balance(holder, token)) for token in compare_array]
            
            if all(balance > 0 for balance in balances):
                verified_wallets.append(holder)

        return verified_wallets

def main():
    etherscan_api_key = ""
    ethplorer_api_key = ""

    scanner = TokenScanner(etherscan_api_key, ethplorer_api_key)

    selection = input("Enter (1) to check a wallet's specific coin balance, or enter (2) to scan for a wallet: \n")

    if selection == '1':
        token_address = input("Enter a token address:")
        wallet_address = input("Enter a wallet address:")
        token_amount = scanner.get_token_balance(wallet_address, token_address)
        print("Token amount:", token_amount)
    
    elif selection == '2':
        starting_tokens_input = input("Enter the tokens addresses (2-4) that you know this wallet has (enter space after each address): ")
        starting_tokens = starting_tokens_input.split()
        number_to_check = input("Enter the number of wallets you want to check (e.g., 50 or 200): ")
        print("Starting scan on token:", starting_tokens[0])
        print(f"Scanning through {number_to_check} wallets...")
        print(scanner.get_possible_wallets(starting_tokens, int(number_to_check)))

if __name__ == "__main__":
    main()
