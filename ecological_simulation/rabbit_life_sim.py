
import random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import numpy as np
import copy
import seaborn as sns


SIZE = 300  # The dimensions of the field
# Probability that grass grows back at any location in the next season.
GRASS_RATE = 0.028
WRAP = True  # Does the field wrap around on itself when rabbits move?


class Rabbit:
    """ A furry creature roaming a field in search of grass to eat.
    Mr. Rabbit must eat enough to reproduce, otherwise he will starve. """

    def __init__(self, max_offspring=1, max_hop_distance=1, color='blue'):
        self.x = rnd.randrange(0, SIZE)
        self.y = rnd.randrange(0, SIZE)
        self.eaten = 0
        self.offspring = max_offspring
        self.hop_dist = max_hop_distance
        self.color = color

    def reproduce(self):
        """ Make a new rabbit at the same location.
         Reproduction is hard work! Each reproducing
         rabbit's eaten level is reset to zero. """

        self.eaten = 0
        return copy.deepcopy(self)

    def eat(self, amount):
        """ Feed the rabbit some grass """

        self.eaten += amount

    def move(self):
        """ Move up, down, left, right randomly """

        mv_lst = list(range(-self.hop_dist, self.hop_dist + 1))

        if WRAP:
            self.x = (self.x + rnd.choice(mv_lst)) % SIZE
            self.y = (self.y + rnd.choice(mv_lst)) % SIZE
        else:
            self.x = min(SIZE-1, max(0, (self.x + rnd.choice(mv_lst))))
            self.y = min(SIZE-1, max(0, (self.y + rnd.choice(mv_lst))))


class Pygmy(Rabbit):

    def __init__(self):
        super().__init__(max_offspring=2)


class CottonTail(Rabbit):

    def __init__(self):
        super().__init__(max_hop_distance=2, color='red')


class Field:
    """ A field is a patch of grass with 0 or more rabbits hopping around
    in search of grass """

    def __init__(self, num_pygmy=1, num_cotton_tail=1):
        """ Create a patch of grass with dimensions SIZE x SIZE
        and initially no rabbits """

        # initialize field
        self.field = np.ones(shape=(SIZE, SIZE), dtype=int)

        # initialize rabbits
        self.rabbits = [Pygmy() for _ in range(num_pygmy)]
        self.rabbits.extend([CottonTail() for _ in range(num_cotton_tail)])

        # keep track of number of rabbits per species and amount of grass
        self.npygmy = [num_pygmy]
        self.ncotton = [num_cotton_tail]
        self.ngrass = [SIZE * SIZE]

        # create colormap
        cmap = colors.ListedColormap(["red", "blue", "white", "green"])
        
        # plot of field to use for animation
        self.fig = plt.figure(figsize=(5, 5))
        self.im = plt.imshow(self.field, cmap=cmap, aspect='auto', vmin=0, vmax=1)

    def add_rabbit(self, rabbit):
        """ A new rabbit is added to the field """
        self.rabbits.append(rabbit)

    def move(self):
        """ Rabbits move """
        for r in self.rabbits:
            r.move()

    def eat(self):
        """ Rabbits eat (if they find grass where they are) """

        for rabbit in self.rabbits:
            rabbit.eat(self.field[rabbit.x, rabbit.y])
            self.field[rabbit.x, rabbit.y] = 0

    def survive(self):
        """ Rabbits who eat some grass live to eat another day """
        self.rabbits = [r for r in self.rabbits if r.eaten > 0]

    def reproduce(self):
        """ Rabbits reproduce like rabbits. """
        born = []
        for rabbit in self.rabbits:
            for _ in range(rnd.randint(1, rabbit.offspring)):
                born.append(rabbit.reproduce())
        self.rabbits += born

        # Capture field state for historical tracking
        rabbit_count = self.num_rabbits()
        self.npygmy.append(rabbit_count[0])
        self.ncotton.append(rabbit_count[1])
        self.ngrass.append(self.amount_of_grass())

    def grow(self):
        """ Grass grows back with some probability """
        growloc = (np.random.rand(SIZE, SIZE) < GRASS_RATE) * 1
        self.field = np.maximum(self.field, growloc)

    def get_rabbits(self):
        rabbits = np.zeros(shape=(SIZE, SIZE), dtype=int)
        for r in self.rabbits:
            rabbits[r.x, r.y] = 1
        return rabbits

    def num_rabbits(self):
        """ How many rabbits are there in the field ? """

        # return len(self.rabbits)
        rabbit_list = [1 if rabbit.color == 'blue' else 0 for rabbit in self.rabbits]
        return rabbit_list.count(1), rabbit_list.count(0)

    def amount_of_grass(self):
        return self.field.sum()

    def generation(self):
        """ Run one generation of rabbits """
        self.move()
        self.eat()
        self.survive()
        self.reproduce()
        self.grow()

    def animate(self, i, speed=1):
        """ Animate one frame of the simulation"""

        # Run some number of generations before rendering next frame
        for n in range(speed):
            self.generation()

        # Update the frame
        self.im.set_array(self.field)
        plt.title("generation = " + str((i + 1) * speed))
        return self.im,

    def run(self, generations=10000, speed=1):
        """ Run the simulation. Speed denotes how may generations run between successive frames """
        anim = animation.FuncAnimation(self.fig, self.animate, fargs=(
            speed, ), frames=generations // speed, interval=1, repeat=False)
        plt.show()

    def history(self, showTrack=True, showPercentage=True, marker='.'):
        plt.figure(figsize=(6, 6))
        plt.xlabel("# Pygmy")
        plt.ylabel("# Cotton Tail")

        xs = self.npygmy[:]
        if showPercentage:
            maxpygmy = max(xs)
            xs = [x / maxpygmy for x in xs]
            plt.xlabel("% Pygmy Rabbits")

        ys = self.ncotton[:]
        if showPercentage:
            maxcotton = max(ys)
            ys = [y / maxcotton for y in ys]
            plt.ylabel("% Cotton Tail Rabbits")

        if showTrack:
            plt.plot(xs, marker=marker)
            # plt.plot(ys, marker=marker)
        else:
            plt.scatter(xs, ys, marker=marker)

        plt.grid()

        plt.title(" Pygmy Rabbits vs. Cotton Tail Rabbits")
        plt.savefig("history.png", bbox_inches='tight')
        plt.show()

    # def history2(self):

    #     xs = self.nrabbits[:]
    #     ys = self.ngrass[:]

    #     sns.set_style('dark')
    #     f, ax = plt.subplots(figsize=(7, 6))

    #     sns.scatterplot(x=xs, y=ys, s=5, color=".15")
    #     sns.histplot(x=xs, y=ys, bins=50, pthresh=.1, cmap="mako")
    #     sns.kdeplot(x=xs, y=ys, levels=5, color="r", linewidths=1)
    #     plt.grid()
    #     plt.xlim(0, max(xs)*1.2)

    #     plt.xlabel("# Rabbits")
    #     plt.ylabel("# Grass")
    #     plt.title("Rabbits vs. Grass: GROW_RATE =" + str(GRASS_RATE))
    #     plt.savefig("history2.png", bbox_inches='tight')
    #     plt.show()


def main():

    # Create the ecosystem
    field = Field(num_pygmy=10, num_cotton_tail=10)

    # Run the ecosystem
    field.run(generations=5000, speed=1)

    # Plot history
    field.history(showPercentage=False)
    # field.history2()


if __name__ == '__main__':
    main()
