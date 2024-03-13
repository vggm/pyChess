from types import *
from constants import *
from utils import *
from state import State


class Movement:
  
  def __init__(self) -> None:
    self.movements = {
      KING: self.king_can_move,
      QUEEN: self.queen_can_move,
      PAWN: self.pawn_can_move,
      KNIGHT: self.knight_can_move,
      BISHOP: self.bishop_can_move,
      ROOK: self.rook_can_move
    }
    
    self.can_catle_temp : bool
    
    self.selected_piece : Piece
    self.piece_on_cell : Piece
    
    self.start : BoardCoord
    self.end : BoardCoord
    
    self.state : State

  def set_parameters(self, selected_piece: Piece, move: BoardCoord, state: State):
    self.can_castle_temp = False
    
    self.selected_piece : Piece = selected_piece
    self.piece_on_cell : Piece = piece_from_coord(move, state.board)
    
    self.start : BoardCoord = state.last_postion
    self.end : BoardCoord = move
    
    self.state : State = state

  def can_move_switch(self) -> bool:
    return self.movements[self.selected_piece%10]()


  def legal_move (
    self,
    selected_piece: Piece, 
    end: BoardCoord, 
    state: State 
    ) -> bool:
    self.set_parameters(selected_piece, end, state)
    white_piece = is_white_piece(selected_piece)

    # same cell
    if self.start == self.end:
      return False
    
    if self.can_castle():
      return True
    
    # same color
    if self.piece_on_cell != VOID \
      and (white_piece and is_white_piece(self.piece_on_cell))\
      or (not white_piece and not is_white_piece(self.piece_on_cell)):
      return False  
    
    return True


  def can_castle(self) -> bool:
    
    if self.can_castle_temp:
      return True
    
    king, rook = self.start, self.end
    board = self.state.board
    
    if self.selected_piece % 10 != KING \
      or piece_from_coord(rook, board) % 10 != ROOK:
      return False
    
    if king not in self.state.initial_kings:
      return False
    
    if rook not in self.state.initial_rooks:
      return False
    
    distance = substract_coords(king, rook)[1]
    
    sig = -1
    if distance < 0:
      distance *= -1
      sig = 1
    
    for i in range(1, distance-1):
      if board[king[0]][king[1] + (i * sig)] != VOID:
        return False
      
    self.can_catle_temp = True
    return True


  def castle_move(self) -> None:
    king, rook = self.start, self.end
    
    if king == (7, 4): # white king
      if rook == (7, 7): # short castle
        self.state.board[7][4] = VOID
        self.state.board[7][7] = VOID
        self.state.board[7][6] = KING
        self.state.board[7][5] = ROOK
      
      else: # long castle
        self.state.board[7][4] = VOID
        self.state.board[7][0] = VOID
        self.state.board[7][1] = VOID
        self.state.board[7][2] = KING
        self.state.board[7][3] = ROOK
    
    else: # black king
      if rook == (0, 7): # shot castle
        self.state.board[0][4] = VOID
        self.state.board[0][7] = VOID
        self.state.board[0][6] = KING + 10
        self.state.board[0][5] = ROOK + 10
      
      else: # long castle
        self.state.board[0][4] = VOID
        self.state.board[0][0] = VOID
        self.state.board[0][1] = VOID
        self.state.board[0][2] = KING + 10
        self.state.board[0][3] = ROOK + 10
    
    self.state.initial_kings.remove(king)
    self.state.initial_rooks.remove(rook)


  def king_can_move(self) -> bool:
    (i, j), (ii, jj) = self.start, self.end
    
    distance = max(abs(i-ii), abs(j-jj))
    return distance == 1 and \
      (self.state.board[ii][jj] == VOID 
        or is_white_piece(self.selected_piece) != is_white_piece(self.piece_on_cell))


  def pawn_can_attack(self) -> bool:
    (i, j), (ii, jj) = self.start, self.end
    
    if self.piece_on_cell == VOID:
      return False
    
    if jj not in [j-1, j+1]:
      return False
    
    if is_white_piece(self.selected_piece):
      if i-1 != ii:
        return False
    else: # black piece
      if i+1 != ii:
        return False
        
    return True


  def pawn_can_move(self) -> bool:
    (i, j), (ii, jj) = self.start, self.end
    
    if self.start in self.state.pinned_pieces:
      return False
    
    # cannot go back
    if is_white_piece(self.selected_piece):
      if ii > i:
        return False
    else:
      if ii < i:
        return False
    
    distance = abs(i-ii)
    # cannot move horizontally unless it can attack
    if j - jj != 0 and not self.pawn_can_attack(): 
      return False
    
    if distance > 2: # cannot move more than two steps
      return False
    
    # only can move two steps at the initial cell
    if distance == 2:
      if self.start not in self.state.initial_pawns:
        return False 
      if is_white_piece(self.selected_piece):
        if piece_from_coord((i-1, j), self.state.board) != VOID:
          return False
      else:
        if piece_from_coord((i+1, j), self.state.board) != VOID:
          return False
    
    # must not be any piece in the cell
    if j == jj and self.piece_on_cell != VOID:
      return False
    
    return True


  def knight_can_move(self) -> bool:
    (i, j), (ii, jj) = self.start, self.end
    
    if self.start in self.state.pinned_pieces:
      return False
    
    if self.piece_on_cell != VOID and same_color(self.selected_piece, self.piece_on_cell):
      return False
    
    return (abs(i - ii) == 2 and abs(j - jj) == 1 
      or abs(j - jj) == 2 and abs(i - ii) == 1)
  
  
  def bishop_can_move(self) -> bool:
    (i, j), (ii, jj) = self.start, self.end
    
    if self.start in self.state.pinned_pieces:
      return False
    
    if self.piece_on_cell != VOID and same_color(self.selected_piece, self.piece_on_cell):
      return False
    
    v_distance = abs(i - ii)
    h_distance = abs(j - jj)
    
    if v_distance != h_distance:
      return False
    
    v = 1 if i < ii else -1
    h = 1 if j < jj else -1
    
    for k in range(1, v_distance):
      if piece_from_coord((i+(k*v), j+(k*h)), self.state.board) != VOID:
        return False                                                  
    
    return True  


  def rook_can_move(self) -> bool:
    (i, j), (ii, jj) = self.start, self.end
    
    if self.start in self.state.pinned_pieces:
      return False
    
    if self.piece_on_cell != VOID and same_color(self.selected_piece, self.piece_on_cell):
      return False
    
    v_distance = abs(i - ii)
    h_distance = abs(j - jj)
    
    # only can move vertically or horizontally, but no both
    if v_distance != 0 and h_distance != 0:
      return False
    
    v = 1 if i < ii else -1
    h = 1 if j < jj else -1
    
    mv, mh = (0, 1) if h_distance > 0 else (1, 0)
    
    for k in range(1, v_distance or h_distance):
      if piece_from_coord((i+(k*v)*mv, j+(k*h)*mh), self.state.board) != VOID:
        return False                                                  
    
    return True          


  def queen_can_move(self) -> bool:
    (i, j), (ii, jj) = self.start, self.end
    
    if self.start in self.state.pinned_pieces:
      return False
    
    if not self.rook_can_move() \
      and not self.bishop_can_move():
      return False
    
    return True                            



