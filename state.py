from utils import copy
from chess_types import *


class State:
  def __init__(self, board=[], pinned_pieces=[]) -> None:
    self.board = copy(board)
    self.white_turn = True
    self.is_check = False
    self.is_check_mate = False
    self.last_postion : BoardCoord = (-1, -1)
    
    self.move = 0
    self.turn = 1
    
    self.king_checked = []
    self.two_steps_pawn = TwoStepPawn()
    self.pinned_pieces = pinned_pieces.copy()
    self.initial_kings = set([(0, 4), (7, 4)])
    self.initial_rooks = set([(0, 0), (0, 7), (7, 0), (7, 7)])
    

  def copy_board (self, board: Board):
    self.board = copy(board)
    
  def copy_state (self):
    state = State(self.board, self.pinned_pieces)
    state.white_turn = self.white_turn
    state.is_check = self.is_check
    state.is_check_mate = self.is_check_mate
    state.last_postion = self.last_postion
    state.move = self.move
    state.turn = self.turn
    state.king_checked = self.king_checked
    state.two_steps_pawn = self.two_steps_pawn
    state.initial_rooks = self.initial_rooks.copy()
    state.initial_kings = self.initial_kings.copy()
    return state
  
  def next_state (self):
    nxt_state = self.copy_state()
    nxt_state.white_turn = not self.white_turn
    nxt_state.move = self.move + 1
    nxt_state.turn = nxt_state.move // 2 + 1
    
    if nxt_state.two_steps_pawn.count > 0:
      nxt_state.two_steps_pawn.count -= 1
    
    return nxt_state
    
    
class NodeGraph:
  def __init__(self, state: State, prv=None, nxt=None) -> None:
    self.prev : NodeGraph = prv 
    self.state = state
    self.next : NodeGraph = nxt
    

class StateGraph:
  def __init__(self) -> None:
    self.curr_node = None 

  def __len__(self) -> bool:
    return self.curr_node is not None
  
  def add(self, state: State):
    new_state = state.copy_state()
    if self.curr_node is None:
      self.curr_node = NodeGraph(new_state)
      return

    new_state.white_turn = not new_state.white_turn
    self.curr_node.next = NodeGraph(new_state, prv=self.curr_node)
    self.curr_node = self.curr_node.next
  
  def back(self) -> State:
    if self.curr_node.prev is not None:
      self.curr_node = self.curr_node.prev
    return self.curr_node.state.copy_state()
  
  def next(self) -> State:
    self.curr_node = self.curr_node.next
    return self.curr_node.state.copy_state()
    
  def is_last(self) -> bool:
    if self.curr_node is None:
      return True
    return self.curr_node.next is None
    