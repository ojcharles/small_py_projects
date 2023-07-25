# A program that runs Conway's game of life as defined in wikipedia

import numpy as np
import cv2
from numba import njit

width = 1000
height = 1000
rounds = 10
fps = 1

@njit
def get_sum_neighbours(board: np.ndarray, iter_y: int, iter_x: int):
    # how many neighbours are 1?
    y_min = iter_y -1 if iter_y -1 > -1 else 0
    y_max = iter_y +1 if iter_y +1 < height  else height
    x_min = iter_x -1 if iter_x -1 > -1 else 0
    x_max = iter_x +1 if iter_x +1 < width  else width
    neighbour_grid = board[y_min:y_max+1,x_min:x_max+1]
    sum_neighbours = np.sum(neighbour_grid)
    return sum_neighbours

@njit
def handle_loop_through_points(board, board_new, height, width):
    for iter_y in range(height):
        for iter_x in range(width):
            if board[iter_y, iter_x] == 1:
                sum_neighbours = get_sum_neighbours(board, iter_y, iter_x)
                # remove self
                sum_neighbours = sum_neighbours - 1
                # rule 1: Any live cell with fewer than two live neighbours dies, as if by underpopulation.
                # rule 2: Any live cell with two or three live neighbours lives on to the next generation.
                # rule 3: Any live cell with more than three live neighbours dies, as if by overpopulation.
                if sum_neighbours < 2 or sum_neighbours > 3:
                    board_new[iter_y, iter_x] = 0
            else:
                # rule 4: Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
                sum_neighbours = get_sum_neighbours(board, iter_y, iter_x)
                if sum_neighbours == 3:
                    board_new[iter_y, iter_x] = 1

board = np.random.choice([0, 1], size=(height, width))
print(board)
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
video = cv2.VideoWriter('gol.mp4', fourcc, float(fps), (width, height), False)
for round in range(rounds):
    print(round)
    board_new = board.copy()
    handle_loop_through_points(board, board_new, height, width)
    board = board_new.copy()
    print(board)
    board_new[board_new==1]=255
    video.write(board.astype( np.uint8, copy=False))
video.release()