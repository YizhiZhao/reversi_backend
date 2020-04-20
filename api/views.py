import json, datetime
from django.shortcuts import render
from django.utils import timezone
from .models import UserAcl, UserHistory
from lib.common import generate_response

def login(request):
    raw_data = json.loads(request.body)
    name, password = raw_data['name'], raw_data['password']
    user_candidates = UserAcl.objects.filter(name=name)
    if len(user_candidates) == 0:
        new_user = UserAcl(name=name, password=password)
        new_user.save()
        data = {'result': True, 'desc': 'Create new user'}
    else:
        user = user_candidates[0]
        if user.password != password:
            data = {'result': False, 'desc': 'Wrong password!'}
        else:
            data = {'result': True }

    return generate_response(data)

def exit(request):
    raw_data = json.loads(request.body)
    raw_name, raw_status, raw_board = raw_data['name'], raw_data['status'], raw_data['board']
    name = UserAcl.objects.get(name=raw_name)
    status = raw_status if raw_status else ''
    board = json.dumps(raw_board)

    new_history = UserHistory(name=name, status=status, board=board, endtime=timezone.now())
    new_history.save()
    data = {'id': new_history.id}
    
    return generate_response(data)

def userdata(request):
    raw_data = json.loads(request.body)

    user_name = raw_data['username']
    result = []
    user_history = UserHistory.objects.filter(name=user_name)
    for record in user_history:
        raw_endtime = record.endtime
        end_time = raw_endtime.strftime('%Y-%m-%d %H:%M:%S')
        
        raw_status = record.status
        if raw_status == '':
            status = 'unfinished'
        else:
            status = raw_status + ' wins'

        raw_board_info = record.board
        board_list = json.loads(raw_board_info)
        board_info = 'cat number: %d v.s AI number %d' % (board_list.count('cat'), board_list.count('ai'))

        result.append({
            'time': end_time,
            'status': status,
            'boardinfo': board_info,
        })

    data = {'result': result}
    return generate_response(data)