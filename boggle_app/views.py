# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    context = {
        'board_width': range(0, 4)
    }
    return render(request, 'boggle_app/index.html', context)


# Skip CSRF checking so so simplify automatic testing using a REST client
@csrf_exempt
def solve(request):
    # try:
    #     raise ValueError
    # except ValueError as e:
    #     return HttpResponse(e.message, status=400)
    return JsonResponse(
        ['These', 'Are', 'The', 'Results'], safe=False, status=200
    )
