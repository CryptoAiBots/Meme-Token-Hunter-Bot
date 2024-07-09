from dotenv import load_dotenv
import os
from web3 import Web3
from helpers.helpers import getTokenAndContract, getPairContract, getReserves, calculatePrice, simulate

# -- HANDLE INITIAL SETUP -- // 
from helpers.server import *
load_dotenv()

arb_for = os.getenv("ARB_FOR")
arb_against = os.getenv("ARB_AGAINST")
units = int(os.getenv("UNITS"))
difference = float(os.getenv("PRICE_DIFFERENCE"))
gas_limit = int(os.getenv("GAS_LIMIT"))
gas_price = float(os.getenv("GAS_PRICE"))

u_pair, s_pair, amount = None, None, None
is_executing = False

# ... (Diğer import ve değişken tanımlamaları buraya ekleyin)

def main():
    global u_pair, s_pair, is_executing

    token0_contract, token1_contract, token0, token1 = getTokenAndContract(arb_for, arb_against, provider)
    u_pair = getPairContract(u_factory, token0.address, token1.address, provider)
    s_pair = getPairContract(s_factory, token0.address, token1.address, provider)

    print(f"uPair Address: {u_pair.address}")
    print(f"sPair Address: {s_pair.address}\n")

    u_pair.on('Swap', lambda: handle_swap_event('Uniswap', token0, token1))
    s_pair.on('Swap', lambda: handle_swap_event('Sushiswap', token0, token1))

    print("Waiting for swap event...")

def handle_swap_event(exchange, token0, token1):
    global is_executing

    if not is_executing:
        is_executing = True

        price_difference = check_price(exchange, token0, token1)
        router_path = determine_direction(price_difference)

        if not router_path:
            print("No MemeHunter Currently Available\n")
            print("-----------------------------------------\n")
            is_executing = False
            return

        is_profitable = determine_profitability(router_path, token0_contract, token0, token1)

        if not is_profitable:
            print("No MemeHunter Currently Available\n")
            print("-----------------------------------------\n")
            is_executing = False
            return

        execute_trade(router_path, token0_contract, token1_contract)

        is_executing = False

def check_price(exchange, token0, token1):
    global is_executing

    print(f"Swap Initiated on {exchange}, Checking Price...\n")

    current_block = provider.eth.blockNumber

    u_price = calculate_price(u_pair)
    s_price = calculate_price(s_pair)

    u_f_price = round(u_price, units)
    s_f_price = round(s_price, units)
    price_difference = (((u_f_price - s_f_price) / s_f_price) * 100).toFixed(2)

    print(f"Current Block: {current_block}")
    print("-----------------------------------------")
    print(f"UNISWAP   | {token1.symbol}/{token0.symbol}\t | {u_f_price}")
    print(f"SUSHISWAP | {token1.symbol}/{token0.symbol}\t | {s_f_price}\n")
    print(f"Percentage Difference: {price_difference}%\n")

    return price_difference

# ... (Diğer fonksiyon tanımlamalarını buraya ekleyin)

if __name__ == "__main__":
    main()
