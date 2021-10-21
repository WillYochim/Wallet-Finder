
import requests

APIKEY_ETHERSCAN = "DVVQU1PHAEJUA9E39V4SKA7F25NTRMGQSZ"
APIKEY_ETHPLORER = "EK-pyu1H-XEfn7of-5JyhC"

def get_token_balance(wallet_address, token_address):

    url = "https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=" + token_address + "&address=" + wallet_address +"&tag=latest&apikey=" + APIKEY_ETHERSCAN

    content = response(url)
    value = content.get("result")

    #Full Decimal Value:
    #value = value[0:len(value) - 18] + "." + value[len(value) - 18: len(value)]
    
    #Value without decimal
    #value = value[0:len(value) - 18]

    return (value)

def get_holder_addresses(token_address, number_of_wallets):

    url = "https://api.ethplorer.io/getTopTokenHolders/"+ token_address +"?apiKey=" + APIKEY_ETHPLORER + "&limit=" + str(number_of_wallets)

    holders_result = response(url)
    holder_wallets = holders_result['holders']
    
    wallet_list = []
    for wallet in holder_wallets:
        wallet_list.append(wallet['address'])
    
    return wallet_list

def get_possible_wallets(token_list, number_to_check):

    verified_wallets = []
    number_to_check = 200
    length = len(token_list)
    main_token_address = token_list[length-length]
    check_list = get_holder_addresses(main_token_address, number_to_check)

    compare_array = []
    if (length == 2):
        second_token = token_list[length-(length+1)]
        compare_array.append(second_token)
    elif (length == 3):
        second_token = token_list[length-(length+1)]
        third_token = token_list[length-(length+2)]
        compare_array.append(second_token)
        compare_array.append(third_token)
    else:
        second_token = token_list[length-(length+1)]
        third_token = token_list[length-(length+2)]
        fourth_token = token_list[length-(length+3)]
        compare_array.append(second_token)
        compare_array.append(third_token)
        compare_array.append(fourth_token)
    
    for holder in check_list:

        if((length - 1) == 1):
            balance = get_token_balance(holder, compare_array[0])
            if (float(balance) > 0):
                verified_wallets.append(holder)
        elif((length - 1) == 2):
            balance = get_token_balance(holder, compare_array[0])
            balance2 = get_token_balance(holder, compare_array[1])
            if (float(balance) > 0 and float(balance2) > 0):
                verified_wallets.append(holder)
        else:
            balance = get_token_balance(holder, compare_array[0])
            balance2 = get_token_balance(holder, compare_array[1])
            balance3 = get_token_balance(holder, compare_array[2])
            if (float(balance) > 0 and float(balance2) > 0 and float(balance3) > 0):
                verified_wallets.append(holder)

    return verified_wallets

def response(url):
    response = requests.get(url)

    return response.json()

def main():

    selection = input("Enter (1) to check a wallets specific coin balance, or enter (2) to scan for a wallet: \n")

    if(int(selection) == 1):
        token_address = input("Enter a token address:")
        wallet_address = input("Enter a wallet address")
        token_amount = get_token_balance(wallet_address, token_address)
        print("Token amount:", token_amount)
    
    else:
        starting_tokens_input = input("Enter the tokens adresses (2-4) that you know this wallet has (enter space after each address): ")
        starting_tokens = starting_tokens_input.split()
        number_to_check = input("Enter the number of wallets you want to check (Ex: 50 or 200): ")
        print("Starting scan on token: " + starting_tokens[0])
        print("Scanning through " + number_to_check + " wallets...")
        print(get_possible_wallets(starting_tokens, number_to_check))

main()


