# imports 
import string
import IPython.display as ip
import random
import time
from colorama import init, Fore, Style

# some custom functions were needed for class methods
from my_module.functions import add, subtract


class LabRat():
# defining the bot itself and its attributes

    icon = '⚉'
    def __init__(self, position=[2, 2], moves=[[0, 2], [1, 0]]):
        self.position = position
        # keeps track of the bot's current position
        
        self.moves = moves
        # bank of moves on x and y axes
        
        self.nextmove = []
        # keeps track of where the bot is moving next
        
        self.moves_made = []
        # keeps track of where in the grid the bot has been
        
        
    def valid_move(self, grid, pos):
    # checks if a specific space is valid
    
        if grid[pos[0]][pos[1]] == '.' or grid[pos[0]][pos[1]] == 'X':
            return True
        else:
            return False

    def update(self, direction):
    # updates the 'nextmove' attribute 
    
        self.nextmove = self.position
        # first updates nextmove to make sure its baseline is the current position
        
        if direction == 'w':
            self.nextmove = subtract(self.nextmove, self.moves[1])
        elif direction == 'a':
            self.nextmove = subtract(self.nextmove, self.moves[0])
        elif direction == 's':
            self.nextmove = add(self.nextmove, self.moves[1])
        elif direction == 'd':
            self.nextmove = add(self.nextmove, self.moves[0])
            
        # directions are based on 'WASD' inputs for simplicity.
        # rather than four possible moves in the bot's move bank, i opted to use two and add or subtract them accordingly
       
    
    def test_move(self, direction, grid):
    # takes in proposed movement direction and determines if the target space is valid without changing attributes
        pos = self.position
        # first assigns the bot position value to a variable in order to prevent accidentally modifying bot position itself
        if direction == 'w':
            return self.valid_move(grid, subtract(pos, self.moves[1]))
        elif direction == 'a':
            return self.valid_move(grid, subtract(pos, self.moves[0]))
        elif direction == 's':
            return self.valid_move(grid, add(pos, self.moves[1]))
        elif direction == 'd':
            return self.valid_move(grid, add(pos, self.moves[0]))
        # returns a bool, similar to valid_move
        
    def move(self, direction, grid):
    # updates bot position attribute using the direction of movement
        self.update(direction)
        # first updates the nextmove attribute 
        if self.valid_move(grid, self.nextmove) == True:
        # then double checks if the move is valid on the current grid. if it is:
            self.position = self.nextmove
            #updates position
        else:
            return False
        # or it says no
        
    def detect_surroundings(self, grid):
    # keeps track of all adjacent spaces + returns a list of viable directions to move
        possibilities = []
        pos = self.position
        if self.valid_move(grid, add(pos, self.moves[1])) == True:
            possibilities.append('s')
            # checks if space below current position is a boundary and adds it to the list of viable moves if it isn't
        if self.valid_move(grid, subtract(pos, self.moves[1])) == True:
            possibilities.append('w')
            # checks if space above current position is a boundary and adds it to the list of viable moves if it isn't
        if self.valid_move(grid, add(pos, self.moves[0])) == True:
            possibilities.append('d')
        if self.valid_move(grid, subtract(pos, self.moves[0])) == True:
            possibilities.append('a')
        return possibilities
    
    def detect_wherefrom(self, grid):
    # keeps track of where the bot has been + returns a list of viable and novel directions to move
        possibilities = []
        pos=self.position
        # creates variable with position value to avoid accidental modification of position
        if add(pos, self.moves[1]) not in self.moves_made and self.valid_move(grid, add(pos, self.moves[1])):
        # checks for newness and for validity
            possibilities.append('s')
        if subtract(pos, self.moves[1]) not in self.moves_made and self.valid_move(grid, subtract(pos, self.moves[1])):
            possibilities.append('w')
        if add(pos, self.moves[0])not in self.moves_made and self.valid_move(grid, add(pos, self.moves[0])):
            possibilities.append('d')
        if subtract(pos, self.moves[0]) not in self.moves_made and self.valid_move(grid, subtract(pos, self.moves[0])):
            possibilities.append('a')
        return possibilities
        # similar to detect_surroundings, it returns a list of possible moves
        # because this list also considers novelty, it's used as a higher priority than the list returned by detect_surroundings
    
class Level():
# for easily tracking level attributes
    def __init__(self, grid, win_state):
        self.grid = grid
        # current grid
        self.win_state = win_state
        # position on board that, when reached, triggers the bot to stop running 
        
# the grids i premade for the three default levels
grid1 = [ '=====LEVEL ONE======',
    '■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■',
    '■ . ■ . . . ■ . ■ . X',
    '■ . ■ . ■ . ■ . ■ . ■',
    '■ . ■ . ■ . ■ . ■ . ■',
    '■ . ■ ■ ■ . . . ■ . ■',
    '■ . . . . . ■ . ■ . ■',
    '■ ■ ■ ■ ■ . ■ . ■ . ■',
    '■ . . . . . ■ . . . ■',
    '■ . ■ ■ ■ ■ ■ ■ ■ . ■',
    '■ . . . . . . . . . ■',
    '■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■'
]
grid2 = [ '=====LEVEL TWO =====',
    '■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■',
    '■ . ■ . . . ■ . ■ . . . . . . ■ . . . ■',
    '■ . ■ . ■ ■ ■ . ■ ■ ■ ■ ■ ■ . ■ . ■ . ■',
    '■ . ■ . ■ . . . . . . . . ■ . ■ . ■ . ■',
    '■ . ■ . ■ ■ ■ ■ ■ ■ ■ ■ . ■ . ■ . ■ . ■',
    '■ . ■ . . . . . . . . ■ . ■ . . . ■ . ■',
    '■ . ■ ■ ■ ■ ■ ■ ■ ■ . ■ . ■ . ■ ■ ■ . ■',
    '■ . . . . . . . . . . ■ . . . . . . . ■',
    '■ . ■ ■ ■ ■ ■ ■ ■ . ■ ■ . ■ . ■ . ■ . ■',
    '■ . ■ . . . . . ■ . . . . ■ . ■ . . . ■',
    '■ . ■ . ■ ■ ■ . ■ ■ ■ ■ ■ ■ . ■ ■ ■ ■ ■',
    '■ . ■ . . . ■ . . . . . . . . . . . . ■',
    '■ . ■ ■ ■ . ■ ■ ■ ■ ■ ■ ■ ■ . ■ . ■ . ■',
    '■ . . . . . . . . . . . . . . ■ . ■ . ■',
    '■ . ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ . ■ . ■ . ■ . ■',
    '■ . . . . . . . . . . . . ■ . . . ■ . ■',
    '■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ X ■'
    
]
grid3 = [ '=====LEVEL THREE======',
    '■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■', 
    '■ . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ■',
    '■ . ■ ■ ■ . ■ ■ ■ ■ ■ . ■ ■ ■ ■ ■ ■ ■ ■ ■ . ■ ■ ■ ■ ■ ■ ■ . ■',
    '■ . ■ . ■ . ■ . . . . . ■ . . . . . . . ■ . . . . . . . ■ . ■',
    '■ . ■ . ■ . ■ . ■ ■ ■ . ■ . ■ ■ ■ ■ ■ . ■ ■ ■ ■ ■ ■ ■ . ■ . ■',
    '■ . ■ . ■ . ■ . ■ . . . ■ . . . . . ■ . . . . . . . . . ■ . ■',
    '■ . ■ . . . ■ . ■ . ■ ■ ■ . ■ ■ ■ . ■ . ■ ■ ■ ■ ■ ■ ■ . ■ . ■',
    '■ . ■ . ■ . ■ . ■ . . . . . . . ■ . ■ . . . . . . . ■ . ■ . ■',
    '■ . ■ . ■ . ■ ■ ■ ■ ■ ■ ■ ■ ■ . ■ . ■ . ■ ■ ■ ■ ■ ■ ■ . ■ . ■',
    '■ . ■ . ■ . . . . . . . . . . . ■ . ■ . ■ . . . . . . . ■ . ■',
    '■ . ■ . ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ . ■ . ■ . ■ . ■ ■ ■ ■ ■ ■ ■ . ■',
    '■ . ■ . . . . . . . . . . . ■ . ■ . ■ . ■ . ■ . . . . . . . ■',
    '■ . ■ ■ ■ ■ ■ ■ ■ ■ ■ . ■ . ■ . ■ . ■ . ■ . ■ ■ ■ ■ ■ ■ ■ ■ ■',
    '■ . . . . . . . . . ■ . ■ . ■ . ■ . ■ . ■ . . . . . . . . . ■',
    '■ . ■ ■ ■ ■ ■ ■ ■ ■ ■ . ■ . ■ ■ ■ . ■ . ■ . ■ ■ ■ ■ ■ ■ ■ . ■',
    '■ . ■ . . . . . . . . . ■ . . . . . ■ . . . . . . . . . . . ■',
    '■ . ■ . ■ ■ ■ ■ ■ ■ ■ ■ ■ . ■ ■ ■ ■ ■ . ■ . ■ . ■ ■ ■ ■ ■ ■ ■',
    '■ . ■ . . . . . . . . . . . . . . . . . ■ . ■ . . . . . . . ■',
    '■ . ■ ■ ■ ■ . ■ . ■ . ■ ■ ■ . ■ ■ ■ ■ . ■ . ■ ■ ■ ■ ■ ■ ■ ■ ■',
    '■ . . . . . . ■ . ■ . . . . . . . . ■ . ■ . . . . . . . . . X',
    '■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■'
]
