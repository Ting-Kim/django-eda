## 페이지 설계

- **(배경)** 왜 이 데이터셋을 선택했는가? (insurance)
- **(과정)** 데이터 분석 과정
    - head, tail 및 데이터 변수 형태 확인
    - 전체적인 데이터 분석(0~100% 값, 결측치 확인 등)
    - 데이터 상관관계 분석
        - (smoker, sex) & charges
        - (sex, smoker) & age
        - charges & age
        - bmi & charges
        - children & charges
        
- **(결론)** 가설 검증

- **(배포)** uWSGI & Nginx로 배포

<br>

#### Bonus 파트
- Bootstrap 사용
- Ajax 사용
- javascript D3 라이브러리 사용
- Client 단에서 Parameter 조절 가능하게 만들기
    - Ajax로 DIY 그래프 만들 수 있는 페이지
- 각 표/그래프마다 좋아요(하트)를 넣고 순위를 그래프로 만들기(?)
 