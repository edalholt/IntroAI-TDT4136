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
        return gameState.isLose() or gameState.isWin() or depth == 0

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
        def minMax(gameState, depth, ghost, pacTurn):
            currentAction = None
            # getting the amount of ghosts in the game
            ghostCount = gameState.getNumAgents() -1

            # checking if it is pacman's turn to make a move, or the ghost's
            if not pacTurn:
                # Running the minValue function 
                minEval = +Infinity
                currentAction = None
                # Testing if the game is over
                if (self.terminalTest(gameState, depth+1)):
                    return self.evaluationFunction(gameState), None
                # Iterating over all legal actions for the specific ghost
                for action in gameState.getLegalActions(ghost):
                    if (ghost == ghostCount):
                        # If both ghosts has had their turn, it's pacman's turn to make a move
                        # Thats why we pass in True
                        eval, nextAction = minMax(gameState.generateSuccessor(ghost, action), depth, 1, True)
                    else: 
                        # 1/x ghosts has made a move, ghost+1 allows the next ghost to make a move
                        eval, nextAction = minMax(gameState.generateSuccessor(ghost, action), depth, ghost+1, False)

                    if minEval > eval: 
                        # if the new obtained value is better than the previous, we use this action rather than the previous because the value is better
                        minEval = eval
                        currentAction = action
                return minEval, currentAction
                
            else:
                # Pacmans turn to make a move
                maxEval = -Infinity
                currentAction = None
                # Testing if the game is over
                if (self.terminalTest(gameState, depth)):
                    return self.evaluationFunction(gameState), None
                for action in gameState.getLegalActions(0):
                    # Iterating through all legal actions for pacman
                    eval, nextAction = minMax(gameState.generateSuccessor(0, action), depth-1, ghost, False)
                    if maxEval < eval: 
                        # if the new obtained value is better than the previous, we use this action rather than the previous because the value is better
                        maxEval = eval
                        currentAction = action
                return maxEval, currentAction
        

        
        value, action = minMax(gameState, self.depth, 1, True)
        return action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def terminalTest(self, gameState, depth):
        return gameState.isLose() or gameState.isWin() or depth == 0


        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
    def getAction(self, gameState):
        
        def minMax(gameState, depth, ghost, alpha, beta, pacTurn):
            currentAction = None
             # getting the amount of ghosts in the game
            ghostCount = gameState.getNumAgents() -1

            # checking if it is pacman's turn to make a move, or the ghosts
            if not pacTurn: 
                minEval = +Infinity
                currentAction = None
                # Testing if the game is over
                if (self.terminalTest(gameState, depth+1)):
                    return self.evaluationFunction(gameState), None

                # Iterating over all legal actions for the specific ghost
                for action in gameState.getLegalActions(ghost):
                    if (ghost == ghostCount):
                        # If both ghosts has had their turn, it's pacman's turn to make a move
                        # Thats why we pass in True
                        eval, nextAction = minMax(gameState.generateSuccessor(ghost, action), depth, 1, alpha, beta, True)
                    else: 
                        # 1/x ghosts has made a move, ghost+1 allows the next ghost to make a move
                        eval, nextAction = minMax(gameState.generateSuccessor(ghost, action), depth, ghost+1, alpha, beta, False)
                    if minEval > eval:
                        # if the new obtained value is better than the previous, we use this action rather than the previous because the value is better 
                        minEval = eval
                        currentAction = action
                    
                    beta = min(beta, minEval)
                    # If beta is less than alpha, we not need to take it into account because we will never expand for this action.
                    if beta < alpha: 
                        return minEval, currentAction
                return minEval, currentAction
                
            else:
                # Pacmans turn to make a move
                maxEval = -Infinity
                currentAction = None
                # Testing if the game is over
                if (self.terminalTest(gameState, depth)):
                    return self.evaluationFunction(gameState), None

                # Iterating through all legal actions for pacman
                for action in gameState.getLegalActions(0):
                    eval, nextAction = minMax(gameState.generateSuccessor(0, action), depth-1, ghost, alpha, beta, False)
                    if maxEval < eval: 
                        maxEval = eval
                        currentAction = action
                    alpha = max(maxEval, alpha)
                    # if the new obtained value is better than the previous, we use this action rather than the previous because the value is better
                    if alpha > beta: 
                        return maxEval, currentAction
                return maxEval, currentAction
        

        
        value, action = minMax(gameState, self.depth, 1, -Infinity, Infinity, True)
        return action

    

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
