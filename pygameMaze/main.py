import pygame
import math
import random
import numpy as np
import matplotlib.pyplot as graph
from deepQ import Agent
from world import World

def runExperiment(difficulty):
    pygame.init()
    world = World(50,20)

    #world.run()

    scores = []
    nn = Agent(gamma=0.9, epsilon=0.995, alpha=0.00005, inputDims=15,
                    numActions=4, memorySize=10000, batchSize=32, epsilonMin=0.05)

    for i in range(1000):
        done = False
        score = 0
        observation = world.reset(difficulty)
        while not done:
            action = nn.chooseAction(observation)                        #action = whole number
            observation_, reward, done, info = world.step(action, True) #observations = array of elements between 0 and 1
                                                                         #reward = floating point val ,negative = bad, positive = good
                                                                         #done = boolean
            score += reward
            nn.remember(observation, action, reward, observation_, done)
            observation = observation_
            nn.learn()
        
        scores.append(score)

        avg_score = np.mean(scores[max(0, i-20):(i+1)])
        print('episode: ', i,'score: %.2f' % score,
            ' average score %.2f' % avg_score)

    scores = []
    for i in range(100):
        done = False
        score = 0
        observation = world.reset(difficulty)
        while not done:
            observation, score, done, info = world.step(nn.chooseAction(observation), True)
        scores.append(score)

        avg_score = np.mean(scores[max(0, i-20):(i+1)])
        print('episode: ', i,'score: %.2f' % score)


    graph.plot(range(1, len(scores) + 1),scores)
    graph.show()

runExperiment(4)