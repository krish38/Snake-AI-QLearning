import pygame
import numpy as np
import random
import matplotlib.pyplot as plt
import sys

# Defining Variables
width, height = 400, 400
box = 20
rows = 20
FPS = 300

# Colours
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

# AI Variables
learnRate = 0.001
discount = 0.8
episodes = 2000
statsN = 10
epsilon = 0.2

# Q-Table
readModel = input("Do you want to load a pre-existing model (y/n)? ")
if readModel == "y":
    Q = np.load("snakeai/savedModel.npy")
    epsilon = 0
    episodes = 100
else:
    Q = np.zeros([2,2,2,2,2,2,2,2,4])

# Pygame Commands
win = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

# Stats Variables
epRewards = []
epStats = {'ep': [], 'avg': [], 'max': [], 'min': []}

class Snake:
    def __init__(self):
        self.x = box * random.randint(5,15)
        self.y = box * random.randint(5,15)
        self.dir = 2
        self.body = [[self.x,self.y]]
        self.food = [box * random.randint(0,19), box * random.randint(0,19)]
        self.score = 0
        self.reward = 0
        self.gameOver = False
    
    def moveSnake(self):
        # Move the snake
        for piece in range(len(self.body)-1):
            self.body[-(piece+1)] = list(self.body[-(piece+2)])
        if self.dir == 1:
            self.body[0][1] -= box
        elif self.dir == 2:
            self.body[0][0] += box
        elif self.dir == 3:
            self.body[0][1] += box
        elif self.dir == 4:
            self.body[0][0] -= box

        #Check if snake is going in the right direction
        foodDir = [0,0,0,0]
        if self.food[1]<self.body[0][1]:
            foodDir[0]=1
        elif self.food[1]>self.body[0][1]:
            foodDir[2]=1
        if self.food[0]<self.body[0][0]:
            foodDir[3]=1
        elif self.food[0]>self.body[0][0]:
            foodDir[1]=1
        
        if foodDir[self.dir-1]==1:
            self.reward=1
        else:
            self.reward = -1
    
    def checkInbound(self):
        if self.body[0][0]<0 or self.body[0][0]>=(width-box) or self.body[0][1]<0 or self.body[0][1]>=(height-box):
            self.reward = -2
            self.gameOver = True
            return False
        for i in range(len(self.body)-1):
            if self.body[0] == self.body[-(i+1)]:
                self.reward = -2
                self.gameOver = True
                return False
        return True
    
    def checkFood(self):
        if self.body[0] == self.food:
            self.score += 1
            self.reward = 5
            self.body.append([0,0])

            foodInBody = True
            while foodInBody:
                self.food = [box * random.randint(0,19), box * random.randint(0,19)]
                foodInBody=False
                for i in self.body:
                    if self.food==i:
                        foodInBody=True
    
    def resetBoard(self):
        self.x = box * random.randint(5,15)
        self.y = box * random.randint(5,15)
        self.dir = 2
        self.body = [[self.x,self.y]]
        self.food = [box * random.randint(0,19), box * random.randint(0,19)]
        self.score = 0
        self.reward = 0
        self.gameOver = False

    def refreshWindow(self):
        win.fill(white)
        x,y = 0,0
        for i in range(rows):
            x += rows 
            y += rows 
            pygame.draw.line(win, black, (x,0), (x,width))
            pygame.draw.line(win, black, (0,y), (width,y))
        
        self.moveSnake()
        for i in self.body:
            pygame.draw.rect(win, black, (i[0], i[1], box, box))
        self.checkFood()
        pygame.draw.rect(win, red, (self.food[0], self.food[1], box, box))
        pygame.display.update()
    
    def getState(self):
        state = ()

        # Is the snake going in the right direction
        foodDir = [0,0,0,0]
        if self.food[1]<self.body[0][1]:
            foodDir[0]=1
        elif self.food[1]>self.body[0][1]:
            foodDir[2]=1
        if self.food[0]<self.body[0][0]:
            foodDir[3]=1
        elif self.food[0]>self.body[0][0]:
            foodDir[1]=1
        for i in foodDir:
            state += (i,)

        dangerous = [0,0,0,0]
        for direction in range(1,5):
            checkLocation = list(self.body[0])
            if direction == 1:
                checkLocation[1]-=box
            elif direction == 2:
                checkLocation[0]+=box
            elif direction == 3:
                checkLocation[1]+=box
            elif direction == 4:
                checkLocation[0]-=box
                
            for piece in range(len(self.body)-1):
                if checkLocation == self.body[piece+1]:
                    dangerous[direction-1]=1
            if checkLocation[0]<0 or checkLocation[0]>=(width-box) or checkLocation[1]<0 or checkLocation[1]>=(height-box):
                dangerous[direction-1]=1
        for i in dangerous:
            state += (i,)
        
        return state

    def makeMove(self):
        self.refreshWindow()
        self.checkInbound()
        return [self.getState(), self.reward, self.gameOver, self.score]

s = Snake()

for episode in range(episodes):
    s.resetBoard()
    state = s.getState()
    
    done = False 
    while not done:
        if random.uniform(0,1) > epsilon:
            s.dir = np.argmax(Q[state])+1
        else:
            s.dir = np.random.randint(1, 4)
        
        newState, reward, done, score = s.makeMove()
        Q[state + (s.dir-1,)] = Q[state + (s.dir-1,)] + learnRate * (s.reward + discount * np.max(Q[newState]) - Q[state + (s.dir-1,)])
        state = newState
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit(), sys.exit()

        pygame.time.delay(50)
        clock.tick(FPS)
    print(f"Game over on episode {episode+1}, with score {s.score}.")

    epRewards.append(s.score)
    if not episode % statsN:
        average_reward = sum(epRewards[-statsN:])/statsN
        epStats['ep'].append(episode)
        epStats['avg'].append(average_reward)
        epStats['max'].append(max(epRewards[-statsN:]))
        epStats['min'].append(min(epRewards[-statsN:]))

pygame.display.quit()

if readModel == 'y':
    plt.plot(epStats['ep'], epStats['avg'], label="average rewards")
    plt.plot(epStats['ep'], epStats['max'], label="max rewards")
    plt.plot(epStats['ep'], epStats['min'], label="min rewards")
    plt.legend(loc=4)
    plt.show()
else:
    saveModel = input("Do you want to save this model (y/n)? ")
    if saveModel=="y":
        np.save("snakeai/savedModel.npy", Q)
