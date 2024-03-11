# consts
BLACK = (255, 255, 255)
WHITE = (0, 0, 0)

# screen size
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 720
SIZE = SCREEN_HEIGHT, SCREEN_WIDTH

# padding
PADDING_X = 0
PADDING_Y = 0
PADDING = PADDING_X, PADDING_Y

# cell sizes
CELL_HEIGHT = 90
CELL_WIDTH = 90

# piece sizes
PIECE_HEIGHT = 80
PIECE_WIDTH = 80
PIECE_SIZE = PIECE_HEIGHT, PIECE_WIDTH

# board sizes
BOARD_HEIGHT = 8
BOARD_WIDTH = 8
TOTAL_CELLS = BOARD_HEIGHT * BOARD_WIDTH

VOID    = 0
KING    = 1
QUEEN   = 2
ROOK    = 3
BISHOP  = 4
KNIGHT  = 5
PAWN    = 6

VOID_STR    = ''
KING_STR    = 'king'
QUEEN_STR   = 'queen'
ROOK_STR    = 'rook'
BISHOP_STR  = 'bishop'
KNIGHT_STR  = 'knight'
PAWN_STR    = 'pawn'

piece_to_name = [
  VOID_STR,     # 0
  KING_STR,     # 1
  QUEEN_STR,    # 2
  ROOK_STR,     # 3
  BISHOP_STR,   # 4
  KNIGHT_STR,   # 5
  PAWN_STR      # 6
]

values_of_pieces = {
  KING_STR:   0,
  QUEEN_STR:  9,
  ROOK_STR:   5,
  BISHOP_STR: 3,
  KNIGHT_STR: 3,
  PAWN_STR:   1
}
