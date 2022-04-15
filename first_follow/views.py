from django.shortcuts import render
import pandas as pd
from urllib3 import HTTPResponse
from first_follow import FF
from django.http import JsonResponse

import json
import copy
def format_(obj):
    obj_ = copy.deepcopy(obj)
    obj_["First"] = {k:list(v) for k,v in obj["First"].items()}
    obj_["Follow"] = {k:list(v) for k,v in obj["Follow"].items()}
    return obj_

def first_follow(request):
    if request.POST:
        res = dict(request.POST)
        res = {'grammer': ['{         "S": ["ACB", "CbB", "Ba"],         "A": ["da", "BC"],         "B": ["g", "@"],         "C": ["h", "@"]     }'], 'NonTerminal': ['{"S", "A", "B", "C"}'], 'Terminal': ['{"a", "b", "d", "g", "h"}']}
        cfg = json.loads(res['grammer'][0])
        terminal = eval(res['Terminal'][0])
        non_terminal = eval(res['NonTerminal'][0])
        print(cfg, terminal, non_terminal)
        ff = FF(cfg, terminal, non_terminal, "S")
        ff.calcFirst()
        ff.calcFollow()
        response = format_(ff.table)
        print(response)
        return JsonResponse(response, safe=False)

            
    return render(request, 'compiler.html', {})

