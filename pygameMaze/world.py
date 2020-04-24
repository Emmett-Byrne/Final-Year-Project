import pygame
import math
import random
import numpy as np
import matplotlib.pyplot as graph
from deepQ import Agent

class World:

    def __init__(self, width, height):

        #maze data
        self.width = width
        self.height = height
        self.tileSize = 20
        self.actionsTaken = 0
        self.remainingMoves = math.trunc(self.width * 10 + self.height)
        
        #player data
        self.playerX = math.trunc(2)
        self.playerY = math.trunc(self.height / 2)
        
        #goal data
        self.goalX = math.trunc(self.width - 3)
        self.goalY = math.trunc(self.height / 2)

        #setup
        pygame.display.set_caption('Maze')
        pygame.font.init()
        self.font = pygame.font.SysFont('Ariel', 30)
        self.display = pygame.display.set_mode((self.width * self.tileSize, self.height * self.tileSize))
        self.grid = [[0 for i in range(width)] for j in range(height)]

    def generateWorld(self, dificulty):

        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = self.randomTile(dificulty)
        
    def randomTile(self, dificulty):

        normalChance = 100 - dificulty * 3   #0 - plains
        wallChance = dificulty * 3      #1 - walls
        swampChance = 0     #2 - swamp
        sandChance = 0      #3 - sand
        forestChance = 0    #4 - forest
        lavaChance = 0      #5 - lava

        randomNum = random.randint(0, normalChance + wallChance + sandChance + swampChance + forestChance + lavaChance - 1)
        
        if randomNum < normalChance:
            return 0
        elif randomNum < normalChance + wallChance:
            return 1
        elif randomNum < normalChance + wallChance + swampChance:
            return 2
        elif randomNum < normalChance + wallChance + swampChance + sandChance:
            return 3
        elif randomNum < normalChance + wallChance + swampChance + sandChance + forestChance:
            return 4
        elif randomNum < normalChance + wallChance + swampChance + sandChance + forestChance + lavaChance:
            return 5

        return random.randint(0,2)

    def setWorldBounds(self):
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 or x == 1 or x == self.width - 1 or x == self.width-2:
                    self.grid[y][x] = 1
                if y == 0 or y == 1 or y == self.height - 1 or y == self.height-2:
                    self.grid[y][x] = 1

    def clearStart(self):
        for y in range(3):
            for x in range(3):
                self.grid[self.playerY - 1 + y][self.playerX - 1 + x] = 0
        for y in range(3):
            for x in range(3):
                self.grid[self.goalY - 1 + y][self.goalX - 1 + x] = 0
    
    def run(self):
        running = True
        while running:
            pygame.time.delay(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.handkeInput()

            self.render()
            if self.playerX == self.goalX and self.playerY == self.goalY:
                running = False #VICTORY!!!!

    def reset(self, dificulty):
        self.actionsTaken = 0
        self.remainingMoves = math.trunc(self.width * 10 + self.height)
        
        #player data
        self.playerX = math.trunc(2)
        self.playerY = math.trunc(self.height / 2)
        
        #goal data
        self.goalX = math.trunc(self.width - 3)
        self.goalY = math.trunc(self.height / 2)

        self.generateWorld(dificulty)
        self.clearStart()
        self.setWorldBounds()

        observation = self.getLongSight()
        observation.append(self.playerX)
        observation.append(self.playerY)

        return np.array(observation, dtype=np.float32)

    def step(self, action, render):
        previous = self.remainingMoves
        previousDistance = self.distanceToGoal()
        moveReward = self.move(action)
        distanceReward = -(self.distanceToGoal() - previousDistance)
        reward = distanceReward + moveReward

        done = False
        if self.remainingMoves < 0:
            done = True
            reward = -100
        if self.playerY == self.goalY and self.playerX == self.goalX:
            done = True
            reward = 100
        info = {}
        observation = self.getLongSight()
        observation.append(self.playerX)
        observation.append(self.playerY)

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

        if render:
            self.render()

        return np.array(observation, dtype=np.float32), reward, done, info

    def handkeInput(self):
        previousDistance = self.distanceToGoal()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move(0)
        if keys[pygame.K_s]:
            self.move(1)
        if keys[pygame.K_a]:
            self.move(2)
        if keys[pygame.K_d]:
            self.move(3)
        
        distanceReward = -(self.distanceToGoal() - previousDistance)
        if distanceReward != 0:
            print(distanceReward)

    def move(self, direction):
        self.actionsTaken += 1
        self.remainingMoves -= 1
        previousX = self.playerX
        previousY = self.playerY
        moved = False

        if direction == 0:
            self.playerY -= 1
            moved = True
        if direction == 1:
            self.playerY += 1
            moved = True
        if direction == 2:
            self.playerX -= 1
            moved = True
        if direction == 3:
            self.playerX += 1
            moved = True

        reward = 0
        if moved:
            tile = self.grid[self.playerY][self.playerX]
            if tile == 0:
                self.remainingMoves -= 1
            if tile == 1:
                self.remainingMoves -= 1
                self.playerX = previousX
                self.playerY = previousY
                reward = -2
            if tile == 2 or tile == 4:
                self.remainingMoves -= 3
                reward = 1
            if tile == 3:
                self.remainingMoves -= 2
                reward = 5
            if tile == 5:
                self.remainingMoves -= 999
                reward = -100

        return reward

    def distanceToGoal(self):
        distanceX = self.goalX - self.playerX
        distanceY = self.goalY - self.playerY
        return math.sqrt(distanceX * distanceX + distanceY * distanceY)

    def render(self):
        for x in range(self.height):
            for y in range(self.width):
                self.drawTile(y, x, self.grid[x][y])
                self.drawGoal()
                self.drawPlayaer()
                self.drawText()
        pygame.display.update()

    def drawTile(self, x, y, tileType):
        if tileType == 0:
            pygame.draw.rect(self.display, (127,255,0), (x*self.tileSize, y*self.tileSize, self.tileSize,self.tileSize))
        elif tileType == 1:
            pygame.draw.rect(self.display, (150,150,150), (x*self.tileSize, y*self.tileSize, self.tileSize,self.tileSize))
        elif tileType == 2:
            pygame.draw.rect(self.display, (101,67,33), (x*self.tileSize, y*self.tileSize, self.tileSize,self.tileSize))
        elif tileType == 3:
            pygame.draw.rect(self.display, (227, 199, 75), (x*self.tileSize, y*self.tileSize, self.tileSize,self.tileSize))
        elif tileType == 4:
            pygame.draw.rect(self.display, (53, 112, 24), (x*self.tileSize, y*self.tileSize, self.tileSize,self.tileSize))
        elif tileType == 5:
            pygame.draw.rect(self.display, (219, 102, 44), (x*self.tileSize, y*self.tileSize, self.tileSize,self.tileSize))
    
    def drawText(self):
        textsurface = self.font.render('Movement Points: ' + str(self.remainingMoves), False, (0, 0, 0))
        self.display.blit(textsurface,(10,10))

    def drawPlayaer(self):
        pygame.draw.rect(self.display, (0,0,255), (self.playerX * self.tileSize + self.tileSize * 0.15, 
                                                    self.playerY * self.tileSize + self.tileSize * 0.15, 
                                                    self.tileSize * 0.7,self.tileSize * 0.7))

    def drawGoal(self):
        pygame.draw.rect(self.display, (255,0,0), (self.goalX * self.tileSize + self.tileSize * 0.15, 
                                                    self.goalY * self.tileSize + self.tileSize * 0.15, 
                                                    self.tileSize * 0.7,self.tileSize * 0.7))

    #Get data for Neural Network
    def getShortSight(self): #5
        sight = [
            self.grid[self.playerY - 1][self.playerX],
            self.grid[self.playerY][self.playerX - 1],
            self.grid[self.playerY][self.playerX],
            self.grid[self.playerY][self.playerX + 1],
            self.grid[self.playerY + 1][self.playerX]
        ]
        return sight
        
    def getLongSight(self): #13
        sight = [
            self.grid[self.playerY - 2][self.playerX],
            self.grid[self.playerY - 1][self.playerX - 1],
            self.grid[self.playerY - 1][self.playerX],
            self.grid[self.playerY - 1][self.playerX + 1],
            self.grid[self.playerY][self.playerX - 2],
            self.grid[self.playerY][self.playerX - 1],
            self.grid[self.playerY][self.playerX],
            self.grid[self.playerY][self.playerX + 1],
            self.grid[self.playerY][self.playerX + 2],
            self.grid[self.playerY + 1][self.playerX - 1],
            self.grid[self.playerY + 1][self.playerX],
            self.grid[self.playerY + 1][self.playerX + 1],
            self.grid[self.playerY + 2][self.playerX]
        ]
        return sight

def run():
    pygame.init()
    world = World(50,20)
    world.reset(0)

    world.run()

    scores = []
    nn = Agent(gamma=0.99, epsilon=0.995, alpha=0.00005, inputDims=15,
                    numActions=4, memorySize=1000000, batchSize=64, epsilonMin=0.1)

    for i in range(5000):
            done = False
            score = 0
            observation = world.reset(4)
            while not done:
                action = nn.chooseAction(observation)                       #action = whole number
                observation_, reward, done, info = world.step(action, True) #observations = array of elements between 0 and 1
                                                                            #reward = floating point val ,negative = bad, positive = good
                                                                            #done = boolean
                score += reward
                print(reward)
                nn.remember(observation, action, reward, observation_, int(done))
                observation = observation_
                nn.learn()
            
            scores.append(score)

            avg_score = np.mean(scores[max(0, i-100):(i+1)])
            print('episode: ', i,'score: %.2f' % score,
                ' average score %.2f' % avg_score)

    graph.plot(range(1, len(scores) + 1),scores)
    graph.show()