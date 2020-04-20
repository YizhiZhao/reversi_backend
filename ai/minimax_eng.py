from copy import deepcopy
import math
from .evaluator import Evaluator

class MinimaxEngine():

    def __init__(self):
        # maximun depth of searching tree.
        self.max_depth = 4
        self.step_count = 0
        self.history_interval = {}
        self.evaluator = Evaluator()

    def get_move(self, board):
        """ Return a move for the given color that maximizes the difference in
        number of pieces for that color. """
        color = 1
        interval = [-math.inf, math.inf]
        if board.count(color) + board.count(-1 * color) < 6:
            self.step_count = 0
        self.step_count += 2 
        if self.step_count < 45:
            _, move = self._max(board, color, 0, *interval)
        else:
            _, move = self._max(board, color, -2, *interval)
        return move

    def _max(self, board, color, depth, alpha, beta):
        moves = board.get_legal_moves(color)
        
        final_move = None
        if self.evaluator.is_terminal(board, color, my_moves=moves):
            return Evaluator.evaluate(board, color, step_count=depth + self.step_count, is_terminal=True), final_move
        elif depth >= self.max_depth:
            return Evaluator.evaluate(board, color, step_count=depth + self.step_count, is_terminal=False), final_move
        if len(moves) == 0:
            return self._min(board, color, depth, alpha, beta)
        v = -math.inf
        for move in moves:
            new_board = deepcopy(board)
            new_board.execute_move(move, color)
            w, _ = self._min(new_board, color, depth + 1, alpha, beta)
            if w > v:
                v = w
                final_move = move
            if v >= beta:
                return v, final_move
            alpha = max(alpha, v)
        return v, final_move

    def _min(self, board, color, depth, alpha, beta):
        op_color = -1 * color
        op_moves = board.get_legal_moves(op_color)
        final_move = None
        if self.evaluator.is_terminal(board, color, op_moves=op_moves):
            return Evaluator.evaluate(board, color, step_count=depth + self.step_count, is_terminal=True), final_move
        elif depth >= self.max_depth:
            return Evaluator.evaluate(board, color, step_count=depth + self.step_count, is_terminal=False), final_move
        if len(op_moves) == 0:
            return self._max(board, color, depth, alpha, beta)
        v = math.inf
        for move in op_moves:
            new_board = deepcopy(board)
            new_board.execute_move(move, op_color)
            w, _ = self._max(new_board, color, depth + 1, alpha, beta)
            if w < v:
                v = w
                final_move = move
            if v <= alpha:
                return v, final_move
            beta = min(beta, v)
        return v, final_move
