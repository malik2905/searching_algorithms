from maze import *
from util import *
import pygame
import sys
import os
import time
import random
import copy


pygame.init()
BORDER = 15
WIDTH, HEIGHT = 1200, 600
WINDOW_WIDTH, WINDOW_HEIGHT = WIDTH + 2 * BORDER, HEIGHT + 2 * BORDER + 50
GRID = 50
BUTTON_WIDTH, BUTTON_HEIGHT = 240, 40
MAZE_BUTTON_WIDTH, MAZE_BUTTON_HEIGHT = 180 + 2 * BORDER, 160
SMALL_LINE = 1
BIG_LINE = 4
WHITE = (255, 255, 255)
GREY_LIGHT = (200, 200, 200)
GREY_DARK = (140, 140, 140)
BLUE_LIGHT = (180, 198, 231)
BLUE_DARK = (142, 170, 219)
GREEN_LIGHT = (197, 224, 179)
GREEN_DARK = (168, 208, 141)
BLACK = (0, 0, 0)
FONT_VALUES = pygame.font.SysFont('Times New Roman', 34)
FONT_NUMBERS = pygame.font.SysFont('Times New Roman', 20)
FONT_LETTERS = pygame.font.SysFont('Times New Roman', 20)
SPEED = 0.1
MAZE = None
MAZE_VALUES = None
GRID_WIDTH, GRID_HEIGHT = 24, 12
FPS = 60
ACTIVE = False
ALGORITHM = None
RUN = True
SHOW_VALUES = False

BLUE = pygame.image.load(
     os.path.join('colors', 'blue.png'))
BLUE = pygame.transform.scale(BLUE, (GRID, GRID))
RED = pygame.image.load(
     os.path.join('colors', 'red.png'))
RED = pygame.transform.scale(RED, (GRID, GRID))
GREEN = pygame.image.load(
     os.path.join('colors', 'green.png'))
GREEN = pygame.transform.scale(GREEN, (GRID, GRID))
YELLOW = pygame.image.load(
     os.path.join('colors', 'yellow.png'))
YELLOW = pygame.transform.scale(YELLOW, (GRID, GRID))
PURPLE = pygame.image.load(
     os.path.join('colors', 'purple.png'))
PURPLE = pygame.transform.scale(PURPLE, (GRID, GRID))
WHITE_BACKGROUND = pygame.image.load(
     os.path.join('colors', 'white.png'))
WHITE_BACKGROUND = pygame.transform.scale(WHITE_BACKGROUND, (WIDTH, HEIGHT))
MAZE_1 = pygame.image.load(
     os.path.join('maze', 'maze_1.png'))
MAZE_1 = pygame.transform.scale(MAZE_1, (MAZE_BUTTON_WIDTH - 20, 100))
MAZE_2 = pygame.image.load(
     os.path.join('maze', 'maze_2.png'))
MAZE_2 = pygame.transform.scale(MAZE_2, (MAZE_BUTTON_WIDTH - 20, 100))
MAZE_3 = pygame.image.load(
     os.path.join('maze', 'maze_3.png'))
MAZE_3 = pygame.transform.scale(MAZE_3, (MAZE_BUTTON_WIDTH - 20, 100))
MAZE_4 = pygame.image.load(
     os.path.join('maze', 'maze_4.png'))
MAZE_4 = pygame.transform.scale(MAZE_4, (MAZE_BUTTON_WIDTH - 20, 100))
MAZE_5 = pygame.image.load(
     os.path.join('maze', 'maze_5.png'))
MAZE_5 = pygame.transform.scale(MAZE_5, (MAZE_BUTTON_WIDTH - 20, 100))
MAZE_6 = pygame.image.load(
     os.path.join('maze', 'maze_6.png'))
MAZE_6 = pygame.transform.scale(MAZE_6, (MAZE_BUTTON_WIDTH - 20, 100))

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Searching Algorithms')


def main():
    global MAZE
    global ACTIVE
    global ALGORITHM
    global RUN
    global SHOW_VALUES
    clock = pygame.time.Clock()
    clock.tick(FPS)

    while True:
        while RUN:
            get_events()
            mouse, click = get_mouse_events()
            draw_starting_window(mouse, click)
            if ALGORITHM != None:
                RUN = False
                pygame.time.wait(200)
        
        RUN = True
        while RUN:
            get_events()
            mouse, click = get_mouse_events()
            draw_maze_window(mouse, click)
            if MAZE != None:
                RUN = False
                pygame.time.wait(200)

        RUN = True
        while RUN:
            get_events()
            mouse, click = get_mouse_events()
            draw_window(mouse=mouse, click=click, start=True)
        
        path, steps = search()
        RUN = True
        while RUN:
            get_events()
            mouse, click = get_mouse_events()
            draw_window(path=path, steps=steps, done=True, end=True, mouse=mouse, click=click)
        
        MAZE = None
        ACTIVE = False
        ALGORITHM = None
        RUN = True
        SHOW_VALUES = False


def search():
    global MAZE
    global SHOW_VALUES
    steps = 0
    path = -1
    start, end = get_coordinates()
    start = Node(start, end=end)
    if ALGORITHM == 'DFS':
        data_structure = DFS()
    elif ALGORITHM == 'GBFS':
        data_structure = GBFS()
    elif ALGORITHM == 'a_star':
        data_structure = A_STAR()
    else:
        data_structure = BFS()
    visited = []
    data_structure.add(start)
    while not data_structure.empty():
        get_events()
        active_node = data_structure.get_next_node()
        steps = active_node.steps + 1
        path += 1
        visited.append(active_node.state)
        i, j = active_node.state
        if MAZE[i][j] != A and MAZE[i][j] != B:
            MAZE[i][j] = Y
            if ALGORITHM == 'GBFS':
                MAZE_VALUES[i][j] = str(active_node.manhattan_distance)
            elif ALGORITHM == 'a_star':
                MAZE_VALUES[i][j] = str(active_node.a_star)
            mouse, click = get_mouse_events()
            draw_window(path, mouse=mouse, click=click)
            time.sleep(SPEED)
        for n in get_neighbors(active_node):
            if n not in visited:
                if end == n:
                    shortest_path = 0
                    while active_node != start:
                        row, column = active_node.state
                        if MAZE[row][column] != B:
                            MAZE[row][column] = Z
                        shortest_path += 1
                        active_node = active_node.parent
                        get_events()
                        mouse, click = get_mouse_events()
                        draw_window(steps=path, mouse=mouse, click=click, path=shortest_path)
                        time.sleep(SPEED)
                    return shortest_path, path
                data_structure.add(Node(n, parent=active_node, steps=steps, end=end))


def get_neighbors(node):
    get_events()
    neighbors = list()
    row, column = node.state
    coordinates = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    for _ in range(4):
        random.shuffle(coordinates)
        i, j = coordinates.pop()
        if valid_coordinates(i + row, j + column) and (MAZE[row + i][column + j] == 0 or MAZE[row + i][column + j] == B):
            neighbors.append((row + i, column + j))
    return neighbors


def get_a_star_distance(steps, pos, end):
    return steps + get_manhattan_distance(pos, end)


def get_manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def valid_coordinates(row, column):
    if row < 0 or column < 0 or row >= GRID_HEIGHT or column >= GRID_WIDTH:
        return False
    return True


def get_coordinates():
    start = None
    end = None
    for i, row in enumerate(MAZE):
        for j, val in enumerate(row):
            if val == A:
                start = (i, j)
            elif val == B:
                end = (i, j)
    return start, end


def draw_window(steps=0, done=False, mouse=None, click=None, start=False, end=False, path=None):
    WINDOW.fill(GREY_LIGHT)
    WINDOW.blit(WHITE_BACKGROUND, (BORDER, BORDER))

    for i, row in enumerate(MAZE):
        for j, val in enumerate(row):
            if val != 0:
                if val == A or val == B:
                    WINDOW.blit(YELLOW, (j * GRID + BORDER, i * GRID + BORDER))
                elif val == X:
                    WINDOW.blit(BLUE, (j * GRID + BORDER, i * GRID + BORDER))
                elif val == Y and done == False:
                    WINDOW.blit(PURPLE, (j * GRID + BORDER, i * GRID + BORDER))
                    if SHOW_VALUES:
                        value = FONT_NUMBERS.render(str(MAZE_VALUES[i][j]), True, BLACK)
                        WINDOW.blit(value, (j * GRID + BORDER + 6, i * GRID + BORDER + 2))
                elif val == Y and done == True:
                    WINDOW.blit(RED, (j * GRID + BORDER, i * GRID + BORDER))
                    if SHOW_VALUES:
                        value = FONT_NUMBERS.render(str(MAZE_VALUES[i][j]), True, BLACK)
                        WINDOW.blit(value, (j * GRID + BORDER + 6, i * GRID + BORDER + 2))
                elif val == Z:
                    WINDOW.blit(GREEN, (j * GRID + BORDER, i * GRID + BORDER))
                    if SHOW_VALUES:
                        value = FONT_NUMBERS.render(str(MAZE_VALUES[i][j]), True, BLACK)
                        WINDOW.blit(value, (j * GRID + BORDER + 6, i * GRID + BORDER + 2))
                
                if val != X and val != Y and val != Z:# and A != val != B:
                    value = FONT_VALUES.render(str(val), True, BLACK)
                    WINDOW.blit(value, (j * GRID + 13 + BORDER, i * GRID + 5 + BORDER))
    #'''
    # horizontal
    for i in range(0, 13):
        if i == 0 or i == 12:               
            pygame.draw.line(WINDOW, BLACK, (0 + BORDER, i * GRID + BORDER), (WIDTH + BORDER, i * GRID + BORDER), BIG_LINE)
        else:              
            pygame.draw.line(WINDOW, BLACK, (0 + BORDER, GRID * i + BORDER), (WIDTH + BORDER, GRID * i + BORDER), SMALL_LINE)

     # vertical
    for i in range(0, 25):
        if i == 0 or i == 24:
            pygame.draw.line(WINDOW, BLACK, (GRID * i + BORDER, 0 + BORDER), (GRID * i + BORDER, WIDTH // 2 + BORDER), BIG_LINE)
        else:
            pygame.draw.line(WINDOW, BLACK, (GRID * i + BORDER, 0 + BORDER), (GRID * i + BORDER, WIDTH // 2 + BORDER), SMALL_LINE)
    #'''

    if start:
        draw_button(mouse, BORDER + GRID * 17, WINDOW_HEIGHT - 49, click, 'start', type='start')
        value = FONT_LETTERS.render('Start', True, BLACK)
        WINDOW.blit(value, (BORDER + GRID * 17 + 30, WINDOW_HEIGHT - 46))

    if ALGORITHM in ['GBFS', 'a_star']:
        draw_button(mouse, BORDER + GRID * 20, WINDOW_HEIGHT - 49, click, 'values', type='values')
        value = FONT_LETTERS.render('Values', True, BLACK)
        WINDOW.blit(value, (GRID * 20 + BORDER + 22, WINDOW_HEIGHT - 46))

    if not end:
        value = FONT_LETTERS.render(f'Found path:', True, BLACK)
        WINDOW.blit(value, (GRID * 7 + BORDER, WINDOW_HEIGHT - 46))
        value = FONT_LETTERS.render(f'Steps: {steps} steps', True, BLACK)
        WINDOW.blit(value, (GRID * 3 + BORDER, WINDOW_HEIGHT - 46))
        if path != None:
            value = FONT_LETTERS.render(f'{path} steps', True, BLACK)
            WINDOW.blit(value, (GRID * 9 + BORDER, WINDOW_HEIGHT - 46))

    if end:
        draw_button(mouse, BORDER + GRID * 17, WINDOW_HEIGHT - 49, click, 'restart', type='restart')
        value = FONT_LETTERS.render('Restart', True, BLACK)
        WINDOW.blit(value, (BORDER + GRID * 17 + 21, WINDOW_HEIGHT - 46))
        value = FONT_LETTERS.render(f'Steps: {steps} steps', True, BLACK)
        WINDOW.blit(value, (GRID * 3 + BORDER, WINDOW_HEIGHT - 46))
        value = FONT_LETTERS.render(f'Found path: {path} steps', True, BLACK)
        WINDOW.blit(value, (GRID * 7 + BORDER, WINDOW_HEIGHT - 46))

    pygame.display.update()



def draw_maze_window(mouse, click):
    WINDOW.fill(GREY_LIGHT)
    COLUMN_1, COLUMN_2, COLUMN_3 = 170 + BORDER + (WINDOW_WIDTH // 3 - MAZE_BUTTON_WIDTH) // 2, 170 + 3 * BORDER + MAZE_BUTTON_WIDTH + (WINDOW_WIDTH // 3 - MAZE_BUTTON_WIDTH) // 2, 170 + 5 * BORDER + 2 * MAZE_BUTTON_WIDTH + (WINDOW_WIDTH // 3 - MAZE_BUTTON_WIDTH) // 2
    ROW_1, ROW_2, ROW_3 = 2 * BORDER, 5 * BORDER + MAZE_BUTTON_HEIGHT, 7 * BORDER + MAZE_BUTTON_HEIGHT * 2

    draw_button(mouse, COLUMN_1, ROW_1, click, maze_0, type='maze')
    value = FONT_LETTERS.render('Maze 1', True, BLACK)
    WINDOW.blit(value, (COLUMN_1 + 2 * BORDER + 46, ROW_1 + 127))
    WINDOW.blit(MAZE_1, (COLUMN_1 + 10, ROW_1 + 10))
    
    draw_button(mouse, COLUMN_2, ROW_1, click, maze_1, type='maze')
    value = FONT_LETTERS.render('Maze 2', True, BLACK)
    WINDOW.blit(value, (COLUMN_2 + 2 * BORDER + 46, ROW_1 + 127))
    WINDOW.blit(MAZE_2, (COLUMN_2 + 10, ROW_1 + 10))

    draw_button(mouse, COLUMN_3, ROW_1, click, maze_2, type='maze')
    value = FONT_LETTERS.render('Maze 3', True, BLACK)
    WINDOW.blit(value, (COLUMN_3 + 2 * BORDER + 46, ROW_1 + 127))
    WINDOW.blit(MAZE_3, (COLUMN_3 + 10, ROW_1 + 10))

    draw_button(mouse, COLUMN_1, ROW_2, click, maze_3, type='maze')
    value = FONT_LETTERS.render('Maze 4', True, BLACK)
    WINDOW.blit(value, (COLUMN_1 + 2 * BORDER + 46, ROW_2 + 127))
    WINDOW.blit(MAZE_4, (COLUMN_1 + 10, ROW_2 + 10))

    draw_button(mouse, COLUMN_2, ROW_2, click, maze_4, type='maze')
    value = FONT_LETTERS.render('Maze 5', True, BLACK)
    WINDOW.blit(value, (COLUMN_2 + 2 * BORDER + 46, ROW_2 + 127))
    #WINDOW.blit(MAZE_5, (COLUMN_2 + 10, ROW_2 + 10))

    draw_button(mouse, COLUMN_3, ROW_2, click, maze_5, type='maze')
    value = FONT_LETTERS.render('Maze 6', True, BLACK)
    WINDOW.blit(value, (COLUMN_3 + 2 * BORDER + 46, ROW_2 + 127))
    #WINDOW.blit(MAZE_6, (COLUMN_3 + 10, ROW_2 + 10))

    draw_button(mouse, COLUMN_1, ROW_3, click, maze_6, type='maze')
    value = FONT_LETTERS.render('Maze 7', True, BLACK)
    WINDOW.blit(value, (COLUMN_1 + 2 * BORDER + 46, ROW_3 + 127))

    draw_button(mouse, COLUMN_2, ROW_3, click, None, type='maze')
    value = FONT_LETTERS.render('Maze 8', True, BLACK)
    WINDOW.blit(value, (COLUMN_2 + 2 * BORDER + 46, ROW_3 + 127))

    draw_button(mouse, COLUMN_3, ROW_3, click, None, type='maze')
    value = FONT_LETTERS.render('Create maze', True, BLACK)
    WINDOW.blit(value, (COLUMN_3 + 2 * BORDER + 25, ROW_3 + 127))

    for i in range(3):
            pygame.draw.line(WINDOW, BLACK, (COLUMN_1 + i * (COLUMN_2 - COLUMN_1), ROW_1 + MAZE_BUTTON_HEIGHT - 40), (COLUMN_1 + i * (COLUMN_2 - COLUMN_1) + MAZE_BUTTON_WIDTH - 1, ROW_1 + MAZE_BUTTON_HEIGHT - 40), SMALL_LINE)
            pygame.draw.line(WINDOW, BLACK, (COLUMN_1 + i * (COLUMN_2 - COLUMN_1), ROW_2 + MAZE_BUTTON_HEIGHT - 40), (COLUMN_1 + i * (COLUMN_2 - COLUMN_1) + MAZE_BUTTON_WIDTH - 1, ROW_2 + MAZE_BUTTON_HEIGHT - 40), SMALL_LINE)
            pygame.draw.line(WINDOW, BLACK, (COLUMN_1 + i * (COLUMN_2 - COLUMN_1), ROW_3 + MAZE_BUTTON_HEIGHT - 40), (COLUMN_1 + i * (COLUMN_2 - COLUMN_1) + MAZE_BUTTON_WIDTH - 1, ROW_3 + MAZE_BUTTON_HEIGHT - 40), SMALL_LINE)

    pygame.display.update()


def draw_starting_window(mouse, click):
    WINDOW.fill(GREY_LIGHT)
    COLUMN_1, COLUMN_2 = WINDOW_WIDTH // 2 - BUTTON_WIDTH - BORDER, WINDOW_WIDTH // 2 + BORDER
    ROW_1, ROW_2, ROW_3, ROW_4, ROW_5, ROW_6, ROW_7, ROW_8 = 20, 20 * 2 + BUTTON_HEIGHT, 20 * 3 + BUTTON_HEIGHT * 2, 20 * 4 + BUTTON_HEIGHT * 3, 20 * 5 + BUTTON_HEIGHT * 4, 20 * 6 + BUTTON_HEIGHT * 5, 20 * 7 + BUTTON_HEIGHT * 6, 20 * 8 + BUTTON_HEIGHT * 7

    draw_button(mouse, COLUMN_1, ROW_5, click, 'DFS')
    value = FONT_LETTERS.render('Depth First Search', True, BLACK)
    WINDOW.blit(value, (COLUMN_1 + 44, ROW_5 + 7))

    draw_button(mouse, COLUMN_2, ROW_5, click, 'BFS')
    value = FONT_LETTERS.render('Breadth First Search', True, BLACK)
    WINDOW.blit(value, (COLUMN_2 + 36, ROW_5 + 7))

    draw_button(mouse, COLUMN_1, ROW_6, click, 'GBFS')
    value = FONT_LETTERS.render('Greedy Best First Search', True, BLACK)
    WINDOW.blit(value, (COLUMN_1 + 17, ROW_6 + 7))

    draw_button(mouse, COLUMN_2, ROW_6, click, 'a_star')
    value = FONT_LETTERS.render('A*', True, BLACK)
    WINDOW.blit(value, (COLUMN_2 + 107, ROW_6 + 7))
    
    pygame.display.update()


def draw_button(mouse, x, y, click, button, type=None):
    global ALGORITHM
    global MAZE
    global MAZE_VALUES
    global RUN
    global ACTIVE
    global SHOW_VALUES
    mouse_x, mouse_y = mouse
    if type == 'maze':
        width, height = MAZE_BUTTON_WIDTH, MAZE_BUTTON_HEIGHT
    elif type in ['start', 'restart', 'values']:
        width, height = 100, 30
    else:
        width, height = BUTTON_WIDTH, BUTTON_HEIGHT

    if x < mouse_x < x + width and y < mouse_y < y + height:
        if type == 'values' and SHOW_VALUES:
            pygame.draw.rect(WINDOW, GREEN_LIGHT, (x, y, width, height))
            pygame.draw.rect(WINDOW, BLACK, (x, y, width, height), 2)
        else:
            pygame.draw.rect(WINDOW, BLUE_LIGHT, (x, y, width, height))
            pygame.draw.rect(WINDOW, BLACK, (x, y, width, height), 2)
        if click == (1, 0, 0) and ACTIVE == False:
            ACTIVE = True
            if type == 'maze':
                MAZE = copy.deepcopy(button)
                MAZE_VALUES = copy.deepcopy(button)
            elif type == 'start':
                RUN = False
            elif type == 'restart':
                RUN = False
            elif type == 'values':
                if SHOW_VALUES == True:
                    SHOW_VALUES = False
                else:
                    SHOW_VALUES = True
            else:
                ALGORITHM = button
        if click == (0, 0, 0):
            ACTIVE = False
    else:
        if type == 'values' and SHOW_VALUES:
            pygame.draw.rect(WINDOW, GREEN_DARK, (x, y, width, height))
            pygame.draw.rect(WINDOW, BLACK, (x, y, width, height), 2)
        else:
            pygame.draw.rect(WINDOW, BLUE_DARK, (x, y, width, height))
            pygame.draw.rect(WINDOW, BLACK, (x, y, width, height), 2)


def get_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def get_mouse_events():
    return pygame.mouse.get_pos(), pygame.mouse.get_pressed()


if __name__ == '__main__':
    main()