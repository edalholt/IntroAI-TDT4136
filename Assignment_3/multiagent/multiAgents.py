# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from numpy import Infinity
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '1'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    # Testing if the game is over
    def terminalTest(self, gameState, depth):
        return gameState.isLose() or gameState.isWin() or depth == self.depth

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        ghostCount = gameState.getNumAgents()-1
        def minMax(state, depth, ghostIndex, pacTurn):
            # Checking if it is pacmans turn or not
            # Finding best moves for ghosts
            if (not pacTurn):
                minValue = Infinity
                if self.terminalTest(state, depth):
                    return self.evaluationFunction(state)
                # Iterating over all legal actions for a ghost
                for action in state.getLegalActions(ghostIndex):
                    stateSucc = state.generateSuccessor(ghostIndex, action)
                    if ghostIndex == ghostCount:
                        # Pacman's turn to make a move
                        minValue = min(minValue, minMax(stateSucc, depth, 1, True))
                    else:
                        # Next ghost's turn to make a move
                        minValue = min(minValue, minMax(stateSucc, depth, ghostIndex+1, False))
                return minValue
            else:
                maxValue = -Infinity
                if self.terminalTest(state, depth+1):
                    return self.evaluationFunction(state)
                # Iterating over all legal moves for Pacman
                for action in state.getLegalActions(0):
                    sateSucc = state.generateSuccessor(0, action)
                    # Go to ghost after pacman
                    maxValue = max(maxValue, minMax(sateSucc, depth+1, 1, False))
                return maxValue

        maxEval = -Infinity
        legalActions = gameState.getLegalActions(0)
        output = ''
        # Check all legal actions
        for action in legalActions:
            next = gameState.generateSuccessor(0, action)
            nextValue = minMax(next, 0, 1, False)

            # Evaluate the best move from all legal actions
            # Returns: Best action
            if nextValue > maxEval:
                output = action
                maxEval = nextValue
        return output

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def terminalTest(self, gameState, depth):
        return gameState.isLose() or gameState.isWin() or depth == self.depth

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        ghostCount = gameState.getNumAgents()-1
        def minMax(state, depth, ghostIndex, pacTurn, alpha, beta):
            # Checking if it is pacmans turn or not
            # Finding best moves for ghosts
            if (not pacTurn):
                minValue = Infinity
                if self.terminalTest(state, depth):
                    return self.evaluationFunction(state)
                # Iterating over all legal actions for a ghost
                for action in state.getLegalActions(ghostIndex):
                    stateSucc = state.generateSuccessor(ghostIndex, action)
                    if ghostIndex == ghostCount:
                        # Pacman's turn to make a move
                        value = minMax(stateSucc, depth, 1, True, alpha, beta)
                        minValue = min(minValue, value)
                        beta = min(beta, value)
                        if (beta <= alpha):
                            break
                        # Pruning?
                    else:
                        # Next ghost's turn to make a move
                        val = minMax(stateSucc, depth, ghostIndex+1, False, alpha, beta)
                        minValue = min(minValue, val)
                        beta = min(beta, val)
                        if (beta <= alpha):
                            break
                        # Pruning ?
                return minValue
            else:
                maxValue = -Infinity
                if self.terminalTest(state, depth+1):
                    return self.evaluationFunction(state)
                # Iterating over all legal moves for Pacman
                for action in state.getLegalActions(0):
                    sateSucc = state.generateSuccessor(0, action)
                    # Go to ghost after pacman
                    val = minMax(sateSucc, depth+1, 1, False, alpha, beta)
                    maxValue = max(maxValue, val)
                    alpha = max(alpha, val)
                    if (beta <= alpha):
                        break
                        
                    # Pruning?
                return maxValue
                
        maxEval = -Infinity
        alpha = -Infinity
        beta = Infinity
        legalActions = gameState.getLegalActions(0)
        output = ''
        # Check all legal actions
        for action in legalActions:
            next = gameState.generateSuccessor(0, action)
            nextValue = minMax(next, 0, 1, False, alpha, beta)
            # Pruning?
            beta = min(beta, nextValue)
            if (beta <= alpha):
                break

            # Evaluate the best move from all legal actions
            # Returns: Best action
            if nextValue > maxEval:
                output = action
                maxEval = nextValue

        return output

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
