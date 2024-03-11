import pickle
from constants import *
from chess_types import *


# 0 <= x,y <= 8
def board_to_real(coords: BoardCoord):
  """ Takes coord from game matrix and turns into coord in the monitor or window

  Args:
      coords (BoardCoord): coord from game matrix

  Returns:
      RealCoord: coords in the monitor
  """
  i, j = coords
  padding = 5
  return padding + (SCREEN_WIDTH / BOARD_WIDTH) * j,\
          padding + (SCREEN_HEIGHT / BOARD_HEIGHT) * i

# 0 <= x,y <= SCREEN_WIDTH,SCREEN_HEIGHT
def real_to_board(coords: RealCoord):
  """ Takes coords from the monitor (mouse pointer) and turns into board coords

  Args:
      coords (RealCoord): coord from window

  Returns:
      BoardCoord: coords in the game matrix
  """
  x, y = coords
  return int(y // CELL_WIDTH), int(x // CELL_HEIGHT)


# Returns a tuple where [0] is the greater and [1] the lower
def greater_lower(x, y):
  if x > y:
    return x, y
  else:
    return y, x


def is_white_piece(piece: Piece):
  # white is under 10
  return piece < 10


def is_king_piece(piece: Piece):
  # white king = 1 / black king = 11
  return piece % 10 == 1

def piece_name(piece: Piece) -> str:
  return piece_to_name[piece % 10]

def copy(structure):
  return pickle.loads(pickle.dumps(structure))


def substract_coords(c1: BoardCoord, c2: BoardCoord) -> BoardCoord:
  (i, j), (ii, jj) = c1, c2
  return i-ii, j-jj


def initialize_board(board: Board):
  # set white pieces
  board[7][0] = 3
  board[7][1] = 5
  board[7][2] = 4
  board[7][3] = 2
  board[7][4] = 1
  board[7][5] = 4
  board[7][6] = 5
  board[7][7] = 3

  # set black pieces
  board[0][0] = 13
  board[0][1] = 15
  board[0][2] = 14
  board[0][3] = 12
  board[0][4] = 11
  board[0][5] = 14
  board[0][6] = 15
  board[0][7] = 13

  # set pawns
  for i in range(8):
    board[1][i] = 16
    board[6][i] = 6


def print_board(board: Board) -> None:
  for row in board:
    for value in row:
      print(f'{value:>2}', end=' ')
    print()
