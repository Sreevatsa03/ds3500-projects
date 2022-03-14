from evo import Evo
import json
from collections import OrderedDict
import pprint as pp

def read_json(filename):
    with open(filename) as orders:
        orders_dict = json.load(orders)

    orders = OrderedDict()
    for key, value in orders_dict.items():
        orders[key] = value

    return orders

def setups(orders):
    num_setups = 0
    order_ids = list(orders.keys())

    for i in range(len(order_ids)):
        key = order_ids[i]
        if i < len(order_ids) - 1:
            if orders[key]["product"] != orders[order_ids[i + 1]]["product"]:
                num_setups += 1

    return num_setups

def setups_agent(solutions):
    orders = solutions[0]

    order_ids = list(orders.keys())

    index = 0
    for i in range(len(order_ids)):
        key = order_ids[i]
        value = orders[str(key)]["product"]
        if i < len(order_ids) - 1:
            next = order_ids[i + 1]
            if (int(next) != len(order_ids) + 1) and (value != orders[next]["product"]):
                index = i
                break
    
    next = order_ids[index + 1]
    for i in range(index, len(order_ids)):
        # move to end in dict and list of ids
        orders.move_to_end(next)
        order_ids.append(order_ids.pop(order_ids.index(next)))
        # print(orders[str(key)]["product"], orders[next]["product"])

        # update next index to move
        next = order_ids[index + 1]

        # check if current order matches next one
        if (int(next) != len(order_ids) + 1) and (value == orders[next]["product"]):
            break

    return orders

def low_priority(orders):
    score = 0
    order_ids = list(orders.keys())

    priorities_reversed = [value["priority"] for value in list(orders.values())][::-1]
    last_high_reverse = priorities_reversed.index("HIGH")
    last_high = len(priorities_reversed) - last_high_reverse - 1
            
    for i in range(last_high):
        key = order_ids[i]
        if orders[key]["priority"] == "LOW":
            score += orders[key]["quantity"]

    return score

def low_priority_agent(solutions):
    orders = solutions[0]
    order_ids = list(orders.keys())

    for i in range(len(order_ids)):
        key = order_ids[i]
        if orders[key]["priority"] == "LOW":
            orders.move_to_end(key)
            break

    return orders

def delays(orders):
    delay = 0
    order_ids = list(orders.keys())
            
    for i in range(len(order_ids) - 1):
        key = order_ids[i]
        next = order_ids[i + 1]
        if int(key) > int(next):
            delay += orders[key]["quantity"]

    return delay

def delays_agent(solutions):
    orders = solutions[0]
    order_ids = list(orders.keys())

    for i in range(len(order_ids) - 1):
        key = order_ids[i]
        next = order_ids[i + 1]
        if int(key) > int(next):
            # swap orders in dictionary
            orders_list = list(orders.items())
            orders_list[i], orders_list[i + 1] = orders_list[i + 1], orders_list[i]
            orders = OrderedDict(orders_list)

            # swap orders in order ids list
            order_ids[i], order_ids[i + 1] = order_ids[i + 1], order_ids[i]
            break

    return orders

def main():
    orders = read_json('orders.json')

    # Create enivronment
    E = Evo()

    # Register fitness criteria
    E.add_fitness_criteria("setups", setups)
    E.add_fitness_criteria("low_priority", low_priority)
    E.add_fitness_criteria("delays", delays)

    # Register agents
    E.add_agent("setups_agent", setups_agent)
    E.add_agent("low_priority_agent", low_priority_agent)
    E.add_agent("delays_agent", delays_agent)

    # Add initial solution
    E.add_solution(orders)

    # Run the evolver
    E.evolve(10000, 500, 10000)

    # save solutions to csv file
    E.save_solutions()

    # visualize tradeoffs
    E.visualize()

if __name__ == '__main__':
    main()