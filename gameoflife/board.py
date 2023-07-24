# this is a class that defines a board, just some board, so we can do things with.

import numpy as np
import random
import time
import cv2

w = 200
h = 200
rounds = 2
fps = 1
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
video = cv2.VideoWriter('test.mp4', fourcc, float(fps), (w, h), False)

class Board:
    # class init / constructor
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.b = np.zeros((self.width, self.height))
    # class methods
    def ran_fill(self) -> np.ndarray:
        # randomly fills a 2d np array with 1 values, num_entries times
        self.b = np.random.choice([0, 1], size=(self.height, self.width))
    def gol_update(self):
        locs_where_1 = np.where(self.b == 1)
        board.b[locs_where_1[0][0], locs_where_1[1][0]] 
    def get_vars_for_10(self, iter, locs_where):        
        iter_y = locs_where[0][iter]
        iter_x = locs_where[1][iter]
        # how many neighbours are 1
        max_square_shape = self.b.shape[0]
        y_min = iter_y -1 if iter_y -1 > -1 else 0
        y_max = iter_y +1 if iter_y +1 < max_square_shape  else max_square_shape
        x_min = iter_x -1 if iter_x -1 > -1 else 0
        x_max = iter_x +1 if iter_x +1 < max_square_shape  else max_square_shape
        neighbour_grid = self.b[y_min:y_max+1,x_min:x_max+1]
        # neighbour_grid
        sum_neighbours = np.sum(neighbour_grid)
        return iter_y, iter_x, sum_neighbours

# init board
board = Board(w, h)
board.ran_fill()
print(board.b)

# rules in condensed form as in wikipedia
# rule 1: Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# rule 2: Any live cell with two or three live neighbours lives on to the next generation.
# rule 3: Any live cell with more than three live neighbours dies, as if by overpopulation.
def handle_rule123(board, iter_y, iter_x, sum_neighbours) -> int:
    if sum_neighbours < 2 or sum_neighbours > 3:
        new_value = 0
    else:
        new_value =  1
    board[iter_y, iter_x] = new_value
    return board

# rule 4: Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
def handle_rule4(board, iter_y, iter_x, sum_neighbours) -> int:
    if sum_neighbours == 3:
        new_value = 1
    else:
        new_value =  0
    board[iter_y, iter_x] = new_value
    return board

for round in range(rounds):
    locs_where_1 = np.where(board.b == 1)
    locs_where_0 = np.where(board.b == 0)
    locs_where_1_nums = len(locs_where_1[0])
    locs_where_0_nums = len(locs_where_0[0])

    # split the board into a concept and a actioned board
    # if do not copy, it just references and the two are one object only!
    board_new = board.b.copy()

    # for each 1 run rules 1,2,3
    for iter in range(locs_where_1_nums):
        iter_y, iter_x, sum_neighbours = board.get_vars_for_10(iter, locs_where_1)
        handle_rule123(board_new, iter_y, iter_x, sum_neighbours)
        # handle self for 1's
        sum_neighbours = sum_neighbours - 1

    for iter in range(locs_where_0_nums):
        iter_y, iter_x, sum_neighbours = board.get_vars_for_10(iter, locs_where_0)
        handle_rule4(board_new, iter_y, iter_x, sum_neighbours)
            
    board.b = board_new.copy()
    print(board.b)
    board_new[board_new==1]=255
    video.write(board_new.astype( np.uint8, copy=False))
 
video.release()
