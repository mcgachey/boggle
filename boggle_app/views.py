# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import traceback

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from boggle_solver import BoggleBoard, BoggleSolver
from word_list import en_us

def index(request):
    context = {
        'board_width': range(0, 4)
    }
    return render(request, 'boggle_app/index.html', context)


# Skip CSRF checking so so simplify automatic testing using a REST client
@csrf_exempt
def solve(request):
    try:
        letters = json.loads(request.body)
        board = BoggleBoard(letters)
        solver = BoggleSolver(board, en_us)
        matches = solver.find_words()
        return JsonResponse(
            matches, safe=False, status=200
        )
    except ValueError as e:
        traceback.print_exc()
        return HttpResponse(e.message, status=400)
    except Exception:
        traceback.print_exc()
        return HttpResponse("Server error", status=500)
