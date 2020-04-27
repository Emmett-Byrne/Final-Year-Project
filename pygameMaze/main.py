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

    scores = []
    nn = agent

    for i in range(1000):
        done = False
        score = 0
        observation = world.reset(difficulty)
        while not done:
            action = nn.chooseAction(observation)                                   #action = Index position of action taken
            newObservation, reward, done = world.step(action, render=False)   #observations = Inputs into the network
                                                                                    #reward = floating point val ,negative = bad, positive = good
                                                                                    #done = boolean
            score += reward
            nn.remember(observation, action, reward, newObservation, done)
            observation = newObservation
            nn.learn()
        
        scores.append(score)

        avg_score = np.mean(scores[max(0, i-20):(i+1)])
        print('episode: ', i,'score: %.2f' % score,
            ' average score %.2f' % avg_score)

    scores = []
    movesTaken = []
    for i in range(100):
        done = False
        score = 0
        observation = world.reset(difficulty)
        moveCount = 0
        while not done:
            observation, score, done = world.step(nn.chooseAction(observation), render=False)
            moveCount += 1
        if score == 100:
            movesTaken.append(moveCount)
        scores.append(score)
        print('episode: ', i,'score: %.2f' % score)

    count = 0
    for score in scores:
        if score == 100:
            count += 1

    averageMove = 0
    if len(movesTaken) > 0:
        for x in movesTaken:
            averageMove += x
        averageMove /= len(movesTaken)

    return count, averageMove, nn

successRates = []
averageMoveTaken = []
timeTaken = []
successRatesSimple = []
averageMoveTakenSimple = []
timeTakenSimple = []

running = True
difficultyLevel = 0
agent = Agent(gamma=0.9, epsilon=0.995, alpha=0.00005, inputDims=15, numActions=4, memorySize=10000, batchSize=32, epsilonMin=0.05)
while running:
    timer = time.perf_counter()
    success, average, agent = runExperiment(difficultyLevel, agent)
    timeTaken.append(time.perf_counter() - timer)
    successRates.append(success)
    averageMoveTaken.append(average)
    if success == 0: running = False
    else: difficultyLevel += 1
highestDifficulty = difficultyLevel

running = True
difficultyLevel = 0
agent = Agent(gamma=0.9, epsilon=0.995, alpha=0.00005, inputDims=15, numActions=4, memorySize=10000, batchSize=32, epsilonMin=0.05, simple=True)
while running:
    timer = time.perf_counter()
    success, average, agent = runExperiment(difficultyLevel, agent)
    timeTakenSimple.append(time.perf_counter() - timer)
    successRatesSimple.append(success)
    averageMoveTakenSimple.append(average)
    if success == 0: running = False
    else: difficultyLevel += 1
highestDifficultySimple = difficultyLevel

print('HighestDifficulty: ', highestDifficulty)
print('HighestDifficultySimple: ', highestDifficultySimple)

graph.plot(range(0, len(successRates)),successRates)
graph.plot(range(0, len(successRatesSimple)),successRatesSimple)
graph.xlabel('Difficulty')
graph.ylabel('Sucess Rate %')
graph.grid(color='c', linestyle='dotted', linewidth=1)
graph.show()

graph.plot(range(0, len(averageMoveTaken)),averageMoveTaken)
graph.plot(range(0, len(averageMoveTakenSimple)),averageMoveTakenSimple)
graph.xlabel('Difficulty')
graph.ylabel('average # of moves taken')
graph.grid(color='c', linestyle='dotted', linewidth=1)
graph.show()

graph.plot(range(0, len(timeTaken)),timeTaken)
graph.plot(range(0, len(timeTakenSimple)),timeTakenSimple)
graph.xlabel('Difficulty')
graph.ylabel('Time Taken')
graph.grid(color='c', linestyle='dotted', linewidth=1)
graph.show()
