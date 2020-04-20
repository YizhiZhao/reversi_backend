from copy import deepcopy
import os
import random
import numpy as np
import math
import sys
from .evaluator import Evaluator

class TreeNode():

    def __init__(self, board, color, parent):
        self.board = board
        self.color = color
        self.is_terminal = Evaluator.is_terminal(board, color)
        self.is_fully_expanded  =   self.is_terminal
        self.parent             =   parent
        self.visit_num          =   0
        self.total_reward       =   0
        self.children           =   {}
        self.v                  =   Evaluator.evaluate(board, color, 0, False)


class MCTSEngine():
    """ Game engine that implements MCTS Algo. """

    def __init__(self):
        self.iter_limit = 200
        self.exploration_constant = 1 / math.sqrt(1.5)

    def get_move(self, board):
        """ Return a move for the given color using MCTS algo """
        new_board = deepcopy(board)
        return self.search(new_board, 1)

    def search(self, board, color):
        self.root = TreeNode(board, color, None)
        self.color = color

        for i in range(self.iter_limit):
            node = self.treePolicy(self.root)
            reward = node.v

            self.backup(node, reward)

        best_child = self.bestChild(self.root)
        return self.getAction(self.root, best_child)

    # return leaf node
    def treePolicy(self, node):
        while not node.is_terminal:
            if node.is_fully_expanded:
                node = self.bestChild(node)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        possible_actions = node.board.get_legal_moves(node.color)
        best_value = float("-inf")
        times = 0

        # chose best unexpanded child 
        for action in possible_actions:
            # if action is in untried actions
            if action not in node.children.keys():
                times = times + 1
                new_board = deepcopy(node.board)
                new_board.execute_move(action, node.color)
                v = Evaluator.evaluate(new_board, node.color, 0, False)
                if v > best_value:
                    best_value = v
                    best_child = TreeNode(new_board, -1 * node.color, node)
                    best_action = action
        
        node.children[best_action] = best_child
        if len(possible_actions) == len(node.children):
            node.is_fully_expanded = True
        return best_child    

    def backup(self, node, reward):
        while node is not None:
            node.visit_num += 1
            node.total_reward += reward
            node = node.parent

    def bestChild(self, node):
        best_value = float("-inf")
        best_nodes = []
        
        for action in node.children.keys():
            child = node.children[action]
            value = child.total_reward / child.visit_num + child.v * math.sqrt(node.visit_num) / (1 + child.visit_num)
            value = node.color * value
            if value > best_value:
                best_value = value
                best_nodes = [child]
            elif value >= best_value * 0.85:
                best_nodes.append(child)
        return random.choice(best_nodes)

    def getAction(self, root, best_child):
        for action, node in root.children.items():
            if node is best_child:
                return action
