﻿import matplotlib.pyplot as plt
import itertools
import random
import copy

"""
Schelling Model code from:
https://www.binpress.com/tutorial/introduction-to-agentbased-models-an-implementation-of-schelling-model-in-python/144
"""


class Schelling:
    def __init__(self,
                 width, height,
                 empty_ratio,
                 similarity_threshold,
                 n_iterations, races=2):
        self.width = width
        self.height = height
        self.races = races
        self.empty_ratio = empty_ratio  # Int limitation?
        self.similarity_threshold = similarity_threshold
        self.n_iterations = n_iterations
        self.empty_houses = []
        self.agents = {}

    def populate(self):
        # Creates a list of coordinates of the houses
        self.all_houses = list(itertools.product(
            range(self.width),
            range(self.height)))

        # Randomizing houses for easier slicing
        random.shuffle(self.all_houses)

        # Getting indices of empty houses
        self.n_empty = int(self.empty_ratio * len(self.all_houses))
        self.empty_houses = self.all_houses[:self.n_empty]

        # Getting indices of the filled houses
        self.remaining_houses = self.all_houses[self.n_empty:]

        # Assigning race to each house
        # Cycles through the remaining houses and assigns a race number
        houses_by_race = [self.remaining_houses[i::self.races]
                          for i in range(self.race)]
        for i in range(self.races):
            # create agents for each race
            self.agents = dict(
                self.agents.items() +
                dict(zip(houses_by_race[i],
                         [i+1]*len(houses_by_race[i]))).items())

    def is_unsatisfied(self, x, y):
        race = self.agents[(x, y)]
        count_similar = 0
        count_different = 0

        if x > 0 and y > 0 and (x-1, y-1) not in self.empty_houses:
            if self.agents[(x-1, y-1)] == race:
                count_similar += 1
            else:
                count_different += 1
        if y > 0 and (x, y-1) not in self.empty_houses:
            if self.agents[(x, y-1)] == race:
                count_similar += 1
            else:
                count_different += 1
        if x < (self.width-1) and y > 0 and (x+1, y-1) not in self.empty_houses:
            if self.agents[(x+1, y-1)] == race:
                count_similar += 1
            else:
                count_different += 1
        if x > 0 and (x-1, y) not in self.empty_houses:
            if self.agents[(x-1, y)] == race:
                count_similar += 1
            else:
                count_different += 1
        if x < (self.width-1) and (x+1, y) not in self.empty_houses:
            if self.agents[(x+1, y)] == race:
                count_similar += 1
            else:
                count_different += 1
        if x > 0 and y < (self.height-1) and (x-1, y+1) not in self.empty_houses:
            if self.agents[(x-1, y+1)] == race:
                count_similar += 1
            else:
                count_different += 1
        if x > 0 and y < (self.height-1) and (x, y+1) not in self.empty_houses:
            if self.agents[(x, y+1)] == race:
                count_similar += 1
            else:
                count_different += 1
        if x < (self.width-1) and y < (self.height-1) and\
           (x+1, y+1) not in self.empty_houses:
            if self.agents[(x+1, y+1)] == race:
                count_similar += 1
            else:
                count_different += 1

        if (count_similar+count_different) == 0:
            return False
        else:
            return float(count_similar) /\
                (count_similar+count_different) < self.happy_threshold

    def update(self):
        for i in range(self.n_iterations):
            self.old_agents = copy.deepcopy(self.agents)
            n_changes = 0
            for agent in self.old_agents:
                if self.is_unhappy(agent[0], agent[1]):
                    agent_race = self.agents[agent]
                    empty_house = random.choice(self.empty_houses)
                    self.agents[empty_house] = agent_race
                    del self.agents[agent]
                    self.empty_houses.remove(empty_house)
                    self.empty_houses.append(agent)
                    n_changes += 1
            print(n_changes)
            if n_changes == 0:
                break


    def move_to_empty(self, x, y):
        race = self.agents[(x, y)]
        empty_house = random.choice(self.empty_houses)
        self.updated_agents[empty_house] = race
        del self.updated_agents[(x, y)]
        self.empty_houses.remove(empty_house)
        self.empty_houses.append((x, y))

    def plot(self, title, file_name):
        fig, ax = plt.subplots()
        # If you want to run the simulation with more than 7 colors,
        # you should set agent_colors accordingly
        agent_colors = {1: 'b', 2: 'r', 3: 'g', 4: 'c', 5: 'm', 6: 'y', 7: 'k'}
        for agent in self.agents:
            ax.scatter(agent[0]+0.5, agent[1]+0.5,
                       color=agent_colors[self.agents[agent]])

        ax.set_title(title, fontsize=10, fontweight='bold')
        ax.set_xlim([0, self.width])
        ax.set_ylim([0, self.height])
        ax.set_xticks([])
        ax.set_yticks([])
        plt.savefig(file_name)

    def calculate_similarity(self):
        similarity = []
        for agent in self.agents:
            count_similar = 0
            count_different = 0
            x = agent[0]
            y = agent[1]
            race = self.agents[(x, y)]
            if x > 0 and y > 0 and (x-1, y-1) not in self.empty_houses:
                if self.agents[(x-1, y-1)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            if y > 0 and (x, y-1) not in self.empty_houses:
                if self.agents[(x, y-1)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            if x < (self.width-1) and y > 0 and (x+1, y-1)\
               not in self.empty_houses:
                if self.agents[(x+1, y-1)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            if x > 0 and (x-1, y) not in self.empty_houses:
                if self.agents[(x-1, y)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            if x < (self.width-1) and (x+1, y) not in self.empty_houses:
                if self.agents[(x+1, y)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            if x > 0 and y < (self.height-1) and (x-1, y+1)\
               not in self.empty_houses:
                if self.agents[(x-1, y+1)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            if x > 0 and y < (self.height-1) and (x, y+1)\
               not in self.empty_houses:
                if self.agents[(x, y+1)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            if x < (self.width-1) and y < (self.height-1)\
               and (x+1, y+1) not in self.empty_houses:
                if self.agents[(x+1, y+1)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            try:
                similarity.append(float(count_similar) /
                                  (count_similar+count_different))
            except:
                similarity.append(1)

        return sum(similarity)/len(similarity)

similarity_threshold_ratio = {}
for i in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
    schelling = Schelling(50, 50, 0.3, i, 500, 2)
    schelling.populate()
    schelling.update()
    similarity_threshold_ratio[i] = schelling.calculate_similarity()

fig, ax = plt.subplots()
plt.plot(similarity_threshold_ratio.keys(), similarity_threshold_ratio.values(), 'ro')
ax.set_title('Similarity Threshold vs. Mean Similarity Ratio', fontsize=15, fontweight='bold')
ax.set_xlim([0, 1])
ax.set_ylim([0, 1.1])
ax.set_xlabel("Similarity Threshold")
ax.set_ylabel("Mean Similarity Ratio")
plt.savefig('schelling_segregation_measure.png')
