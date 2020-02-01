import pygame
import math
import random
import numpy as np

class World:

    def __init__(self, width, height):

        #maze data
        self.width = width
        self.height = height
        self.tileSize = 20
        self.actionsTaken = 0
        self.remainingMoves = math.trunc(self.width * 5)
        
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
        self.generateWorld()
        self.clearStart()
        self.setWorldBounds()

    def generateWorld(self):

        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = self.randomTile()
        
    def randomTile(self):

        normalChance = 10   #0 - plains
        wallChance = 4      #1 - walls
        swampChance = 2     #2 - swamp
        sandChance = 3      #3 - sand
        forestChance = 2    #4 - forest
        lavaChance = 2      #5 - lava

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
            print(self.getLongSight())
            if self.playerX == self.goalX and self.playerY == self.goalY:
                running = False #VICTORY!!!!

    def step(self, action):
        previous = self.remainingMoves
        self.move(action)
        movePointsUsed = self.remainingMoves - previous

    def handkeInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move(0)
        if keys[pygame.K_s]:
            self.move(1)
        if keys[pygame.K_a]:
            self.move(2)
        if keys[pygame.K_d]:
            self.move(3)

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

        if moved:
            tile = self.grid[self.playerY][self.playerX]
            if tile == 0:
                self.remainingMoves -= 0
            if tile == 1:
                self.remainingMoves -= 0
                self.playerX = previousX
                self.playerY = previousY
            if tile == 2 or tile == 4:
                self.remainingMoves -= 3
            if tile == 3:
                self.remainingMoves -= 2
            if tile == 5:
                self.remainingMoves -= 999

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
    def getShortSight(self):
        sight = [
            self.grid[self.playerY - 1][self.playerX],
            self.grid[self.playerY][self.playerX - 1],
            self.grid[self.playerY][self.playerX],
            self.grid[self.playerY][self.playerX + 1],
            self.grid[self.playerY + 1][self.playerX]
        ]
        return sight
        
    def getLongSight(self):
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

pygame.init()
world = World(50,20)
world.run()
