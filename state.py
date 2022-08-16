
class State(object):
    def __init__(self,board) -> None:
        self.board = board
        self.whiteTurn = True
        self.isCheck = False
        self.isCheckMate = False
        self.numOfMoves = 0