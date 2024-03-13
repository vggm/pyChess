import sys
import pygame as pg
from state import State, StateGraph
from utils import *
from sprites import *
from movement import Movement


def main():
  pg.init()
  pg.display.set_caption('PyChess!')

  clock = pg.time.Clock()
  window = pg.display.set_mode(SIZE, vsync=1)

  restart = True
  while restart:
    restart = False

    # this will be the matrix of the game
    gameBoard = [[0 for _ in range(BOARD_HEIGHT)] for _ in range(BOARD_WIDTH)]
    last_move = 0

    stateGraph = StateGraph()
    initialize_board(gameBoard)
    
    movement_checker = Movement()

    curr_state = State(gameBoard)
    stateGraph.add(curr_state)

    # background image
    bg = pg.image.load('img/board.png')
    bg = pg.transform.scale(bg, (720, 720))

    caught_piece = False
    selected_piece = None
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
            if stateGraph:
              curr_state = stateGraph.back()
          elif event.key == pg.K_RIGHT:
            if not stateGraph.is_last():
              curr_state = stateGraph.next()

      mouse_x, mouse_y = pg.mouse.get_pos()
      
      if caught_piece and pg.mouse.get_pressed()[2]: # drop piece
        caught_piece = False
        i, j = curr_state.last_postion
        curr_state.board[i][j] = selected_piece
      
      if caught_piece and not pg.mouse.get_pressed()[0]: # drop piece
        caught_piece = False
        can_move = False
        i, j = real_to_board((mouse_x, mouse_y))
        if mouse_in_board((mouse_x, mouse_y)) and movement_checker.legal_move(selected_piece, (i, j), curr_state):
          
          if movement_checker.can_castle():
            movement_checker.castle_move()
            can_move = True
          else:
            can_move = movement_checker.can_move_switch()
            if can_move:
              curr_state.board[i][j] = selected_piece
             
          if can_move:
            stateGraph.add(curr_state)
            curr_state = curr_state.next_state()
        
        if not can_move:
          i, j = curr_state.last_postion
          curr_state.board[i][j] = selected_piece
        
        
      elif not caught_piece and pg.mouse.get_pressed()[0]: # select piece
        if mouse_in_board((mouse_x, mouse_y)) and is_a_piece((mouse_x, mouse_y), curr_state.board):
          i, j = real_to_board((mouse_x, mouse_y))
          piece = curr_state.board[i][j]
          
          # its a piece and must be the same turn as its color
          # if True: # uncomment to move pieces the other turn
          if curr_state.white_turn == is_white_piece(piece):
            caught_piece = True
            # print('white' if is_white_piece(piece) else 'black')
            # print(piece_name(piece))
            curr_state.board[i][j] = VOID
            curr_state.last_postion = (i, j)
            selected_piece = piece        
        

      window.fill(WHITE)
      window.blit(bg, PADDING)

      if last_move != curr_state.move:
        last_move = curr_state.move
        print_board(curr_state.board)

      # show every piece on the board
      for i, row in enumerate(curr_state.board):
        for j, piece in enumerate(row):
          if piece_name(piece) == VOID_STR:
            continue
          window.blit(get_sprite_from_piece(piece), board_to_real((i, j)))

      # show the caughtPiece above the rest of the pieces
      if caught_piece:
        window.blit(get_sprite_from_piece(selected_piece), (mouse_x - PIECE_WIDTH / 2, mouse_y - PIECE_HEIGHT / 2))

      pg.display.flip()
      clock.tick(60)
    # main loop


if __name__ == "__main__":
  main()
  pg.quit()
  sys.exit()
