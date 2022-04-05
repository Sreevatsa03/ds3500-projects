from evo import Evo
import json
from collections import OrderedDict
import pprint as pp

def read_json(filename):
    """ Read in JSON files """

    with open(filename) as orders:
        orders_dict = json.load(orders)
    
    # read data into OrderedDict for easy manipulation
    orders = OrderedDict()
    for key, value in orders_dict.items():
        orders[key] = value

    return orders

def setups(orders):
    """ Fitness criteria: count the number of setups in the orders list """

    num_setups = 0

    # reset order ids to ids in current solution
    order_ids = list(orders.keys())

    # iterate through the orders
    for i in range(len(order_ids)):
        key = order_ids[i]
        if i < len(order_ids) - 1:

            # add 1 to num_setups if current product doesn't match next product
            if orders[key]["product"] != orders[order_ids[i + 1]]["product"]:
                num_setups += 1

    return num_setups

def setups_agent(solutions):
    """ Agent: minimize number of setups in orders list """

    # set orders to current solution and ids to current ids
    orders = solutions[0]
    order_ids = list(orders.keys())

    # keep track of index where next product doesn't match current product
    index = 0

    # iterate through orders
    for i in range(len(order_ids)):
        key = order_ids[i]
        value = orders[str(key)]["product"]
        if i < len(order_ids) - 1:
            next = order_ids[i + 1]

            # stop iterating and set index to current i when current product doesn't match the next product
            if (int(next) != len(order_ids) + 1) and (value != orders[next]["product"]):
                index = i
                break
    
    # initialize next product
    next = order_ids[index + 1]

    # iterate through orders starting at current index and move next order until next product matches
    for i in range(index, len(order_ids)):

        # move to end in dict and list of ids
        orders.move_to_end(next)
        order_ids.append(order_ids.pop(order_ids.index(next)))

        # update next index to move
        next = order_ids[index + 1]

        # check if current order matches next one
        if (int(next) != len(order_ids) + 1) and (value == orders[next]["product"]):
            break

    return orders

def low_priority(orders):
    """ Fitness criteria: quantify amount of low priority orders done before last high priority """

    # initialize score and set order ids
    score = 0
    order_ids = list(orders.keys())

    # get index of last high priority order
    priorities_reversed = [value["priority"] for value in list(orders.values())][::-1]
    last_high_reverse = priorities_reversed.index("HIGH")
    last_high = len(priorities_reversed) - last_high_reverse - 1
    
    # iterate until last high priority order
    for i in range(last_high):
        key = order_ids[i]

        # add product quantity to score if the product is low priority
        if orders[key]["priority"] == "LOW":
            score += orders[key]["quantity"]

    return score

def low_priority_agent(solutions):
    """ Agent: minimize lowpriority score """

    # set orders to current solution and ids to current ids
    orders = solutions[0]
    order_ids = list(orders.keys())

    # iterate through orders
    for i in range(len(order_ids)):
        key = order_ids[i]
        
        # if order is low priority move it to end
        if orders[key]["priority"] == "LOW":
            orders.move_to_end(key)
            break

    return orders

def delays(orders):
    """ Fitness criteria: quantify amount of delay in orders list """

    # initialize delay and set order ids
    delay = 0
    order_ids = list(orders.keys())
    
    # iterate through order ids
    for i in range(len(order_ids) - 1):
        key = order_ids[i]
        next = order_ids[i + 1]

        # if order id of current order is greater than next order add quantity of order to delay
        if int(key) > int(next):
            delay += orders[key]["quantity"]

    return delay

def delays_agent(solutions):
    """ Agent: minimize delay """

    # set orders to current solution and ids to current ids
    orders = solutions[0]
    order_ids = list(orders.keys())

    # iterate through order ids
    for i in range(len(order_ids) - 1):
        key = order_ids[i]
        next = order_ids[i + 1]

        # if current order id is greater than next order's order id, swap them
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
    # read in data
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