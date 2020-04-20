import json
from django.shortcuts import render
from django.http import HttpResponse
from .minimax_eng import MinimaxEngine
from .mcts_eng import MCTSEngine
from .board import Board
from lib.common import generate_response

minimax = MinimaxEngine()
mcts = MCTSEngine()

def nextmove(request):
    requestJson = json.loads(request.body)
    rawBoard = requestJson['board']
    curBoard = Board(rawBoard)
    engineName = requestJson['engine']
    if engineName == 'minimax':
        nextMove = minimax.get_move(curBoard)
    elif engineName == 'mcts':
        nextMove = mcts.get_move(curBoard)
    else:
        data = {'result': False, 'desc': 'Wrong AI engine name'}
        return generate_response(data)

    if nextMove:
        data = {'result': True, 'nextmove': nextMove[0]*8 + nextMove[1]}
    else:
        data = {'result': True, 'nextmove': None}

    response = generate_response(data)
    return response
