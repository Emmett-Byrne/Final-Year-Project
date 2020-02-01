from keras.layers import Dense, Activation
from keras.models import Sequential, load_model
from keras.optimizers import Adam
import numpy as np

class ReplayBuffer(object):
    def __init__(self, memorySize, inputShape, numActions, discrete=False):
        self.memorySize = memorySize 
        self.memoryCounter = 0
        self.discrete = discrete
        self.stateMemory = np.zeros((self.memorySize, inputShape))
        self.newStateMemory = np.zeros((self.memorySize, inputShape))
        dtype = np.int8 if self.discrete else np.float32
        self.actionMemory = np.zeros((self.memorySize, numActions), dtype=dtype)
        self.rewardMemory = np.zeros((self.memorySize))
        self.terminalMemory = np.zeros(self.memorySize, dtype=np.float32)

    def storeTransitions(self, state, action, reward, newState, done):
        index = self.memoryCounter % self.memorySize #if we go over the max size of our memory we will overwriting old memory
        self.stateMemory[index] = state
        self.newStateMemory = newState
        if self.discrete:
            actions = np.zeros(self.actionMemory.shape[1])
            actions[action] = 1.0
            self.actionMemory[index] = actions
        else:
            self.actionMemory[index] = actions
        self.rewardMemory[index] = reward
        self.terminalMemory[index] = 1 - done
        self.memoryCounter +=1
    
    def sampleBuffer(self, batchSize): #fill memory
        maxMemory = min(self.memoryCounter, self.memorySize)
        batch = np.random.choice(maxMemory, batchSize)

        states = self.stateMemory[batch]
        actions = self.actionMemory[batch]
        rewards = self.rewardMemory[batch]
        newStates = self.newStateMemory[batch]
        terminal = self.terminalMemory[batch]

        return states, actions, rewards, newStates, terminal

def createDeepQ(learningRate, numActions, inputDims, layer1Dims, layer2Dims):
    model = Sequential([
        Dense(layer1Dims, input_shape=(inputDims,)),
        Activation('relu'),
        Dense(layer2Dims),
        Activation('relu'),
        Dense(numActions)
    ])
    model.compile(optimizer=Adam(lr=learningRate), loss='mse')
    return model

class Agent(object):
    def __init__(self, alpha, gamma, numActions, epsilon, batchSize,
                inputDims, epsilonDecrement=0.996, epsilonMin=0.01,
                memorySize=1000000, fname='model.h5'):
        self.actionSpace = [i for i in range(numActions)]
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilonDecrement = epsilonDecrement
        self.epsilonMin = epsilonMin
        self.batchSize = batchSize
        self.fileName = fname
        self.memory = ReplayBuffer(memorySize, inputDims, numActions, discrete=True)
        self.eval = createDeepQ(alpha, numActions, inputDims, 64, 64)

    def remember(self, state, action, reward, newState, done):
        self.memory.storeTransitions(state, action, reward, newState, done)
    
    def chooseAction(self, state):
        state = state[np.newaxis, :]
        rand = np.random.random()
        if rand < self.epsilon:
            action = np.random.choice(self.actionSpace)
        else:
            actions = self.eval.predict(state)
            action = np.argmax(actions)
        
        return action

    def learn(self):
        if self.memory.memoryCounter > self.batchSize:
            state, action, reward, newState, done = self.memory.sampleBuffer(self.batchSize)

            actionValues = np.array(self.actionSpace, dtype=np.int8)
            actionIndeces = np.dot(action,actionValues)

            eval = self.eval.predict(state)
            next = self.eval.predict(newState)
            target = eval.copy()

            batchIndex = np.arange(self.batchSize, dtype=np.int32)

            target[batchIndex, actionIndeces] = reward + self.gamma*np.max(next, axis=1)*done
            
            _ = self.eval.fit(state,target, verbose=0)

            self.epsilon = self.epsilon*self.epsilonDecrement if self.epsilon > self.epsilonMin else self.epsilonMin