import random

maze = []
Stack = []

X_WALL = "-"
Y_WALL = "|"
ROAD = " "
VISITED = "*"
UNVISITED = "#"


def is_up_cell_empty(labyrinth, line: int, letter: int, search_char: str) -> bool:
    if line > 1:  # üstü tara
        if labyrinth[line - 2][letter] == search_char:

            return True
        else:
            return False


def is_down_cell_empty(labyrinth, line: int, letter: int, search_char: str) -> bool:
    if line < len(labyrinth) - 2:  # altı tara
        if labyrinth[line + 2][letter] == search_char:
            return True
        else:
            return False


def is_left_cell_empty(labyrinth, line: int, letter: int, search_char: str) -> bool:
    if letter > 1:  # solu tara
        if labyrinth[line][letter - 2] == search_char:
            return True
        else:
            return False


def is_right_cell_empty(labyrinth, line: int, letter: int, search_char: str) -> bool:
    if letter < len(labyrinth[0]) - 2:  # sağı tara
        if labyrinth[line][letter + 2] == search_char:
            return True
        else:
            return False


def is_any_empty(labyrinth, line: int, letter: int, empty_neighbours: list) -> bool:
    if is_right_cell_empty(labyrinth, line, letter, UNVISITED):
        empty_neighbours.append("right")

    if is_left_cell_empty(labyrinth, line, letter, UNVISITED):
        empty_neighbours.append("left")

    if is_up_cell_empty(labyrinth, line, letter, UNVISITED):
        empty_neighbours.append("up")

    if is_down_cell_empty(labyrinth, line, letter, UNVISITED):
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
        maze.append(((" " + X_WALL) * maze_x) + ROAD)
        maze.append((Y_WALL + UNVISITED) * maze_x + Y_WALL)
    maze.append(((" " + X_WALL) * maze_x) + ROAD)

    random_exit = random.randrange(1, len(maze) - 1)
    maze[random_exit] = change(maze[random_exit], "e", len(maze[0]) - 1)


def maze_digger(line: int, letter: int):
    maze[line] = change(maze[line], VISITED, letter)
    string_maze = "".join(maze)

    while UNVISITED in string_maze:
        print(line, letter, "NEW_STEP---------------------")
        maze_printer(int(len(maze) / 2))

        empty_neighbours = []

        if is_any_empty(maze, line, letter, empty_neighbours):

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


def start(len_maze, maze_height):
    maze_generator(len_maze, maze_height)
    maze_digger(1, 1)
    print("************FINISH*************")
    maze_printer(maze_height)

    for i in range(len(maze)):
        for ii in range(len(maze[0])):
            if maze[i][ii] == "*":
                maze[i] = change(maze[i], " ", ii)

    print("edit")
    maze_printer(maze_height)
