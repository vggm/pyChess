from utils import *

values = {'King': 0,
          'Queen': 9,
          'Rook': 5,
          'Bishop': 3,
          'Knight': 3,
          'Pawn': 1}

class Piece(object):
    def __init__(self, coord, isWhite, isKing = False) -> None:
        
        # Coords to draw
        self.drawX = coord[0]
        self.drawY = coord[1]
        
        # Coords on the board
        self.x = realToCoord(self.drawX, self.drawY)[0]
        self.y = realToCoord(self.drawX, self.drawY)[1]
        
        self.name = type(self).__name__
        self.value = values[self.name]
        
        self.isWhite = isWhite
        self.isKing = isKing
    
    def move(self,x,y):
        self.x = x
        self.y = y
        
    def draw(self,x,y):
        self.drawX = x
        self.drawY = y
    
    def canMove(self,movement,board):
        return True


class King(Piece):
    def canMove(self, movement, board):
        return abs(self.x - movement[0]) <= 1 and abs(self.y - movement[1]) <= 1


class Queen(Piece):
    pass


class Rook(Piece):
    def canMove(self, movement, board):
        
        if movement[0] != self.x and movement[1] != self.y:
            return False
        
        return rookMove(self,movement,board)
            


class Knight(Piece):
    def canMove(self, movement, board):
        return (abs(self.x - movement[0]) == 2 and abs(self.y - movement[1]) == 1) or \
             (abs(self.x - movement[0]) == 1 and abs(self.y - movement[1]) == 2)


class Bishop(Piece):
    pass


class Pawn(Piece):
    def __init__(self, coord, isWhite):
        super().__init__(coord, isWhite)
        self.originalPosition = True
        self.moved2cells = False
    
    def move(self,x,y):
        if not self.originalPosition and self.moved2cells:
            self.moved2cells = False
        
        if abs(self.y - y) == 2:
            self.moved2cells = True
            
        self.x = x
        self.y = y
        self.originalPosition = False
        
    def canAttack(self,movement,board):
        
        # If there is a enemy piece in the diagonal of the pawn, can attack
        if self.isWhite:
            try:
                if board[self.y-1][self.x-1] != None and not board[self.y-1][self.x-1].isWhite and \
                    (movement[0] == (self.x - 1) and movement[1] == (self.y - 1)):
                        return True
            except Exception:
                pass
            
            try:
                if board[self.y-1][self.x+1] != None and not board[self.y-1][self.x+1].isWhite and \
                    (movement[0] == (self.x + 1) and movement[1] == (self.y - 1)):
                        return True
            except Exception:
                pass
        
        else:
            try:
                if board[self.y+1][self.x-1] != None and board[self.y+1][self.x-1].isWhite and \
                    (movement[0] == (self.x - 1) and movement[1] == (self.y + 1)):
                        return True
            except Exception:
                pass
            
            try:    
                if board[self.y+1][self.x+1] != None and board[self.y+1][self.x+1].isWhite and \
                    (movement[0] == (self.x + 1) and movement[1] == (self.y + 1)):
                        return True
            except Exception:
                pass
            
        return False
    
    def canPassant(self,movement,board):
        
        # En passant
        if self.isWhite:
            try:
                if board[self.y][self.x-1] != None and not board[self.y][self.x-1].isWhite and \
                    board[self.y][self.x-1].name == "Pawn" and board[self.y][self.x-1].moved2cells and \
                    (movement[0] == (self.x - 1) and movement[1] == (self.y - 1)):
                        return True
            except Exception:
                pass
                    
            try:
                if board[self.y][self.x+1] != None and not board[self.y][self.x+1].isWhite and \
                    board[self.y][self.x+1].name == "Pawn" and board[self.y][self.x+1].moved2cells and \
                    (movement[0] == (self.x + 1) and movement[1] == (self.y - 1)):
                        return True
            except Exception:
                pass
        else:
            try:
                if board[self.y][self.x-1] != None and board[self.y][self.x-1].isWhite and \
                    board[self.y][self.x-1].name == "Pawn" and board[self.y][self.x-1].moved2cells and \
                    (movement[0] == (self.x - 1) and movement[1] == (self.y + 1)):
                        return True
            except Exception:
                pass
            
            try:        
                if board[self.y][self.x+1] != None and board[self.y][self.x+1].isWhite and \
                    board[self.y][self.x+1].name == "Pawn" and board[self.y][self.x+1].moved2cells and \
                    (movement[0] == (self.x + 1) and movement[1] == (self.y + 1)):
                        return True
            except Exception:
                pass
            
        return False
        
    def canMove(self,movement,board):
        distance = abs(self.y - movement[1])
        
        # If the distance is more than 2
        if distance > 2: 
            return False
        
        # If the movement is in another column, return False
        if movement[0] != self.x and not self.canAttack(movement,board) and not self.canPassant(movement,board):
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
            if self.isWhite and board[self.y-1][self.x] != None:
                return False
            
            if not self.isWhite and board[self.y+1][self.x] != None:
                return False
            
        return True


def isPiece(x,y,board):
    coord = realToCoord(x,y)
    return board[coord[1]][coord[0]] != None

# Returns True if the last move was a Passant
def isPassant(piece,lastPosition,board):
    if lastPosition[1] != piece.y and piece.name == "Pawn":
        if piece.isWhite:
            return board[piece.y+1][piece.x] != None and not board[piece.y+1][piece.x].isWhite and \
                board[piece.y+1][piece.x].name == "Pawn" and board[piece.y+1][piece.x].moved2cells
        else:
            return board[piece.y-1][piece.x] != None and board[piece.y-1][piece.x].isWhite and \
                board[piece.y-1][piece.x].name == "Pawn" and board[piece.y-1][piece.x].moved2cells
    
    return False
    
# If there isnt pieces between piece and the move, returns True
def rookMove(piece,movement,board):
    if piece.x != movement[0]:
        dst,org = greaterLower(movement[0],piece.x)
        
        while org < dst:
            if board[piece.y][org] != None and org != piece.x:
                return False
            org += 1
    else:
        dst,org = greaterLower(movement[1],piece.y)
        
        while org < dst:
            if board[org][piece.x] != None and org != piece.y:
                return False
            org += 1
            
    return True
            
    
def legalMove(piece,coord,board):
    
    # If the cursor is out of the board return False
    if coord[0] >= BOARD_WIDHT or coord[0] < 0 or coord[1] >= BOARD_HEIGHT or coord[1] < 0:
        return False
    
    # Same cell
    if coord[0] == piece.x and coord[1] == piece.y:
        return False
    
    if not piece.canMove(coord,board):
        return False
    
    # If the piece of that cell is the same color than the caught one, return False
    if board[coord[1]][coord[0]] != None and board[coord[1]][coord[0]].isWhite == piece.isWhite: 
        return False
    
    return True
  