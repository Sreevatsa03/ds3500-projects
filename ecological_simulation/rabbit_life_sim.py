import random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import numpy as np
import copy
import sys
from IPython import display


# Does the field wrap around on itself when rabbits move?
WRAP = True

# colors
WHITE = 0
GREEN = 1
BLUE = 2
RED = 3


class Rabbit:
    """ A furry creature roaming a field in search of grass to eat.
    Mr. Rabbit must eat enough to reproduce, otherwise he will starve. """

    def __init__(self, max_offspring=1, max_hop_distance=1, color=BLUE, field_size=300):
        self.size = field_size
        self.x = rnd.randrange(0, self.size)
        self.y = rnd.randrange(0, self.size)
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
            self.x = (self.x + rnd.choice(mv_lst)) % self.size
            self.y = (self.y + rnd.choice(mv_lst)) % self.size
        else:
            self.x = min(self.size - 1, max(0, (self.x + rnd.choice(mv_lst))))
            self.y = min(self.size - 1, max(0, (self.y + rnd.choice(mv_lst))))


class Pygmy(Rabbit):

    def __init__(self):
        super().__init__(max_offspring=2)


class CottonTail(Rabbit):

    def __init__(self):
        super().__init__(max_hop_distance=2, color=RED)


class Field:
    """ A field is a patch of grass with 0 or more rabbits hopping around
    in search of grass """

    def __init__(self, field_size=300, grass_rate=0.04, num_pygmy=1, num_cotton_tail=1):
        """ Create a patch of grass with dimensions size x size
        and initially no rabbits """

        # set field size
        self.size = field_size

        # set rate that grass grows back next season
        self.grass_rate = grass_rate

        # initialize field
        self.field = np.ones(shape=(self.size, self.size), dtype=int)

        # initialize rabbits
        self.rabbits = [Pygmy() for _ in range(num_pygmy)]
        self.rabbits += [CottonTail() for _ in range(num_cotton_tail)]

        # keep track of number of rabbits per species and amount of grass
        self.npygmy = [num_pygmy]
        self.ncotton = [num_cotton_tail]
        self.ngrass = [self.size * self.size]

        # create colormap
        cmap = colors.ListedColormap(["red", "blue", "white", "green"])
        # cmap = colors.ListedColormap(["white", "green", "blue", "red"])

        # plot of field to use for animation
        # plot_field = copy.deepcopy(self.field)
        # for i in range(len(plot_field)):
        #     for j in range(len(plot_field[i])):
        #         if plot_field[i][j] ==

        self.fig = plt.figure(figsize=(5, 5))
        self.im = plt.imshow(self.field, cmap=cmap,
                             aspect='auto', vmin=0, vmax=1)

    def _move(self):
        """ Rabbits move """
        for r in self.rabbits:
            r.move()
            # self.field[r.x, r.y] = r.color

    def _eat(self):
        """ Rabbits eat (if they find grass where they are) """

        for rabbit in self.rabbits:
            rabbit.eat(self.field[rabbit.x, rabbit.y])
            self.field[rabbit.x, rabbit.y] = 0

    def _survive(self):
        """ Rabbits who eat some grass live to eat another day """
        self.rabbits = [r for r in self.rabbits if r.eaten > 0]

    def _reproduce(self):
        """ Rabbits reproduce like rabbits. """
        born = []
        for rabbit in self.rabbits:
            for _ in range(rnd.randint(1, rabbit.offspring)):
                born.append(rabbit.reproduce())
        self.rabbits += born

        # Capture field state for historical tracking
        rabbit_count = self._num_rabbits()
        self.npygmy.append(rabbit_count[0])
        self.ncotton.append(rabbit_count[1])
        self.ngrass.append(self._amount_of_grass())

    def _grow(self):
        """ Grass grows back with some probability """
        growloc = (np.random.rand(self.size, self.size) < self.grass_rate) * 1
        self.field = np.maximum(self.field, growloc)

    def _get_rabbits(self):
        rabbits = np.zeros(shape=(self.size, self.size), dtype=int)
        for r in self.rabbits:
            rabbits[r.x, r.y] = 1
        return rabbits

    def _num_rabbits(self):
        """ How many rabbits are there in the field ? """

        rabbit_list = [rabbit.color for rabbit in self.rabbits]
        return rabbit_list.count(2), rabbit_list.count(3)

    def _amount_of_grass(self):
        num_grass = np.sum(self.field[self.field == 1])
        return num_grass

    def _generation(self):
        """ Run one generation of rabbits """
        self._move()
        self._eat()
        self._survive()
        self._reproduce()
        self._grow()

    def _animate(self, i, speed=1):
        """ Animate one frame of the simulation"""

        # Run some number of generations before rendering next frame
        for _ in range(speed):
            self._generation()

        # Update the frame
        self.im.set_array(self.field)
        plt.title("generation = " + str((i + 1) * speed))
        return self.im,

    def run(self, generations=5000, speed=1):
        """ Run the simulation. Speed denotes how may generations run between successive frames """
        anim = animation.FuncAnimation(self.fig, self._animate, fargs=(
            speed, ), frames=generations // speed, interval=1, repeat=False)
        plt.show()

    @staticmethod
    def _update(num, x, y, z, line1, line2):
        line1.set_data(x[:num], y[:num])
        line2.set_data(x[:num], z[:num])
        return [line1, line2]

    def history(self, speed=1, marker='.'):
        # initialize plot
        fig, ax = plt.subplots()

        # set lists to plot
        pygmy = np.array(self.npygmy[:])
        cotton = np.array(self.ncotton[:])
        gens = np.arange(len(pygmy))

        # plot figure
        line1, = ax.plot(gens, pygmy, color="b", marker=marker)
        line2, = ax.plot(gens, cotton, color="r", marker=marker)

        ani = animation.FuncAnimation(fig, self._update, len(gens), fargs=[
                                      gens, pygmy, cotton, line1, line2], interval=speed, repeat=False, blit=False)

        # configure plot and display
        plt.legend(labels=["Pygmy", "Cottontail"])
        plt.grid()
        plt.xlabel("Generation")
        plt.ylabel("# Rabbits")
        plt.title("Pygmy Rabbits vs. Cotton Tail Rabbits per Generation")
        plt.savefig("pyg_vs_cot_hist.png", bbox_inches='tight')
        ani.save("pyg_vs_cot_hist.gif", dpi=300, writer=animation.PillowWriter(fps=25))
        plt.show()

    def history2(self, marker='o'):
        # initialize 3D plot
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(projection='3d')

        # set lists to plot
        xs = self.npygmy[:]
        ys = self.ncotton[:]
        zs = self.ngrass[:]

        # plot figure
        ax.scatter(xs, ys, zs, marker=marker)

        # configure plot and display
        plt.grid()
        ax.set_xlabel("# Pygmy")
        ax.set_ylabel("# Cotton Tail")
        ax.set_zlabel("Amount of Grass")
        plt.title("Pygmy Rabbits vs. Cotton Tail Rabbits vs. Amount of Grass")
        plt.savefig("pop_hist.png", bbox_inches='tight')
        plt.show()


def main():

    if len(sys.argv) != 7:

        # run ex: python rabbit_life_sim.py 300 0.04 10 10 1000 10
        print("USAGE: $ python rabbit_life_sim.py <field size> <grass growth rate> <initial pygmy> <initial cottontail> <num generations> <sim speed>")
        sys.exit()

    # Create the ecosystem
    field = Field(field_size=int(sys.argv[1]), grass_rate=float(
        sys.argv[2]), num_pygmy=int(sys.argv[3]), num_cotton_tail=int(sys.argv[4]))

    # Run the ecosystem
    field.run(generations=int(sys.argv[5]), speed=int(sys.argv[6]))

    # Plot history
    field.history(speed=int(sys.argv[6]))
    field.history2()


if __name__ == '__main__':
    main()
