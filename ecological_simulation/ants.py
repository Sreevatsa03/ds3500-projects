#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 22:23:58 2020
@author: rachlin
@file  : ants.py
"""
import random as rnd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import sys


# Colors
WHITE = 0
RED = 1
BLUE = 2
GREEN = 3
YELLOW = 4
BLACK = 5


# Directions
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

# Turns
STRAIGHT = 0
RIGHT = 1
REVERSE = 2
LEFT = 3

SIZE = 300


class Ant:

    def __init__(self, x=0, y=0, direction=NORTH):
        """ Construct a new ant at position (x,y)
        and heading in the specified direction (NORTH, SOUTH, EAST, or WEST) """
        self.x = rnd.randrange(0, SIZE)
        self.y = rnd.randrange(0, SIZE)
        self.direction = rnd.randrange(4) # One of 4 directions

    def get_position(self):
        """ Get the x and y position of the ant """
        return self.x, self.y

    def turn(self, turn):
        """ Turn LEFT, RIGHT, or REVERSE direction
        Update direction (NORTH, SOUTH, EAST, WEST) accordingly """
        self.direction = (self.direction + turn) % 4

    def move(self, steps):
        """ Move in current direction some number of steps.
        Wrap around if the ant goes out of bounds """
        if self.direction == NORTH:
            self.x = (self.x - steps) % SIZE
        elif self.direction == SOUTH:
            self.x = (self.x + steps) % SIZE
        elif self.direction == EAST:
            self.y = (self.y + steps) % SIZE
        elif self.direction == WEST:
            self.y = (self.y - steps) % SIZE


class World:

    def __init__(self):
        """ Create a world. """
        self.world = np.zeros((SIZE, SIZE), dtype=int)  # World grid
        self.rules = {}  # Rule storage: curr_color -> (next_col, turn, steps)
        self.ants = []   # List of ant objects.

        self.fig = plt.figure(figsize=(6,6))
        cmap = colors.ListedColormap(['white', 'red', 'blue', 'green', 'yellow', 'black'])
        self.im = plt.imshow(self.world, cmap=cmap, interpolation=None, vmin=0, vmax=5)
        self.ruleset = ''

    def add_rule(self, current_color, next_color, turn, steps):
        """ Register a rule with the world.
        If an an ant is at a position with <current_color>,
        then it changes the color to <next_color> at that location,
        then does a specified <turn>, and takes <steps> forward """
        self.rules[current_color] = (next_color, turn, steps)

    def add_rules(self, rules):
        self.ruleset = rules
        turn_map = {"L":LEFT, "R":RIGHT, "V":REVERSE, "S":STRAIGHT}
        num_rules = len(rules) // 2

        # L1R1V2
        for i in range(num_rules):
            current_color = i
            if i < num_rules - 1:
                next_color = i + 1
            else:
                next_color = 0
            turn = turn_map[rules[2*i]]
            step = int(rules[2*i+1])
            self.add_rule(current_color, next_color, turn, step)


    def add_ant(self, ant):
        """ Add an ant to the world """
        self.ants.append(ant)

    def move(self):
        """ An ant moves according to some rule, updating the
        state of the world in the process. """

        for ant in self.ants:
            # Get the current position of the ant
            x, y = ant.get_position()

            # Get the color at that point in the world
            current_color = self.world[x,y]

            # Identify the next color, ant's turn, and number
            # of steps based on the color at the ant's current position
            next_color, turn, steps = self.rules[current_color]

            # Update the color at the current position
            self.world[x,y] = next_color

            # Turn and move the ant
            ant.turn(turn)
            ant.move(steps)

    def animate(self, i, speed=1):
        for n in range(speed):
            self.move()
        self.im.set_array(self.world)
        plt.title("Rules: "+self.ruleset+"\ngeneration = " + str(i*speed))
        return self.im,


    def run(self, frames, speed=100):

        anim = animation.FuncAnimation(self.fig, self.animate, fargs=(speed,), frames=frames, interval=1, blit=False)
        plt.show()




def main():

    if len(sys.argv) != 4:
        print("USAGE: $ python ants.py <rules> <speed> <initial_ants>")
        sys.exit()


    # Create worlds
    world = World()

    # Add some rules
    # Interesting rules: L1R1, L1R1S1, L1S2R1V2 L1S2L1S2R1
    world.add_rules(sys.argv[1])

    # Simulation speed
    speed = int(sys.argv[2])

    # Starting ants
    num_ants = int(sys.argv[3])
    for _ in range(num_ants):
        world.add_ant(Ant())

    # Run the world
    world.run(100000, speed=speed)


if __name__ == '__main__':
    main()
