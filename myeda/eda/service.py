# 복잡한 비지니스 로직을 구현하기 위한 파일
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os
import base64
from io import BytesIO
from .models import Dataframe, Graph_plot

BASE_DIR = Path(__file__).resolve().parent.parent
insurance_df = pd.read_csv(os.path.join(BASE_DIR, 'eda','static', 'eda','insurance.csv'))

# Create your views here.
def myeda(request):
    head = insurance_df.head(5).to_html
    tail = insurance_df.tail(5).to_html

    sns.stripplot(x="region", y="children", data=insurance_df)
    my_stringIOBytes = BytesIO()
    plt.savefig(my_stringIOBytes, format='png')
    my_stringIOBytes.seek(0)
    my_base64_pngData = base64.b64encode(my_stringIOBytes.read()).decode("UTF-8")

    html = '<h3>header check</h3>'+'<img src=\"data:image/png;base64,{}\">'.format(my_base64_pngData) + '<h3>tail check</h3>'

    graph2 = sns.stripplot(x="region", y="charges", data=insurance_df)
    # plt.show()


    context = {'head':head, 'tail':tail, 'graph1':html, 'graph2':graph2, 'test':'test'}
    # context = {}
    return render(request, 'myeda.html', context)

# head, tail 반환
def head_and_tail():

    if is_in_dataframe("head"):
        head = Dataframe.objects.filter(name="head")[0]._html
    else:
        head = insurance_df.head(5).to_html()
        data = Dataframe(name="head", _html=head)
        data.save()
        
    if is_in_dataframe("tail"):
        tail = Dataframe.objects.filter(name="tail")[0]._html
    else:
        tail = insurance_df.tail(5).to_html()
        data = Dataframe(name="tail", _html=tail)
        data.save()

    return head, tail

# 전반적인 데이터 분석
def overall_analysis():
    temp = ["<h3 class='mt-4'>데이터 훑어보기</h3>"]

    ## 표본의 성비(sex) 계산
    male_cnt = insurance_df[insurance_df['sex']=='male'].count()[0]
    female_cnt = insurance_df[insurance_df['sex']=='female'].count()[0]
    temp.append("<div><b>male per</b> : %f <br> <b>female per</b> : %f 👩🏻‍🤝‍🧑🏻 표본의 성비는 비슷한 것을 알 수 있다!</div><br>" 
        % (male_cnt/insurance_df.count()[0], female_cnt/insurance_df.count()[0]))

    ## 데이터 변수 describe()
    temp.append('<div><span style="color:gray;">&#60;숫자형 변수들의 통계량 요약&#62;</span>')
    
    if is_in_dataframe("describe"):
        describe = Dataframe.objects.filter(name="describe")[0]._html
    else:
        describe = insurance_df.describe().to_html()
        data = Dataframe(name="describe", _html=describe)
        data.save()

    temp.append(describe)
    temp.append('</div>')
    temp.append('<br><hr><h4>이상치 확인</h4><br>❗ <code>children, charges</code>를 확인해볼 필요가 있다.<br>')

    ## region-children stripplot 조회
    if is_in_Graph_plot("region_children"):
        region_children = Graph_plot.objects.filter(name="region_children")[0]._html
    
    ## region-children stripplot 그리기
    else:
        sns.stripplot(x="region", y="children", data=insurance_df)
        region_children = plt_to_pngData()
        plt.close()
        data = Graph_plot(name="region_children", x="region", y="children",_html=region_children)
        data.save()

    temp.append(region_children)
    temp.append('<br>✅ <code>charges</code>는 소량의 이상치가 발견되었다.<br><br><hr><h4>결측치 확인</h4>')

    ## 결측치 확인 DataFrame
    temp.append('<span style="color:gray;">&#60;데이터에 Null 값 존재 여부&#62;</span>')

    if is_in_dataframe("isnull_any"):
        isnull_any = Dataframe.objects.filter(name="isnull_any")[0]._html
    else:
        isnull_any = insurance_df.isnull().any().to_frame().to_html()
        data = Dataframe(name="isnull_any", _html=isnull_any)
        data.save()
    
    temp.append(isnull_any)
    temp.append('<br>✅ <b>결측치</b>는 존재하지 않는다.<br><br><br><br>')

    return ''.join(temp)

# 데이터 상관관계 분석 1
def data_relation_1():
    temp = ["<h3 class='mt-4'>데이터 간 관계를 파악해보자</h3><hr>"]
    temp.append("<span style='color:gray;'>&#60;변수 간 상관계수&#62;</span>")

    if is_in_dataframe("corr"):
        corr = Dataframe.objects.filter(name="corr")[0]._html
    else:
        corr = insurance_df.corr().to_html()
        data = Dataframe(name="corr", _html=corr)
        data.save()
    
    temp.append(corr)
    temp.append("<br>❗ <code>(charges, age), (bmi, charges)</code> 상관계수가 높게 나왔다.<br><hr>")

    temp.append("<br><br><div><b>&#60; <code>region</code> - <code>charges</code>&#62; (hue = <code>smoker</code>) </b></div>")

    ## region - charges (hue = smoker)  Plot! 
    if is_in_Graph_plot("region_charges_smoker"):
        region_charges_smoker = Graph_plot.objects.filter(name="region_charges_smoker")[0]._html
    else:
        fig, ax = plt.subplots(figsize=(8,6))
        sns.swarmplot(x="region", y="charges", data=insurance_df, hue="smoker")
        region_charges_smoker = plt_to_pngData()
        plt.close()
        data = Graph_plot(name="region_charges_smoker", x="region", y="charges", hue="smoker", _html=region_charges_smoker)
        data.save()

    temp.append(region_charges_smoker)
    
    ## region - charges (hue = sex)  Plot!
    temp.append("<hr><br><div><b>&#60; <code>region</code> - <code>charges</code>&#62; (hue = <code>sex</code>) </b></div>")

    if is_in_Graph_plot("region_charges_sex"):
        region_charges_sex = Graph_plot.objects.filter(name="region_charges_sex")[0]._html
    else:
        fig, ax = plt.subplots(figsize=(8,6))
        sns.swarmplot(x="region", y="charges", data=insurance_df, hue="sex")
        region_charges_sex = plt_to_pngData()
        plt.close()
        data = Graph_plot(name="region_charges_sex", x="region", y="charges", hue="sex", _html=region_charges_sex)
        data.save()

    temp.append(region_charges_sex)
    temp.append('<br>✅ <code>charges</code>가 높은 표본은 흡연자인 경우가 대부분이다.<br><br><hr>')

    ## sex - age (hue = smoker)  Plot!
    temp.append("<br><div><b>&#60; <code>sex</code> - <code>age</code>&#62; (hue = <code>smoker</code>) </b></div>")
    
    if is_in_Graph_plot("sex_age_smoker"):
        sex_age_smoker = Graph_plot.objects.filter(name="sex_age_smoker")[0]._html
    else:
        fig, ax = plt.subplots(figsize=(8,6))
        sns.swarmplot(x="sex", y="age", data=insurance_df, hue="smoker")
        sex_age_smoker = plt_to_pngData()
        plt.close()
        data = Graph_plot(name="sex_age_smoker", x="sex", y="age", hue="smoker", _html=sex_age_smoker)
        data.save()
        
    temp.append(sex_age_smoker)
    temp.append('<br>✅ 남자가 여자보다 흡연자 비율이 비교적 높게 나왔다.<br><br><br>')

    return ''.join(temp)

# 데이터 상관관계 분석 2
def data_relation_2():
    temp = ["<h3 class='mt-4'>데이터 간 관계를 파악해보자 Ⅱ</h3><hr>"]

    ## age - charges  Plot!
    temp.append("<br><div><b>&#60; <code>age</code> - <code>charges</code> &#62;</b></div>")
    
    if is_in_Graph_plot("age_charges"):
        age_charges = Graph_plot.objects.filter(name="age_charges")[0]._html
    else:
        fig, ax = plt.subplots(figsize=(8,6))
        sns.scatterplot(x='age', y='charges', data=insurance_df)
        plt.yticks([i for i in range(0,64000,5000)])
        age_charges = plt_to_pngData()
        plt.close()
        data = Graph_plot(name="age_charges", x="age", y="charges", _html=age_charges)
        data.save()

    temp.append(age_charges)

    ## bmi - charges  Plot!
    temp.append("<hr><br><br><div><b>&#60; <code>bmi</code> - <code>charges</code> &#62; (hue = <code>smoker</code>)</b></div>")

    if is_in_Graph_plot("bmi_charges"):
        bmi_charges = Graph_plot.objects.filter(name="bmi_charges")[0]._html
    else:
        fig, ax = plt.subplots(figsize=(8,6))
        ax.set_xticks(np.arange(15,60,5))
        sns.scatterplot(x='bmi', y='charges', data=insurance_df, hue="smoker")
        bmi_charges = plt_to_pngData()
        plt.close()
        data = Graph_plot(name="bmi_charges", x="bmi", y="charges", _html=bmi_charges)
        data.save()

    temp.append(bmi_charges)

    ## description ! 
    temp.append("<br><br>✅ <b>Plot을 통해 다음의 3가지를 알 수 있다.</b><br>")
    temp.append("<ol start='1'><li>전 연령에 걸쳐서 <code>charges</code>가 1,000~1,7000에 가장 많이 분포하는 것으로 보인다.</li>")
    temp.append("<li>연령이 증가할수록 <code>charges</code>도 비례하여 증가하는 것으로 확인된다.</li>")
    temp.append("<li><code>charges</code>가 높을수록 데이터 수가 감소하는 것으로 보인다.</li></ol><br><br><br>")

    return ''.join(temp)

# 데이터 상관관계 분석 3
def data_relation_3():
    temp = ["<h3 class='mt-4'>데이터 간 관계를 파악해보자 Ⅲ</h3><hr>"]

    ## children - charges  Plot!
    temp.append("<br><br><div><b>&#60; <code>children</code> - <code>charges</code> &#62;</b></div>")

    if is_in_Graph_plot("children_charges"):
        children_charges = Graph_plot.objects.filter(name="children_charges")[0]._html
    else:
        fig, ax = plt.subplots(figsize=(8,6))
        sns.stripplot(x='children', y="charges", data=insurance_df)
        children_charges = plt_to_pngData()
        plt.close()
        data = Graph_plot(name="children_charges", x="children", y="charges", _html=children_charges)
        data.save()

    temp.append(children_charges)

    temp.append("<br><br>✅ <code>children</code>이 증가함에 따라 . .<br>")
    temp.append("<ul><li>오히려 <code>charges</code>가 감소하는 경향을 보인다.</li>")
    temp.append("<li><b>표본</b>의 수가 감소하는 경향을 보였다.</li></ul>")
    temp.append("<p>✔ <b><a href="">Data Set에 대한 설명</a>에서 <code>charges</code>가 모호하다고 서술했었는데, ")
    temp.append("위 Plot을 통해 부양 가족을 포함한 1인당 납부하는 금액이라고 추측할 수 있다.</b></p><br><br><br>")

    return ''.join(temp)

# 데이터 검증
def verificate():
    temp = ["<h3 class='mt-4'> 가설 검증하기</h4><hr>"]
    # implement !
    temp.append("<b>✏ 기존에 설정했던 가설</b><br><br>")
    temp.append("<ul>")
    temp.append("<li><code>age, bmi</code>가 높고 (<code>smoker</code>=='yes')인 경우 <code>charges</code>가 높지 않을까?</li>") 
    temp.append("<ul>✔ <code>age, bmi, smoker</code>는 모두 <code>charges</code>와 연관성을 보였다.</ul><br>")
    temp.append("<li>(<code>sex</code>=='male')인 경우가 <code>smoker</code>의 비중이 높지 않을까?</li>")
    temp.append("<ul>✔ 지배적이지 않은 약간의 연관성을 보였다.</ul><br>")
    temp.append("<li><code>children</code>이 많을수록 더 높은 <code>charges</code>를 가지지 않을까?</li>")
    temp.append("<ul>❌ 가설이 틀렸다. 오히려 <code>charges</code>가 감소하는 경향을 보였다.</ul>")
    temp.append("</ul>")
    
    return ''.join(temp)

# DIY Graph !
def diy_graph():
    temp = []
    # implement !
    pass


#/ plt를 base64 인코딩 후 html 변환시켜주는 메서드 /#
def plt_to_pngData():
    my_stringIOBytes = BytesIO()
    plt.savefig(my_stringIOBytes, format='png')
    my_stringIOBytes.seek(0)
    my_base64_pngData = base64.b64encode(my_stringIOBytes.read()).decode("UTF-8")
    html_str = '<img src=\"data:image/png;base64,{}\">'.format(my_base64_pngData)
    return html_str

#/ Dataframe이 DB 테이블에 있는지 체크 (boolean) /#
def is_in_dataframe(df_name):
    if not Dataframe.objects.filter(name=df_name):
        return False
    else:
        return True

#/ Graph_plot이 DB 테이블에 있는지 체크 (boolean) /#
def is_in_Graph_plot(plt_name):
    if not Graph_plot.objects.filter(name=plt_name):
        return False
    else:
        return True


