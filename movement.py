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
  cell_piece = board[i][j]
  white_piece = is_white_piece(piece)

  # same cell
  if boardCoord == curr_state.last_postion:
    return False
  
  if can_castle(piece, curr_state.last_postion, boardCoord, curr_state):
    return True
  
  # same color
  if cell_piece != VOID \
    and (white_piece and is_white_piece(cell_piece))\
    or (not white_piece and not is_white_piece(cell_piece)):
    return False  
  
  return True


def can_castle(selected_piece: Piece, king: BoardCoord, rook: BoardCoord, state: State) -> bool:
  board = state.board
  
  if selected_piece % 10 != KING \
    or piece_from_coord(rook, board) % 10 != ROOK:
    return False
  
  if king not in state.initial_kings:
    return False
  
  if rook not in state.initial_rooks:
    return False
  
  distance = substract_coords(king, rook)[1]
  
  sig = -1
  if distance < 0:
    distance *= -1
    sig = 1
  
  for i in range(1, distance-1):
    if board[king[0]][king[1] + (i * sig)] != VOID:
      return False
    
  return True


def castle_move(king: BoardCoord, rook: BoardCoord, state: State) -> None:
  if king == (7, 4): # white king
    if rook == (7, 7): # short castle
      state.board[7][4] = VOID
      state.board[7][7] = VOID
      state.board[7][6] = KING
      state.board[7][5] = ROOK
    
    else: # long castle
      state.board[7][4] = VOID
      state.board[7][0] = VOID
      state.board[7][1] = VOID
      state.board[7][2] = KING
      state.board[7][3] = ROOK
  
  else: # black king
    if rook == (0, 7): # shot castle
      state.board[0][4] = VOID
      state.board[0][7] = VOID
      state.board[0][6] = KING + 10
      state.board[0][5] = ROOK + 10
    
    else: # long castle
      state.board[0][4] = VOID
      state.board[0][0] = VOID
      state.board[0][1] = VOID
      state.board[0][2] = KING + 10
      state.board[0][3] = ROOK + 10
  
  state.initial_kings.remove(king)
  state.initial_rooks.remove(rook)


def king_can_move(piece_selected: Piece, piece_on_cell: Piece, king: BoardCoord, move: BoardCoord, state: State) -> bool:
  (i, j), (ii, jj) = king, move
  
  distance = max(abs(i-ii), abs(j-jj))
  return distance == 1 and \
    (state.board[ii][jj] == VOID 
      or is_white_piece(piece_selected) != is_white_piece(piece_on_cell))


def pawn_can_move(piece_selected: Piece, piece_on_cell: Piece, pawn: BoardCoord, move: BoardCoord, state: State) -> bool:
  (i, j), (ii, jj) = pawn, move
  
  if pawn in state.pinned_pieces:
    return False
  
  distance = abs(i-ii)
  if j - jj != 0: # cannot move horizontally
    return False
  
  if distance > 2: # cannot move more than two steps
    return False
  
  # only can move two steps at the initial cell
  if distance == 2 and pawn not in state.initial_pawns:
    return False 
  
  # must not be any piece in the cell
  if piece_on_cell != VOID:
    return False
  
  return True


def knight_can_move(piece_selected: Piece, piece_on_cell: Piece, knight: BoardCoord, move: BoardCoord, state: State) -> bool:
  (i, j), (ii, jj) = knight, move
  
  if knight in state.pinned_pieces:
    return False
  
  if piece_on_cell != VOID and same_color(piece_selected, piece_on_cell):
    return False
  
  return (abs(i - ii) == 2 and abs(j - jj) == 1 
    or abs(j - jj) == 2 and abs(i - ii) == 1)
  
  
def bishop_can_move(piece_selected: Piece, piece_on_cell: Piece, bishop: BoardCoord, move: BoardCoord, state: State) -> bool:
  (i, j), (ii, jj) = bishop, move
  
  if bishop in state.pinned_pieces:
    return False
  
  if piece_on_cell != VOID and same_color(piece_selected, piece_on_cell):
    return False
  
  v_distance = abs(i - ii)
  h_distance = abs(j - jj)
  
  if v_distance != h_distance:
    return False
  
  v = 1 if i < ii else -1
  h = 1 if j < jj else -1
  
  for k in range(1, v_distance):
    if piece_from_coord((i+(k*v), j+(k*h)), state.board) != VOID:
      return False                                                  
  
  return True                                        


def can_move_switch(selected_piece: Piece, move: BoardCoord, state: State) -> bool:
  piece_on_cell = piece_from_coord(move, state.board)
  
  return movements[selected_piece%10](
    selected_piece,
    piece_on_cell,
    state.last_postion,
    move,
    state
  )


movements = {
  KING: king_can_move,
  PAWN: pawn_can_move,
  KNIGHT: knight_can_move,
  BISHOP: bishop_can_move,
}
