from django.shortcuts import render
from django.http import HttpResponse
import json
from .service import *

# bootstrap 적용한 html Test 용
def load_eda(request):
    print("load_eda 호출됨")
    if request.method == "POST":
        print("load_eda POST 요청됨")
        try:
            num = request.POST.get('num', None)
            # 구현
            if num == '2':
                html_context = overall_analysis()
                
            elif num == '3':
                html_context = data_relation_1()

            elif num == '4':
                html_context = data_relation_2()

            elif num == '5':
                html_context = data_relation_3()
            elif num == '6':
                html_context = verificate()
            else:
                raise Exception("불러올 페이지가 없습니다.")
        except Exception as e:
            raise KeyError

        # print(html_context)        

        context = {'html':html_context} # 구현

        return HttpResponse(json.dumps(context), content_type="application/json")

    head, tail = head_and_tail()
    context = {'head':head, 'tail':tail}

    return render(request, 'index.html', context)


def profile(request):
    context = {}
    return render(request, 'introduce.html', context)

def letter(request):
    try:
        if request.method == "POST":
            print("letter POST 요청됨")
            
            ## 메시지 DB에 저장
            name = request.POST.get("name")
            content = request.POST.get("content")
            save_letter(name, content)
            ##

            alert("전송 완료되었습니다.")
            
        else:
            alert("올바른 요청이 아닙니다.")

    except:
        alert("예기치 못한 오류가 발생하였습니다.")
    finally:
        return render(request, 'index.html', {})
        
    return render(request, 'index.html', {})
    


def ready_eda(request):
    context = {}
    return render(request, 'bootstrap_test.html', context)

