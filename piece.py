from utils import *
from chess_types import *
from constants import *


class TestPiece:
  def __init__(self, piece: Piece) -> None:
    self.piece = piece
    self.name = piece_name(piece)
    self.is_white = is_white_piece(piece)


class CaughtPiece(object):
  def __init__(self, piece: Piece, boardCoord: BoardCoord) -> None:
    # Coords to draw
    self.real_coord = board_to_real(boardCoord)

    # Coords on the board
    self.board_coord = real_to_board(self.real_coord)

    self.name = piece_to_name[piece]
    self.value = values_of_pieces[self.name]

    self.is_white = is_white_piece(piece)
    self.is_king = is_king_piece(piece)

  def move(self, board_coord: BoardCoord):
    self.board_coord = board_coord

  def draw(self, real_coord: RealCoord):
    self.real_coord = real_coord

  def canMove(self, movement, board):
    return True


class King(CaughtPiece):
  def __init__(self, coord, isWhite):
    super().__init__(coord, isWhite, True)
    self.originalPosition = True

  def move(self, x, y):
    self.x = x
    self.y = y
    self.originalPosition = False

  def canMove(self, movement, board):
    distance = abs(self.x - movement[0]) <= 1 and abs(self.y - movement[1]) <= 1

    if distance > 1 and not can_castle(self, movement, board):
      return False

    return True


class Queen(CaughtPiece):
  def canMove(self, movement, board):
    return rookMove(self, movement, board) or bishopMove(self, movement, board)


class Rook(CaughtPiece):
  def __init__(self, coord, isWhite):
    super().__init__(coord, isWhite)
    self.originalPosition = True

  def move(self, x, y):
    self.x = x
    self.y = y
    self.originalPosition = False

  def canMove(self, movement, board):
    return rookMove(self, movement, board)


class Knight(CaughtPiece):
  def canMove(self, movement, board):
    return (abs(self.x - movement[0]) == 2 and abs(self.y - movement[1]) == 1) or \
      (abs(self.x - movement[0]) == 1 and abs(self.y - movement[1]) == 2)


class Bishop(CaughtPiece):
  def canMove(self, movement, board):
    return bishopMove(self, movement, board)


class Pawn(CaughtPiece):
  def __init__(self, coord, isWhite):
    super().__init__(coord, isWhite)
    self.originalPosition = True
    self.moved2cells = False

  def move(self, x, y):
    if not self.originalPosition and self.moved2cells:
      self.moved2cells = False

    if abs(self.y - y) == 2:
      self.moved2cells = True

    self.x = x
    self.y = y
    self.originalPosition = False

  def canAttack(self, movement, board):

    # If there is a enemy piece in the diagonal of the pawn, can attack
    if self.isWhite:
      try:
        if board[self.y - 1][self.x - 1] != None and not board[self.y - 1][self.x - 1].isWhite and \
            (movement[0] == (self.x - 1) and movement[1] == (self.y - 1)):
          return True
      except Exception:
        pass

      try:
        if board[self.y - 1][self.x + 1] != None and not board[self.y - 1][self.x + 1].isWhite and \
            (movement[0] == (self.x + 1) and movement[1] == (self.y - 1)):
          return True
      except Exception:
        pass

    else:
      try:
        if board[self.y + 1][self.x - 1] != None and board[self.y + 1][self.x - 1].isWhite and \
            (movement[0] == (self.x - 1) and movement[1] == (self.y + 1)):
          return True
      except Exception:
        pass

      try:
        if board[self.y + 1][self.x + 1] != None and board[self.y + 1][self.x + 1].isWhite and \
            (movement[0] == (self.x + 1) and movement[1] == (self.y + 1)):
          return True
      except Exception:
        pass

    return False

  def canPassant(self, movement, board):

    # En passant
    if self.isWhite:
      try:
        if board[self.y][self.x - 1] != None and not board[self.y][self.x - 1].isWhite and \
            board[self.y][self.x - 1].name == "Pawn" and board[self.y][self.x - 1].moved2cells and \
            (movement[0] == (self.x - 1) and movement[1] == (self.y - 1)):
          return True
      except Exception:
        pass

      try:
        if board[self.y][self.x + 1] != None and not board[self.y][self.x + 1].isWhite and \
            board[self.y][self.x + 1].name == "Pawn" and board[self.y][self.x + 1].moved2cells and \
            (movement[0] == (self.x + 1) and movement[1] == (self.y - 1)):
          return True
      except Exception:
        pass
    else:
      try:
        if board[self.y][self.x - 1] != None and board[self.y][self.x - 1].isWhite and \
            board[self.y][self.x - 1].name == "Pawn" and board[self.y][self.x - 1].moved2cells and \
            (movement[0] == (self.x - 1) and movement[1] == (self.y + 1)):
          return True
      except Exception:
        pass

      try:
        if board[self.y][self.x + 1] != None and board[self.y][self.x + 1].isWhite and \
            board[self.y][self.x + 1].name == "Pawn" and board[self.y][self.x + 1].moved2cells and \
            (movement[0] == (self.x + 1) and movement[1] == (self.y + 1)):
          return True
      except Exception:
        pass

    return False

  def canMove(self, movement, board):
    distance = abs(self.y - movement[1])

    # If the distance is more than 2
    if distance > 2:
      return False

    # If the movement is in another column, return False
    if movement[0] != self.x and not self.canAttack(movement, board) and not self.canPassant(movement, board):
      return False

      # If the pawn goes back, return False
    if self.isWhite:
      if movement[1] > self.y: return False
    else:
      if movement[1] < self.y: return False

    # If the distance is 2 and the pawn has been moved, return False
    if distance == 2 and not self.originalPosition:
      return False

    # If there is a piece between the cells, return False
    if distance == 2:
      if self.isWhite and board[self.y - 1][self.x] != None:
        return False

      if not self.isWhite and board[self.y + 1][self.x] != None:
        return False

    return True





# Returns True if the last move was a Passant
def is_passant(piece, lastPosition, board):
  if lastPosition[1] != piece.y and piece.name == "Pawn":
    if piece.isWhite:
      return board[piece.y + 1][piece.x] != None and not board[piece.y + 1][piece.x].isWhite and \
        board[piece.y + 1][piece.x].name == "Pawn" and board[piece.y + 1][piece.x].moved2cells
    else:
      return board[piece.y - 1][piece.x] != None and board[piece.y - 1][piece.x].isWhite and \
        board[piece.y - 1][piece.x].name == "Pawn" and board[piece.y - 1][piece.x].moved2cells

  return False


def can_castle(king, movement, board):
  if not king.isKing:
    return False

  if board[movement[1]][movement[0]].name == "Rook":
    rook = board[movement[1]][movement[0]]
    if king.originalPosition and rook.originalPosition:
      return rookMove(king, movement, board)

  return False


def castle(king, rook, board):
  if abs(king.x - rook.x) == 3:
    king.x = 6
    rook.x = 5

    board[king.y][7] = None
    board[king.y][4] = None

    board[king.y][6] = king
    board[king.y][5] = rook

    x, y = board_to_real(king.x, king.y)
    king.drawX = x
    king.drawY = y

    x, y = board_to_real(rook.x, rook.y)
    rook.drawX = x
    rook.drawY = y
  else:
    king.x = 2
    rook.x = 3

    board[king.y][0] = None
    board[king.y][4] = None

    board[king.y][2] = king
    board[king.y][3] = rook

    x, y = board_to_real(king.x, king.y)
    king.drawX = x
    king.drawY = y

    x, y = board_to_real(rook.x, rook.y)
    rook.drawX = x
    rook.drawY = y


def bishopMove(piece, movement, board):
  org = [piece.x, piece.y]

  if abs(piece.x - movement[0]) != abs(piece.y - movement[1]):
    return False

  index = [1, 1]

  if piece.x > movement[0]:
    index[0] *= -1

  if piece.y > movement[1]:
    index[1] *= -1

  org[0] += index[0]
  org[1] += index[1]
  while org[0] != movement[0] and org[1] != movement[1]:

    if board[org[1]][org[0]] != None:
      return False

    org[0] += index[0]
    org[1] += index[1]

  return True


# If there isnt pieces between piece and the move, returns True
def rookMove(piece, movement, board):
  if movement[0] != piece.x and movement[1] != piece.y:
    return False

  index = 1

  if piece.x != movement[0]:
    org = piece.x

    if piece.x > movement[0]:
      index *= -1

    org += index
    while org != movement[0]:
      if board[piece.y][org] != None:
        return False
      org += index
  else:
    org = piece.y

    if piece.y > movement[1]:
      index *= -1

    org += index
    while org != movement[1]:
      if board[org][piece.x] != None:
        return False
      org += index

  return True


def legal_move(piece, coord, state):
  board = state.board

  if state.white_turn and not piece.isWhite or not state.white_turn and piece.isWhite:
    return False

  # If the cursor is out of the board return False
  if coord[0] >= BOARD_WIDTH or coord[0] < 0 or coord[1] >= BOARD_HEIGHT or coord[1] < 0:
    return False

  # Same cell
  if coord[0] == piece.x and coord[1] == piece.y:
    return False

  if not piece.canMove(coord, board):
    return False

  # If the piece of that cell is the same color than the caught one, return False
  if board[coord[1]][coord[0]] != None and board[coord[1]][coord[0]].isWhite == piece.isWhite and not can_castle(piece,
                                                                                                                 coord,
                                                                                                                 board):
    return False

  return True
