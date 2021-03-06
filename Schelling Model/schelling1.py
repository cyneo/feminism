﻿import matplotlib.pyplot as plt
import itertools
import random
import copy
import numpy as np
from matplotlib import animation

"""
My own attempt at creating a schelling model.

Steps in Schelling:
Initialization:
- Size
- No. of types
- Occupation Rate
- Threshold
- Create agent

Evolution:
- Relocate
- Check for disatisfied
- % Satisfied

Stopping condition:

Agents must have:
- House location
- Happiness
- id

should update graph at each time step

Does the system always converge for a fixed threshold?
Why do we not implement it such that we use current overall happiness to help
the system converge?
Why do you think that it converges faster when the % filled is smaller?
"""
# seems that not the entire population gets plotted

class agent:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y


def initpop(width, height, occupy_rate, race_ratio=0.5, no_types=2):
    all_houses = list(itertools.product(
        range(width),
        range(height)))
    houses = {(x, y): House(x, y)
              for (x, y) in all_houses}
    for house in all_houses:
        houses[house].neighbors = neighbors(house[0], house[1], all_houses)

    random.shuffle(all_houses)
    n_occupied = int(occupy_rate * len(all_houses))
    # indices of occupied houses
    occupied_houses = all_houses[:n_occupied]
    print(len(occupied_houses))

    # Populating the houses

    for house in occupied_houses:
        if random.random() < race_ratio:
            houses[house].race = 2
        else:
            houses[house].race = 1

    # incides of empty houses
    empty_houses = all_houses[n_occupied:]
    for house in empty_houses:
        houses[house].race = None
    """
    house_color = {0: 'w', 1: 'b', 2: 'r', 3: 'g', 4: 'c',
                   5: 'm', 6: 'y', 7: 'k'}
    for x, y in occupied_houses:
        plt.scatter(x, y, color=house_color[houses[(x, y)].race])

    plt.tight_layout()
    plt.show()
    """
    return houses, occupied_houses, empty_houses


# Check happiness
def check_state(houses, threshold):
    unhappy = []
    occupied_houses = []
    for house in houses.values():
        if house.race:
            occupied_houses.append(house.xy)

    for xy in occupied_houses:
        same = 0
        different = 0
        for neighbor in houses[xy].neighbors:
            if house.race == houses[neighbor].race:
                same += 1

            elif houses[neighbor].race and houses[neighbor].race != house.race:
                different += 1
        try:
            houses[xy].happiness = same / (same+different)
        except ZeroDivisionError:
            houses[xy].happiness = 0
        if houses[xy].happiness < threshold:
            unhappy.append(xy)

    empty_houses = [x for x in list(houses.keys()) if x not in occupied_houses]
    return houses, unhappy, occupied_houses, empty_houses


def move(houses, unhappy, occupied_houses, empty_houses):
    for xy in unhappy:
        occupied_houses.remove(xy)
        move_to = random.randint(0, len(empty_houses) - 1)
        houses[empty_houses[move_to]].race = houses[xy].race
        houses[xy].race = None
        empty_houses.pop(move_to)
        empty_houses.append(xy)
        
    return houses
'''
    # Randomizing houses for easier slicing
    random.shuffle(houses)

    # Getting incides of empty houses
    no_empty = int(width * height * occupy_rate)
    empty = houses[:no_empty]
    occupied = houses[no_empty:]

    # Creating agents
'''


def run(width, height, threshold, occupy_rate=0.9, no_types=2):
    x = initpop(width, height, occupy_rate)
    
    # f, (ax1, ax2) = plt.subplots(1, 2)
    house_color = {0: 'w', 1: 'b', 2: 'r', 3: 'g', 4: 'c',
                   5: 'm', 6: 'y', 7: 'k'}
    # for house in x[0].values():
    #     if house.race:
    #         ax1.scatter(house.x, house.y, color=house_color[house.race])
    
    def main():
        xcord = []
        ycord = []
        color = []
        for house in x[0].values():
            if house.race:
                xcord.append(house.x)
                ycord.append(house.y)
                color.append(house_color[house.race])

        fig = plt.figure()
        scat = plt.scatter(xcord, ycord, c=color, s=100)

        ani = animation.FuncAnimation(fig, update_plot,
                                      fargs=(house_color, scat))
        plt.show()

    def get_data():
        xcord = []
        ycord = []
        color = []

        y = check_state(x[0], threshold)
        z = move(y[0], y[1], y[2], y[3])
        
        for house in z.values():
            if house.race:
                xcord.append(house.x)
                ycord.append(house.y)
                color.append(house.race)

        return xcord, ycord, color
    
    def update_plot(i, house_color, scat):
        xcord, ycord, color = get_data()
        scat.set_offsets([np.asarray(xcord), np.asarray(ycord)])
        scat.set_array(np.asarray(color))
        return scat,

    main()

    """
    # animation function.  This is called sequentially
    def animate(i):
        xcord = []
        ycord = []
        color = []
        y = check_state(x[0], threshold)
        z = move(y[0], y[1], y[2], y[3])
        for house in z.values():
            if house.race:
                xcord.append(house.x)
                ycord.append(house.y)
                color.append(house_color[house.race])

        scat.set_offsets((xcord, ycord))
        scat.set_array(color)

        return scat,


    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate,
                                   frames=200, interval=20, blit=True)

    plt.show()
    """


'''
def main():
    numframes = 100
    numpoints = 10
    color_data = np.random.random((numframes, numpoints))
    x, y, c = np.random.random((3, numpoints))

    fig = plt.figure()
    scat = plt.scatter(x, y, c=c, s=100)

    ani = animation.FuncAnimation(fig, update_plot, frames=range(numframes),
                                  fargs=(numpoints, scat))
    plt.show()

    
def update_plot(i, numpoints, scat):
    x, y, c = np.random.random((3, numpoints))
    scat.set_offsets([x, y])
    scat.set_array(c)
    return scat,

main()
'''

class House:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xy = (x, y)


def neighbors(x, y, houses):
    # Returns a list of tuples of neighbors
    neighbor = [coord for coord in
                list(itertools.product(range(x-1, x+2), range(y-1, y+2)))
                if coord in houses and coord != (x, y)]

    return neighbor

