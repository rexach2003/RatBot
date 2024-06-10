# imports
import string
import IPython.display as ip
import random
import time
from colorama import init, Fore, Style

def add(list1, list2):
    # adds two lists together
    sumlist = []
    for (elem1, elem2) in zip(list1, list2):
        sumlist.append(elem1 + elem2)
    return sumlist

def subtract(list1, list2):
    # subtracts a list from another list
    sublist = []
    for (elem1, elem2) in zip(list1, list2):
        sublist.append(elem1 - elem2)
    return sublist

def color(text, color=Fore.RED, brightness=Style.BRIGHT):
    # makes a string red
    out = f"{brightness}{color}{text}{Style.RESET_ALL}"
    return out

def make_it_rainbow(text):
    # for flair and funsies
    output = ''
    for char in text:
        output = output + color(char, color=random.choice([Fore.RED, Fore.YELLOW, Fore.BLUE, Fore.GREEN]))
    return output
    
def walking(grid, position):
    # generates grid with the bot icon in its current position
    activegrid = grid
    row = activegrid[position[0]].split()
    # finds the appropriate string and splits it into individual characters
    row[int(position[1] / 2)] = color('⚉')
    # adds the icon to its place within the row
    activegrid[position[0]] = ' '.join(row)
    # re-concatenates the row 
    return activegrid
    
def reset(grid):
    # removes the bot icon from the grid
    activegrid = grid
    for i in range(len(activegrid)):
        activegrid[i] = activegrid[i].replace('⚉', color('.', color=Fore.BLACK, brightness=Style.DIM))
    return activegrid

def detect_win_state(grid):
    # finds the position in the grid that has an 'X'
    for row in grid:
    # iterates over the rows
        if 'X' in row:
        # finds the row containing the 'X'
            output = [grid.index(row), grid[grid.index(row)].find('X')]
            # returns position of 'X'
        else:
            continue
    return output
              

def run(bot, level):
    # evaluates inputs and changes the bot position accordingly
    active = level.grid.copy()
    # creates a copy of the level grid to manipulate within the function
    ip.clear_output(True)
    # ensures a clean slate
    active = walking(active, bot.position)
    # generates grid with bot in current place
    for row in active:
        print(row)
    # displays grid
    if len(bot.detect_wherefrom(level.grid)) > 0:
        # checks whether there are any viable adjacent spaces that the bot hasn't already been
        go = random.choice(bot.detect_wherefrom(level.grid))
        # chooses a direction from the generated list of new and viable moves
        if bot.test_move(go, level.grid):
        # checks if moving in the given direction will land on a viable space
            try:
                bot.move(go, level.grid)
                # moves icon in given direction
            except:
                bot.move(random.choice(bot.detect_surroundings(level.grid)), level.grid)
                # to catch false positives
        else:
        # if the chosen direction is not viable
            go = random.choice(bot.detect_wherefrom(level.grid))
            # chooses a new direction from the generated list of new and viable spaces
            if guy.test_move(go, level.grid):
                # repeat of above instructions. while loops resulted in the bot getting stuck repeatedly
                try:
                    bot.move(go, level.grid)
                except:
                    bot.move(random.choice(bot.detect_surroundings(level.grid)), level.grid)
                    # if the second chosen direction also results in an invalid space, default to list of viable spaces only
    else:
    # if all adjacent spaces have already been explored
        bot.moves_made.clear()
        # provides a blank slate so the bot doesn't get stuck
        
    bot.moves_made.append(bot.position)
    # updates list of places bot has already been
    active = reset(active)
    # clears grid
    active = walking(active, bot.position)
    # adds icon to new position
    time.sleep(0.3)
    # wait

def rat_maze(bot, levels):
# assigns a grid and runs the visuals
    level = 1
    # start with level 1
    while level == 1:
    # acts as counter
        while bot.position != levels[0].win_state:
        # detects whether or not the bot has reached the end point
            run(bot, levels[0])
            # displays exploration of grid
        ip.clear_output(True)
        # clears last output
        win_grid = walking(levels[0].grid, levels[0].win_state)
        # creates grid with icon on the end point
        for row in win_grid:
            print(row)
        # displays grid with icon on end point
        print(make_it_rainbow("YOU WIN!"))
        print('would you like to continue? \t> yes \t>no')
        # provides feedback and allows for user to go on to next level or end the session
        response = input()
        if response == 'yes':
            level = level + 1
            # moves on to level 2
        else: 
            level = 0

    while level == 2:
        bot.position = [2, 2]
        # resets bot to original position
        bot.moves_made.clear()
        # clears previous list of explored positions
        while bot.position != levels[1].win_state:
            run(bot, levels[1])
        ip.clear_output(True)
        win_grid = walking(levels[1].grid, levels[1].win_state)
        for row in win_grid:
            print(row)
        print(make_it_rainbow("YOU WIN!"))
        print('would you like to continue? \t> yes \t>no')
        response = input()
        if response == 'yes':
            level = level + 1
        else: 
            level = 0

    while level == 3:
        bot.position = [2, 2]
        bot.moves_made.clear()
        while bot.position != levels[2].win_state:
            run(bot, levels[2])
        ip.clear_output(True)
        win_grid = walking(levels[2].grid, levels[2].win_state)
        for row in win_grid:
            print(row)
        print(make_it_rainbow("YOU WIN!"))
        print(make_it_rainbow("congrats!"))
        break
        # ends the session once the bot reaches the end point of the third level

def run_custom_maze(bot, level):
# runs the bot on a custom grid
    go = True
    bot.position = [2,2]
    # resets bot to start
    bot.moves_made.clear()
    # clears list of previous positions
    while go:
        while bot.position != level.win_state:
        # checks whether bot has reached the end point
            run(bot, level)
            # runs and displays exploration of grid
            if bot.position == level.win_state:
                break
            # stop once it reaches the end point
        ip.clear_output(True)
        # clears last display of grid
        win_grid = walking(level.grid, level.win_state)
        for row in win_grid:
            print(row)
        # displays grid with icon on endpoint
        print(make_it_rainbow("YOU WIN!"))
        print(make_it_rainbow("congrats!"))
        go = False
        # ends loop

    