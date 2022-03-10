from evo import Evo
import json
from collections import OrderedDict

def read_json(filename):
    with open(filename) as orders:
        orders_dict = json.load(orders)

    orders = OrderedDict()
    for key, value in orders_dict.items():
        orders[key] = value

    return orders

def setups(orders):
    num_setups = 0
    for key in orders.keys():
        if int(key) < len(orders):
            if orders[key]["product"] != orders[str(int(key) + 1)]["product"]:
                num_setups += 1

    return num_setups

def setups_agent(solutions):
    orders = solutions[0]

    order_ids = list(orders.keys())

    for i in range(len(order_ids)):
        key = order_ids[i]
        value = orders[str(key)]["product"]
        if int(key) < len(order_ids):
            next = str(int(key) + 1)
            while (int(next) != len(order_ids) + 1) and (value != orders[next]["product"]):
                orders.move_to_end(next)
                order_ids.append(order_ids.pop(order_ids.index(next)))
                print(orders[str(key)]["product"], orders[next]["product"])
                next = str(int(next) + 1)

    return orders

def low_priority():
    pass

def delays():
    pass

def main():
    orders = read_json('orders.json')

    # dummy_dict = dict()
    # for key, value in orders.items():
    #     if int(key) < 11:
    #         dummy_dict[key] = value

    # dummy = OrderedDict()
    # for key, value in dummy_dict.items():
    #     dummy[key] = value

    # print(dummy)
    # print(setups(orders))

    # new_orders = setups_agent(orders)


    
    # print(setups(new_orders))
    # print(setups(new_orders))

    # # Create enivronment
    # E = Evo()

    # # Register fitness criteria
    # E.add_fitness_criteria("setups", setups)

    # # Register agents
    # E.add_agent("setups_agent", setups_agent)

    # # Add initial solution
    # L = [rand.randrange(1, 99) for _ in range(100)]
    # E.add_solution(L)
    # print(E)

    # # Run the evolver
    # E.evolve(1000000, 500, 10000)

if __name__ == '__main__':
    main()