
# types
Piece = int
Board = list[list[int]]
RealCoord = tuple[int, int]
BoardCoord = tuple[int, int]

class TwoStepPawn():
  def __init__(self) -> None:
    self.pos = []
    self.count = 0