import math

def count_calculator(doner_price: float, money: float) -> tuple:

    count: float = money / doner_price
    doner = math.floor(count)

    change = money-(doner*doner_price)

    return (doner, change)
