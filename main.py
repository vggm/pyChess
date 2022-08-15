import pickle
import sys
import pygame as pg
from utils import *
from piece import *


# this will be the matrix of the game
board = []
lastPosition = []
###########


def copy(x):
    return pickle.loads(pickle.dumps(x))


def main():
    global board
    global lastPosition
    
    pg.init()
    pg.display.set_caption('PyChess!')
    
    clock = pg.time.Clock()
    window = pg.display.set_mode(SIZE,vsync=1)
    
    restart = True
    while restart:
        restart = False
        
        stackOfBoards = []
        board = [ [ None for i in range(BOARD_HEIGHT) ] for j in range(BOARD_WIDHT) ]
        
        # set white pieces
        board[7][0] = Rook(coordToReal(0,7),True)
        board[7][7] = Rook(coordToReal(7,7),True)
        board[7][1] = Knight(coordToReal(1,7),True)
        board[7][6] = Knight(coordToReal(6,7),True)
        board[7][2] = Bishop(coordToReal(2,7),True)
        board[7][5] = Bishop(coordToReal(5,7),True)
        board[7][3] = Queen(coordToReal(3,7),True)
        board[7][4] = King(coordToReal(4,7),True)
        for i in range(BOARD_WIDHT):
            board[6][i] = Pawn(coordToReal(i,6),True)
            
        # set black pieces
        board[0][7] = Rook(coordToReal(7,0),False)
        board[0][0] = Rook(coordToReal(0,0),False)
        board[0][1] = Knight(coordToReal(1,0),False)
        board[0][6] = Knight(coordToReal(6,0),False)
        board[0][2] = Bishop(coordToReal(2,0),False)
        board[0][5] = Bishop(coordToReal(5,0),False)
        board[0][3] = Queen(coordToReal(3,0),False)
        board[0][4] = King(coordToReal(4,0),False)
        for i in range(BOARD_WIDHT):
            board[1][i] = Pawn(coordToReal(i,1),False)
        
        # background image
        bg = pg.image.load('img/board.png')
        bg = pg.transform.scale(bg, (720,720))
            
        pieceCaught = None
        end = False
        while not end:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    end = True
                elif event.type == pg.KEYDOWN: 
                    if event.key == pg.K_ESCAPE:
                        end = True
                    elif event.key == pg.K_r:
                        restart = True
                        end = True
                    elif event.key == pg.K_LEFT:
                        if len(stackOfBoards) != 0:
                            board = stackOfBoards.pop()
                
        
            mouseX, mouseY = pg.mouse.get_pos()
            
            
            # if there is a piece caught, it fly over the board whenever the cursor goes
            # if there isnt a piece caught and the left bottom of the mouse if pressed over
            #   a piece, that piece is now caught 
            
            if pieceCaught != None:
                pieceCaught.draw(mouseX-PIECE_WIDTH/2,mouseY-PIECE_HEIGHT/2)
            elif pg.mouse.get_pressed()[0]:
                if isPiece(mouseX,mouseY,board):
                    stackOfBoards.append(copy(board))
                    x,y = realToCoord(mouseX,mouseY)
                    pieceCaught = board[y][x]
                    pieceCaught.draw(mouseX,mouseY)
                    lastPosition = [x,y]
                    
                    
            # if the player drop the piece:
            #   if it is a legalMove, the piece will move
            #   if it isnt a legalMove, the piece will not move
            
            if pieceCaught != None and not pg.mouse.get_pressed()[0]:
                col,row = realToCoord(mouseX,mouseY)
                
                if legalMove(pieceCaught,(col,row),board):
                    x,y = coordToReal(col,row)
                    pieceCaught.move(col,row)
                    pieceCaught.draw(x,y)
                    
                    if isPassant(pieceCaught,lastPosition,board):
                        if pieceCaught.isWhite:
                            board[pieceCaught.y+1][pieceCaught.x] = None
                        else:
                            board[pieceCaught.y-1][pieceCaught.x] = None
                    
                    board[lastPosition[1]][lastPosition[0]] = None
                    board[row][col] = pieceCaught
                    
                    pieceCaught = None
                else:
                    stackOfBoards.pop()
                    
                    x,y = coordToReal(lastPosition[0],lastPosition[1])
                    pieceCaught.draw(x,y)                    
                    pieceCaught = None

    
            window.fill(WHITE)
            window.blit(bg,PADDING)
            
            # show every piece on the board
            for col in board:
                for piece in col:
                    if piece != None:
                        window.blit(getSprite(piece.name,piece.isWhite),(piece.drawX,piece.drawY))
            
            # show the cuaghtPiece above the rest of the pieces
            if pieceCaught != None:
                window.blit(getSprite(pieceCaught.name,pieceCaught.isWhite),(pieceCaught.drawX,pieceCaught.drawY))
                
            pg.display.flip() 
            clock.tick(60)  
            

if __name__ == "__main__":
    main()
    pg.quit()
    sys.exit()
    