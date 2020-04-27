from keras.layers import Dense, Activation
from keras.models import Sequential, load_model
from keras.optimizers import Adam
import numpy as np

class ReplayBuffer(object):
    def __init__(self, memorySize, inputShape, numActions):
        self.memorySize = memorySize
        self.memoryCounter = 0
        self.stateMemory = np.zeros((self.memorySize, inputShape))
        self.newStateMemory = np.zeros((self.memorySize, inputShape))
        self.actionMemory = np.zeros((self.memorySize, numActions), dtype=np.int8)
        self.rewardMemory = np.zeros(self.memorySize)
        self.terminalMemory = np.zeros(self.memorySize, dtype=np.float32)

    def storeTransition(self, state, action, reward, newState, done):
        index = self.memoryCounter % self.memorySize #Overrights old memory if we've exceeded the size of our memory
        self.stateMemory[index] = state
        self.newStateMemory[index] = newState
        actions = np.zeros(self.actionMemory.shape[1])
        actions[action] = 1.0
        self.actionMemory[index] = actions
        self.rewardMemory[index] = reward
        self.terminalMemory[index] = 1 - done
        self.memoryCounter += 1

    def sampleBuffer(self, batchSize):
        memorySize = min(self.memoryCounter, self.memorySize)   #If we've filled up our memory and are overrighting old memory we use 
        batch = np.random.choice(memorySize, batchSize)         #creates a list of size batchsize of random indexes between 0 and memory size

        states = self.stateMemory[batch]
        actions = self.actionMemory[batch]
        rewards = self.rewardMemory[batch]
        newState = self.newStateMemory[batch]
        terminal = self.terminalMemory[batch]

        return states, actions, rewards, newState, terminal

#lr = learning rate, 
#numActions = the number of output nodes
#inputNodes = the number of input nodes
#fc1 = the number of nodes in the first fully connected layer
#fc2 = the number of nodes in the second fully connected layer
def buildQNetwork(lr, numActions, inputNodes, fc1Nodes, fc2Nodes):
    model = Sequential([
                Dense(fc1Nodes, input_shape=(inputNodes,)),
                Activation('relu'),
                Dense(fc2Nodes),
                Activation('relu'),
                Dense(numActions)])

    model.compile(optimizer=Adam(lr=lr), loss='mse')

    return model

#lr = learning rate, 
#numActions = the number of output nodes
#inputNodes = the number of input nodes
#fc1 = the number of nodes in the first fully connected layer
def buildSimpleQNetwork(lr, numActions, inputNodes, fc1Nodes):
    model = Sequential([
                Dense(fc1Nodes, input_shape=(inputNodes,)),
                Activation('relu'),
                Dense(numActions)])

    model.compile(optimizer=Adam(lr=lr), loss='mse')

    return model

class Agent(object):
    def __init__(self, alpha, gamma, numActions, epsilon, batchSize,
                 inputDims, epsilonDecrement=0.996,  epsilonMin=0.01,
                 memorySize=1000000, fname='brain.h5', simple=False):
        self.actions = [i for i in range(numActions)] #create a list to the size mumActions
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilonDecrement = epsilonDecrement
        self.epsilonMin = epsilonMin
        self.batchSize = batchSize
        self.file = fname
        self.memory = ReplayBuffer(memorySize, inputDims, numActions)
        if not simple: self.brain = buildQNetwork(alpha, numActions, inputDims, 256, 256)
        else: self.brain = buildSimpleQNetwork(alpha, numActions, inputDims, 256)

    def remember(self, state, action, reward, newState, done):
        self.memory.storeTransition(state, action, reward, newState, done)

    def chooseAction(self, state):
        state = state[np.newaxis, :] #converts from 1D list to 2D because that's how the network likes it.
        rand = np.random.random()

        #determine if we take a random action
        if rand < self.epsilon:
            action = np.random.choice(self.actions) #takes a completely random action
        else:
            actions = self.brain.predict(state)     #gets a value for each action
            action = np.argmax(actions)             #gets the index of the action with the highest value

        return action

    def learn(self):
        if self.memory.memoryCounter > self.batchSize: #Checks if we've filled up our memory more than our batch size
            state, action, reward, newState, done = self.memory.sampleBuffer(self.batchSize) #samples a piece of memory

            #actions are stored as a 2D list and here we convert it to a 1D list.
            #example: [0,0,1,0] is converted to 2, [0,1,0,0] is converted to 1.
            actionValues = np.array(self.actions, dtype=np.int8)
            actionIndices = np.dot(action, actionValues)

            prediction = self.brain.predict(state)
            predictionNext = self.brain.predict(newState)
            target = prediction.copy()
            batchIndex = np.arange(self.batchSize, dtype=np.int32) #creates list starting at 0 and incrementing to the size of batchSize

            target[batchIndex, actionIndices] = reward + self.gamma*np.max(predictionNext, axis=1)*done #reward + (discountFactor)(Action with highest value)(done)

            self.brain.fit(state, target, verbose=0)
            self.epsilon = self.epsilon*self.epsilonDecrement if self.epsilon > self.epsilonMin else self.epsilonMin #update epsilon

    def saveModel(self):
        self.brain.save(self.file)

    def loadModel(self):
        self.brain = load_model(self.file)