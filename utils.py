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


def mouse_in_board(realCoord: RealCoord) -> bool:
  x, y = realCoord
  return 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT


def substract_coords(c1: BoardCoord, c2: BoardCoord) -> BoardCoord:
  (i, j), (ii, jj) = c1, c2
  return i-ii, j-jj


def piece_from_coord(boardCoord: BoardCoord, board: Board) -> Piece:
  i,j = boardCoord
  return board[i][j]


def is_a_piece(realCoord: RealCoord, board: Board) -> bool:
  i, j = real_to_board(realCoord)
  return board[i][j] != VOID


def same_color(p1: Piece, p2: Piece) -> bool:
  p1_white = is_white_piece(p1)
  p2_white = is_white_piece(p2)
  return p1_white == p2_white or not p1_white and not p2_white


def initialize_board(board: Board):
  # set white pieces
  board[7][0] = ROOK
  board[7][1] = KNIGHT
  board[7][2] = BISHOP
  board[7][3] = QUEEN
  board[7][4] = KING
  board[7][5] = BISHOP
  board[7][6] = KNIGHT
  board[7][7] = ROOK

  # set black pieces
  board[0][0] = ROOK + 10
  board[0][1] = KNIGHT + 10
  board[0][2] = BISHOP + 10
  board[0][3] = QUEEN + 10
  board[0][4] = KING + 10
  board[0][5] = BISHOP + 10
  board[0][6] = KNIGHT + 10
  board[0][7] = ROOK + 10

  # set pawns
  for i in range(8):
    board[1][i] = 16
    board[6][i] = 6


def print_board(board: Board) -> None:
  for row in board:
    for value in row:
      print(f'{value:>2}', end=' ')
    print()
  print()
