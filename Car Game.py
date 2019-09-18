import pygame
import math
import random
import copy

random.seed(7)
pygame.init()
display_size = (960, 540)
window = pygame.display.set_mode(display_size)
pygame.display.set_caption("car")
run = True


class Bot:
    def __init__(self, pos, vel, hidden_layers, target):
        self.x = pos[0]
        self.y = pos[1]
        self.vel = vel
        self.goal = target
        self.seconds = 0
        self.brain_structure = [2, 1]
        index = 1
        for i in hidden_layers:
            self.brain_structure.insert(index, i)
            index += 1
        self.brain = Brain((self.x, self.y), self.brain_structure)
        self.brain.guess()
        self.stop_moving = False
        self.fitness = 0
        self.reached_goal = False

    def move(self):
        if not self.stop_moving:
            angle = self.brain.activation[len(self.brain_structure) - 1][0] * math.tau
            self.x += int(math.cos(angle) * self.vel)
            self.y += int(-(math.sin(angle) * self.vel))
            self.brain.inp = (self.x, self.y)
            self.brain.guess()

    def fitness_function(self):
        if self.reached_goal:
            self.fitness = 10000 / (self.seconds ** 2)
        else:
            self.fitness = 1 / math.sqrt(((self.x - self.goal.x) ** 2) + ((self.y - self.goal.y) ** 2))
        # self.fitness = (1000000 / (self.seconds ** 2) +
                        # (1 / (math.sqrt(((self.x - self.goal.x) ** 2) + ((self.y - self.goal.y) ** 2)))))

    @staticmethod
    def mutate(car, mutate_rate):
        new_bot = copy.deepcopy(car)
        new_bot.fitness = 0
        new_bot.seconds = 0
        for l in range(len(new_bot.brain.weights)):
            for i in range(len(new_bot.brain.weights[l])):
                for j in range(len(new_bot.brain.weights[l][i])):
                    new_bot.brain.weights[l][i][j] += random.normalvariate(0, mutate_rate)
        for l in range(len(new_bot.brain.bias_weights)):
            for i in range(len(new_bot.brain.bias_weights[l])):
                new_bot.brain.bias_weights[l][i] += random.normalvariate(0, mutate_rate)
        return new_bot

    @staticmethod
    def generate_bots(amount, init_pos, vel, layers, target):
        bs = []
        for bot in range(amount):
            bs.append(Bot(init_pos, vel, layers, target))
        return bs

    @staticmethod
    def new_generation(arr_of_bots, n_of_best_bots=3, mutation_rate=.01):
        for bot in arr_of_bots:
            bot.fitness_function()
            bot.x = start_pos[0]
            bot.y = start_pos[1]
            bot.reached_goal = False
            bot.stop_moving = False
        best = Bot.find_best_bots(arr_of_bots, n_of_best_bots)
        for i in range(len(arr_of_bots) - n_of_best_bots):
            best.append(Bot.mutate(best[i % n_of_best_bots], mutation_rate))
        return best

    @staticmethod
    def find_best_bots(arr, n_of_bots):
        fitness = [i.fitness for i in arr]
        best_bots = []
        for i in range(n_of_bots):
            max1 = -1
            index = 0
            index_orig = 0
            for j in range(len(fitness)):
                if fitness[j] > max1:
                    max1 = fitness[j]
                    index = j
                    index_orig = j + i
            fitness.remove(fitness[index])
            best_bots.append(index_orig)
        return [arr[i] for i in best_bots]


class Brain:
    def __init__(self, inp, structure):
        self.structure = structure
        self.inp = inp
        self.hidden_layers = [structure[i] for i in range(1, len(structure) - 1)]
        self.weights = Brain.initialize_weights(structure, False)
        self.bias_weights = Brain.initialize_weights(structure[1:], True)
        self.output = []
        self.activation = []

    @staticmethod
    def initialize_weights(neurons, bias):
        matrix = []
        if bias:
            for i in range(len(neurons)):
                matrix.append([])
                inp = neurons[i - 1]
                oup = neurons[i]
                for j in range(oup):
                    matrix[i].append(random.normalvariate(0, 1) /
                                     (math.sqrt(2 / inp)))
        else:
            for i in range(1, len(neurons)):
                matrix.append([])
                inp = neurons[i - 1]
                oup = neurons[i]
                for j in range(oup):
                    matrix[i - 1].append([])
                    for k in range(inp):
                        matrix[i - 1][j].append(random.normalvariate(0, 1)
                                                / (math.sqrt(2 / neurons[0])))
        return matrix

    def guess(self):
        self.output = []
        self.activation = []
        self.output.append(self.inp)
        self.activation.append(self.inp)
        for neuron_layer in range(1, len(self.structure)):
            self.output.append([])
            self.activation.append([])
            for i in range(self.structure[neuron_layer]):
                guess = 0
                for j in range(self.structure[neuron_layer - 1]):
                    guess += self.activation[neuron_layer - 1][j] * self.weights[neuron_layer - 1][i][j]
                self.output[neuron_layer].append(guess + self.bias_weights[neuron_layer - 1][i])
                if len(self.activation) == len(self.structure):
                    self.activation[neuron_layer].append(
                        Brain.sigmoid(guess + self.bias_weights[neuron_layer - 1][i]))
                else:
                    ans = guess + self.bias_weights[neuron_layer - 1][i]
                    self.activation[neuron_layer].append(ans if ans > 0 else ans * 0.01)

    @staticmethod
    def sigmoid(n):
        try:
            ans = 1 / (1 + math.exp(-n))
        except OverflowError:
            return 1
        return ans


class Goal:
    def __init__(self, pos, radius):
        self.x = pos[0]
        self.y = pos[1]
        self.radius = radius

"""
class Obstacles:
    def __init__(self, points):
        
"""

def check_for_collisions():
    for bot in bots:
        if bot.x >= display_size[0] or bot.x <= 0 or bot.y >= display_size[1] or bot.y <= 0:
            bot.stop_moving = True
            bot.seconds = time
        elif goal.x - goal.radius <= bot.x <= goal.x + goal.radius and\
                goal.y - goal.radius <= bot.y <= goal.y + goal.radius:
            bot.stop_moving = True
            bot.reached_goal = True
        elif not bot.reached_goal:
            bot.seconds = time


def draw_window():
    pygame.draw.circle(window, (0, 50, 150), (goal.x, goal.y), goal.radius)
    for i in range(len(bots) - 1):
        pygame.draw.circle(window, (0, 0, 0), (bots[i + 1].x, bots[i + 1].y), 3)
        bots[i + 1].move()
    pygame.draw.circle(window, (255, 0, 0), (bots[0].x, bots[0].y), 5)
    bots[0].move()


start_pos = int(display_size[0] / 2), int((display_size[1] * 7) / 8)
goal = Goal((400, 40), 10)
bots = Bot.generate_bots(100, start_pos, 5, [5, 5], goal)
time = 0
while run:
    pygame.time.delay(1)
    window.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    check_for_collisions()
    draw_window()
    pygame.display.update()
    if time >= 7:
        bots = Bot.new_generation(bots, 1, .05)
        time = 0
    else:
        time += .03
pygame.quit()
