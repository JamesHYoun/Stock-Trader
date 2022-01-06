import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


MYBANK = "My_Bank"


# Generates a forecast of stock prices for a set duration.
def get_chart(duration):
    prices = []
    min_price = float('inf')
    for t in range(duration):
        price = t + np.random.normal(0, 1)
        min_price = min(min_price, price)
        prices.append(price)
    return [float("{:.2f}".format(price - min_price + 1)) for price in prices]


# Generates price forecasts for all companies in consideration.
def create_market(names, duration):
    market = {}
    for name in names:
        market[name] = get_chart(duration)
    return market


# Determines the optimal trading strategy for maximum profit.
def get_trades(market, duration, init_worth):
    market[MYBANK] = [init_worth] * duration
    worth = init_worth
    prev_name, best_name = MYBANK, ""
    trades = []
    profits = []
    for t in range(0, duration - 1):
        if t > 0:
            gain = market[best_name][t] / market[best_name][t - 1]
            new_worth = worth * gain
            profits.append(new_worth - worth)
            worth = new_worth
        max_rate = 1
        for name, prices in market.items():
            rate = prices[t + 1] / prices[t]
            if rate > max_rate:
                max_rate = rate
                best_name = name
        if max_rate == 1:
            best_name = MYBANK
        trades.append([prev_name, best_name, worth])
        prev_name = best_name
    del market[MYBANK]
    return trades, worth, profits


# Display Helper Functions

def create_graph(x_nums, y_nums):
    plt.xticks(np.arange(min(x_nums), max(x_nums) + 1, 1))
    plt.yticks(np.arange(min(y_nums), max(y_nums) + 1, 1))
    plt.legend()
    plt.xlabel('time (day)')
    plt.ylabel('price ($)')
    plt.title("Stock Prices Forecast")
    plt.show()


def print_info(trades, worth, profits):
    print("TRADES:")
    for t in range(len(trades)):
        print(f"{t}: ", end='')
        funds = '{:.2f}'.format(trades[t][2])
        print(f"{trades[t][0]} -> {trades[t][1]}, ${funds}")
    print("PROFITS:")
    for t in range(len(profits)):
        print(f"{t+1}: ", end='')
        print('{:.2f}'.format(profits[t]))
    print("WORTH: $", end='')
    print('{:.2f}'.format(worth))


# Helper Functions

def get_all_prices(market):
    min_p = min([min(prices) for _, prices in market.items()])
    max_p = max([max(prices) for _, prices in market.items()])
    return range(int(min_p), int(max_p + 1) + 1, 1)


# Caller Code

names = ['A', 'B', 'C']
duration = 10
market = create_market(names, duration)
init_worth = 10
trades, worth, profits = get_trades(market, duration, init_worth)
print_info(trades, worth, profits)
times = [t for t in range(duration)]
all_prices = get_all_prices(market)
for name, prices in market.items():
    plt.plot(times, prices, label=f'Co. {name}')
create_graph(times, all_prices)
