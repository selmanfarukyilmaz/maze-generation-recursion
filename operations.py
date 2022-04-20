import random

maze = []
Stack = []

X_WALL = "-"
Y_WALL = "|"
ROAD = " "
VISITED = "*"
UNVISITED = "#"
EXIT = "e"
STEP = "."


def is_up_cell_empty(labyrinth, line: int, letter: int, search_char: str, search_index: int, edge_index: int) -> bool:
    if line > edge_index:  # üstü tara #1 #0
        if labyrinth[line - search_index][letter] == search_char:  # -2

            return True
        else:
            return False


def is_down_cell_empty(labyrinth, line: int, letter: int, search_char: str, search_index: int, edge_index: int) -> bool:
    if line < len(labyrinth) - edge_index:  # altı tara #-2 #0
        if labyrinth[line + search_index][letter] == search_char:  # +2
            return True
        else:
            return False


def is_left_cell_empty(labyrinth, line: int, letter: int, search_char: str, search_index: int, edge_index: int) -> bool:
    if letter > edge_index:  # solu tara #1 #0
        if labyrinth[line][letter - search_index] == search_char:  # -2
            return True
        else:
            return False


def is_right_cell_empty(labyrinth, line: int, letter: int, search_char: str, search_index: int,
                        edge_index: int) -> bool:
    if letter < len(labyrinth[0]) - edge_index:  # sağı tara #2 #0
        if labyrinth[line][letter + search_index] == search_char:  # +2
            return True
        else:
            return False


def is_any_empty(labyrinth, line: int, letter: int, empty_neighbours: list, search_char: str, search_index: int,
                 edge_index_right_down: int, edge_index_left_up: int) -> bool:
    if is_right_cell_empty(labyrinth, line, letter, search_char, search_index, edge_index_right_down):  # 2
        empty_neighbours.append("right")

    if is_left_cell_empty(labyrinth, line, letter, search_char, search_index, edge_index_left_up):  # 1
        empty_neighbours.append("left")

    if is_up_cell_empty(labyrinth, line, letter, search_char, search_index, edge_index_left_up):
        empty_neighbours.append("up")

    if is_down_cell_empty(labyrinth, line, letter, search_char, search_index, edge_index_right_down):
        empty_neighbours.append("down")

    if empty_neighbours:
        return True
    else:
        return False


def change(text: str, char: str, index: int) -> str:
    return text[:index] + char + text[(index + 1):]


def maze_printer(maze_height: int):
    for i in range(maze_height * 2 + 1):
        print(maze[i])


def maze_generator(maze_x: int, maze_y: int):
    for i in range(maze_y):
        maze.append(((" " + X_WALL) * maze_x) + " ")
        maze.append((Y_WALL + UNVISITED) * maze_x + Y_WALL)
    maze.append(((" " + X_WALL) * maze_x) + " ")

    random_exit = random.randrange(1, len(maze) - 1)
    maze[random_exit] = change(maze[random_exit], EXIT, len(maze[0]) - 1)
    return random_exit


def maze_digger(line: int, letter: int):
    maze[line] = change(maze[line], VISITED, letter)
    string_maze = "".join(maze)

    while UNVISITED in string_maze:
        print(line, letter, "NEW_STEP---------------------")
        maze_printer(int(len(maze) / 2))

        empty_neighbours = []

        if is_any_empty(maze, line, letter, empty_neighbours, UNVISITED, 2, edge_index_right_down=2,
                        edge_index_left_up=1):

            random_choose = random.randrange(0, len(empty_neighbours))
            chosen_neighbour = empty_neighbours[random_choose]

            Stack.append((line, letter))

            if chosen_neighbour == "right":
                maze[line] = change(maze[line], VISITED, letter + 2)
                maze[line] = change(maze[line], ROAD, letter + 1)
                letter = letter + 2

            if chosen_neighbour == "left":
                maze[line] = change(maze[line], VISITED, letter - 2)
                maze[line] = change(maze[line], ROAD, letter - 1)
                letter = letter - 2

            if chosen_neighbour == "up":
                maze[line - 2] = change(maze[line - 2], VISITED, letter)
                maze[line - 1] = change(maze[line - 1], ROAD, letter)
                line = line - 2

            if chosen_neighbour == "down":
                maze[line + 2] = change(maze[line + 2], VISITED, letter)
                maze[line + 1] = change(maze[line + 1], ROAD, letter)
                line = line + 2

            string_maze = "".join(maze)

        elif Stack:
            line, letter = Stack.pop()

        # else:
        #     line = (random.randrange(0, (2 * maze_height) + 1))
        #     letter = (random.randrange(0, (2 * len_maze) + 1))
        # HİÇBİR ZAMAN GIRMIYOR #TODO


def maze_cleaning(clean_char):
    for i in range(len(maze)):
        for ii in range(len(maze[0])):
            if maze[i][ii] == clean_char:
                maze[i] = change(maze[i], ROAD, ii)





def find_road(line: int, letter: int):
    while True:

        empty_neighbours = []

        maze_printer(int(len(maze) / 2))
        print(line, letter, "NEW_STEP---------------------")
        if is_exit(line, letter):
            print("*****FINISH*****")
            maze_printer(int(len(maze) / 2))
            return

        if is_any_empty(maze, line, letter, empty_neighbours, ROAD, 1, edge_index_right_down=2, edge_index_left_up=1):

            Stack.append((line, letter))

            if empty_neighbours[0] == "right":
                maze[line] = change(maze[line], STEP, letter + 1)
                letter = letter + 1

            if empty_neighbours[0] == "left":
                maze[line] = change(maze[line], STEP, letter - 1)
                letter = letter - 1

            if empty_neighbours[0] == "up":
                maze[line - 1] = change(maze[line - 1], STEP, letter)
                line = line - 1

            if empty_neighbours[0] == "down":
                maze[line + 1] = change(maze[line + 1], STEP, letter)
                line = line + 1

        elif is_dead_end(line, letter):
            maze[line] = change(maze[line], UNVISITED, letter)
            line, letter = Stack.pop()

        else:
            raise Exception("Stack Empty Error")


def is_dead_end(line: int, letter: int):
    empty_neighbours = []
    if not is_any_empty(maze, line, letter, empty_neighbours, ROAD, search_index=1, edge_index_right_down=2,
                        edge_index_left_up=2):
        return True
    else:
        return False


def is_exit(line: int, letter: int):
    empty_neighbours = []

    if is_any_empty(maze, line, letter, empty_neighbours, EXIT, 1, edge_index_right_down=0, edge_index_left_up=0):

        maze_cleaning(UNVISITED)
        return True

    else:
        return False

def start(len_maze: int, maze_height: int):
    random_exit = maze_generator(len_maze, maze_height)
    maze_digger(1, 1)

    maze[random_exit] = change(maze[random_exit], ROAD, len(maze[0]) - 2)

    print("************FINISH*************")
    maze_printer(maze_height)

    maze_cleaning(VISITED)

    find_road(1, 1)