import pygame as pg
from constants import *
from chess_types import Piece
from utils import is_white_piece, piece_name


def get_image(url):
  img = pg.image.load(url)
  return pg.transform.smoothscale(img, PIECE_SIZE)

# sync the image of the piece with its name
white_sprites = {
  KING_STR   : get_image('img/white/king.png'),
  QUEEN_STR  : get_image('img/white/queen.png'),
  ROOK_STR   : get_image('img/white/rook.png'),
  BISHOP_STR : get_image('img/white/bishop.png'),
  KNIGHT_STR : get_image('img/white/knight.png'),
  PAWN_STR   : get_image('img/white/pawn.png')
}

black_sprites = {
  KING_STR   : get_image('img/black/king.png'),
  QUEEN_STR  : get_image('img/black/queen.png'),
  ROOK_STR   : get_image('img/black/rook.png'),
  BISHOP_STR : get_image('img/black/bishop.png'),
  KNIGHT_STR : get_image('img/black/knight.png'),
  PAWN_STR   : get_image('img/black/pawn.png')
}

def get_sprite(name: str, is_white: bool) -> pg.Surface:
  return white_sprites[name] if is_white else black_sprites[name]
  
def get_sprite_from_piece(piece: Piece) -> pg.Surface:
  name = piece_name(piece)
  is_white = is_white_piece(piece)
  return get_sprite(name, is_white)
  