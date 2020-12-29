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
    head = insurance_df.head(5).to_html()
    tail = insurance_df.tail(5).to_html()

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
    temp.append(insurance_df.describe().to_html())
    temp.append('</div>')
    temp.append('<br><hr><h4>이상치 확인</h4><br>❗ <code>children, charges</code>를 확인해볼 필요가 있다.<br>')

    ## region-children stripplot 그리기
    sns.stripplot(x="region", y="children", data=insurance_df)
    temp.append(plt_to_pngData())
    plt.close()
    
    ## region-charges striplot 그리기
    sns.stripplot(x="region", y="charges", data=insurance_df)
    temp.append(plt_to_pngData())
    plt.close()

    temp.append('<br>✅ <code>charges</code>는 소량의 이상치가 발견되었다.<br><br><hr><h4>결측치 확인</h4>')

    ## 결측치 확인 DataFrame
    temp.append('<span style="color:gray;">&#60;데이터에 Null 값 존재 여부&#62;</span>')
    temp.append(insurance_df.isnull().any().to_frame().to_html())
    
    temp.append('<br>✅ <b>결측치</b>는 존재하지 않는다.<br><br><br><br>')

    return ''.join(temp)

# 데이터 상관관계 분석 1
def data_relation_1():
    temp = ["<h3 class='mt-4'>데이터 간 관계를 파악해보자</h3><hr>"]
    temp.append("<span style='color:gray;'>&#60;변수 간 상관계수&#62;</span>")
    temp.append(insurance_df.corr().to_html())
    temp.append("<br>❗ <code>(charges, age), (bmi, charges)</code> 상관계수가 높게 나왔다.<br><hr>")


    ## region - charges (hue = smoker)  Plot! 
    fig, ax = plt.subplots(figsize=(8,6))
    sns.swarmplot(x="region", y="charges", data=insurance_df, hue="smoker")
    temp.append("<br><br><b>&#60; <code>region</code> - <code>charges</code>&#62; (hue = <code>smoker</code>) </b>")
    temp.append(plt_to_pngData())
    plt.close()

    ## region - charges (hue = sex)  Plot!
    fig, ax = plt.subplots(figsize=(8,6))
    sns.swarmplot(x="region", y="charges", data=insurance_df, hue="sex")
    temp.append("<hr><br><b>&#60; <code>region</code> - <code>charges</code>&#62; (hue = <code>sex</code>) </b>")
    temp.append(plt_to_pngData())
    plt.close()
    temp.append('<br>✅ <code>charges</code>가 높은 표본은 흡연자인 경우가 대부분이다.<br><br><hr>')

    ## sex - age (hue = smoker)  Plot!
    fig, ax = plt.subplots(figsize=(8,6))
    sns.swarmplot(x="sex", y="age", data=insurance_df, hue="smoker")
    temp.append("<br><b>&#60; <code>sex</code> - <code>age</code>&#62; (hue = <code>smoker</code>) </b>")
    temp.append(plt_to_pngData())
    plt.close()
    temp.append('<br>✅ 남자가 여자보다 흡연자 비율이 비교적 높게 나왔다.<br><br><br>')

    return ''.join(temp)

# 데이터 상관관계 분석 2
def data_relation_2():
    temp = ["<h3 class='mt-4'>데이터 간 관계를 파악해보자 Ⅱ</h3><hr>"]

    ## age - charges  Plot!
    fig, ax = plt.subplots(figsize=(8,6))
    sns.scatterplot(x='age', y='charges', data=insurance_df)
    plt.yticks([i for i in range(0,64000,5000)])
    temp.append("<br><b>&#60; <code>age</code> - <code>charges</code> &#62;</b>")
    temp.append(plt_to_pngData())
    plt.close()

    ## bmi - charges  Plot!
    fig, ax = plt.subplots(figsize=(8,6))
    ax.set_xticks(np.arange(15,60,5))
    sns.scatterplot(x='bmi', y='charges', data=insurance_df, hue="smoker")
    temp.append("<hr><br><br><b>&#60; <code>bmi</code> - <code>charges</code> &#62; (hue = <code>smoker</code>)</b>")
    temp.append(plt_to_pngData())
    plt.close()

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
    fig, ax = plt.subplots(figsize=(8,6))
    sns.stripplot(x='children', y="charges", data=insurance_df)
    temp.append("<br><br><b>&#60; <code>children</code> - <code>charges</code> &#62;</b>")
    temp.append(plt_to_pngData())
    plt.close()

    temp.append("<br><br>✅ <code>children</code>이 증가함에 따라 . .<br>")
    temp.append("<ul><li>오히려 <code>charges</code>가 감소하는 경향을 보인다.</li>")
    temp.append("<li><b>표본</b>의 수가 감소하는 경향을 보였다.</li></ul>")
    temp.append("<p>✔ <b><a href="">Data Set에 대한 설명</a>에서 <code>charges</code>가 모호하다고 서술했었는데, ")
    temp.append("위 Plot을 통해 부양 가족을 포함한 1인당 납부하는 금액이라고 추측할 수 있다.</b></p><br><br><br>")

    return ''.join(temp)

# 데이터 검증
def verificate():
    temp = []
    # implement !
    pass

# DIY Graph !
def diy_graph():
    temp = []
    # implement !
    pass

def plt_to_pngData():
    my_stringIOBytes = BytesIO()
    plt.savefig(my_stringIOBytes, format='png')
    my_stringIOBytes.seek(0)
    my_base64_pngData = base64.b64encode(my_stringIOBytes.read()).decode("UTF-8")
    html_str = '<img src=\"data:image/png;base64,{}\">'.format(my_base64_pngData)
    return html_str