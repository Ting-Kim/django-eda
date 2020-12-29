from django.shortcuts import render
from django.http import HttpResponse
import json
from .service import *

# bootstrap 적용한 html Test 용
def load_eda(request):
    print("load_eda 호출됨")
    if request.method == "POST":
        print("load_eda POST 요청됨")
        num = request.POST.get('num', None)
        # print(type(num))
        # 구현
        if num == '2':
            html_context = overall_analysis()
            
        elif num == '3':
            html_context = data_relation_1()

        elif num == '4':
            html_context = data_relation_2()

        elif num == '5':
            html_context = data_relation_3()
            
        print(html_context)
        

        context = {'hello':'world', 'html':html_context} # 구현
        # context = {'hello':'world'} # 구현

        return HttpResponse(json.dumps(context), content_type="application/json")

    head, tail = head_and_tail()
    context = {'head':head, 'tail':tail}

    return render(request, 'index.html', context)


def post_eda(request):
    return
    

