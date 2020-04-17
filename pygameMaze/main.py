import pygame
import math
import random
import numpy as np
import matplotlib.pyplot as graph
import time
from deepQ import Agent
from world import World

def runExperiment(difficulty, agent):
    pygame.init()
    world = World(50,20)

    #world.run()

    scores = []
    nn = agent

    for i in range(1000):
        done = False
        score = 0
        observation = world.reset(difficulty)
        while not done:
            action = nn.chooseAction(observation)                        #action = whole number
            observation_, reward, done, info = world.step(action, False) #observations = array of elements between 0 and 1
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
            observation, score, done, info = world.step(nn.chooseAction(observation), False)
        scores.append(score)
        print('episode: ', i,'score: %.2f' % score)

    count = 0
    for score in scores:
        if score == 100:
            count += 1

    return count, nn

successRates = []
running = True
difficultyLevel = 0
startTime = time.perf_counter()
while running:
    agent = Agent(gamma=0.9, epsilon=0.995, alpha=0.00005, inputDims=15, numActions=4, memorySize=10000, batchSize=32, epsilonMin=0.05)
    success, agent = runExperiment(difficultyLevel, agent)
    successRates.append(success)
    if success < 50: running = False
    else: difficultyLevel += 1
duration = time.perf_counter() - startTime
highestDifficulty = difficultyLevel

successRatesSimple = []
running = True
difficultyLevel = 0
startTime = time.perf_counter()
while running:
    agent = Agent(gamma=0.9, epsilon=0.995, alpha=0.00005, inputDims=15, numActions=4, memorySize=10000, batchSize=32, epsilonMin=0.05, simple=True)
    success, agent = runExperiment(difficultyLevel, agent)
    successRatesSimple.append(success)
    if success < 50: running = False
    else: difficultyLevel += 1
durationSimple = time.perf_counter() - startTime
highestDifficultySimple = difficultyLevel

graph.plot(range(0, len(successRates)),successRates)
graph.plot(range(0, len(successRatesSimple)),successRatesSimple)
graph.show()