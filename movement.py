from types import *
from constants import *
from utils import *
from state import State


def is_a_piece(realCoord: RealCoord, board):
  i, j = real_to_board(realCoord)
  return board[i][j] != 0


def legal_move (
  piece: Piece, 
  boardCoord: BoardCoord, 
  curr_state: State 
  ) -> bool:
  i, j = boardCoord
  board = curr_state.board
  white_piece = is_white_piece(piece)

  # same cell
  if boardCoord == curr_state.last_postion:
    return False
  
  cell_piece = board[i][j]
  if cell_piece != VOID and is_white_piece(cell_piece) and white_piece:
    return False
  
  return True


def can_castle(king: BoardCoord, rook: BoardCoord, state: State) -> bool:
  board = state.board
  
  if king not in state.initial_kings:
    return False
  
  if rook not in state.initial_rooks:
    return False
  
  distance = substract_coords(king, rook)[1]
  
  sig = 1
  if distance < 0:
    distance *= -1
    sig = -1
  
  for i in range(1, distance-1):
    if board[king[0]][king[1] + (i * sig)] != VOID:
      return False
