import pygame as pg

# consts
BLACK = (255, 255, 255)
WHITE = (0, 0, 0)

# screen size
SCREEN_HEIGHT = 720
SCREEN_WIDTH  = 720
SIZE = SCREEN_HEIGHT, SCREEN_WIDTH

# padding
PADDING_X = 0
PADDING_Y = 0
PADDING = PADDING_X, PADDING_Y

# cell sizes
CELL_HEIGHT = 90
CELL_WIDTH  = 90

# piece sizes
PIECE_HEIGHT = 80
PIECE_WIDTH  = 80
PIECE_SIZE = PIECE_HEIGHT, PIECE_WIDTH

# board sizes
BOARD_HEIGHT = 8
BOARD_WIDHT  = 8
TOTAL_CELLS = BOARD_HEIGHT * BOARD_WIDHT


def getImage(url):
    img = pg.image.load(url)
    return pg.transform.smoothscale(img,PIECE_SIZE)


# sync the image of the piece with its name

whiteSprites = {'King':getImage('img/white/king.png'),
                'Queen':getImage('img/white/queen.png'),
                'Rook':getImage('img/white/rook.png'),
                'Bishop':getImage('img/white/bishop.png'),
                'Knight':getImage('img/white/knight.png'),
                'Pawn':getImage('img/white/pawn.png')}

blackSprites = {'King':getImage('img/black/king.png'),
                'Queen':getImage('img/black/queen.png'),
                'Rook':getImage('img/black/rook.png'),
                'Bishop':getImage('img/black/bishop.png'),
                'Knight':getImage('img/black/knight.png'),
                'Pawn':getImage('img/black/pawn.png')}


def getSprite(name, isWhite):
    if isWhite:
        return whiteSprites[name]
    else:
        return blackSprites[name]
    
# 0 <= x,y <= 8
def coordToReal(x,y):
    return 5+(SCREEN_WIDTH/8)*x, 5+(SCREEN_HEIGHT/8)*y

# 0 <= x,y <= SCREEN_WIDTH,SCREEN_HEIGHT
def realToCoord(x,y):
    return int(x//CELL_HEIGHT), int(y//CELL_WIDTH)

# Returns a tuple where [0] is the greater and [1] the lesser
def greaterLower(x,y):
    if x > y: return x,y
    else: return y,x