# 학적 정보 기반 자동 시간표 작성 알고리즘
<hr style="height:3px; background-color:black; border:none;" />

충북대학교 오픈소스기초프로젝트 좌충우돌💥팀에서 진행하는 자동 시간표 작성 알고리즘에 대한 소개 문서입니다.

## 💻프로젝트 소개
이 프로그램은 매 학기 시간표를 짜는 번거로움을 덜기 위해 개발되었습니다. 입력받은 로그인 정보를 토대로 학생의 이수 현황과 개설 과목 정보를 바탕으로 자동으로 시간표를 구성해주며, 이를 통해 수강 계획에 드는 시간을 줄이고, 보다 효율적인 학사 운영이 가능하도록 돕습니다. 특히 수강 신청을 앞둔 학생이나 졸업 요건을 관리하는 이들에게 유용합니다.
### 이 알고리즘에서는
- GUI 팝업 창이 열려서 로그인 정보를 입력받습니다
- 입력받은 학번과 비밀번호를 이용해서 개신누리 사이트에 자동으로 로그인, 학적 정보를 스캔합니다.
- 수집된 사용자의 학점이수현황과 학년정보, 기이수한 과목들 등의 정보들을 토대로 임의의 시간표를 작성합니다.

## 📅개발 기간
2025.04.03(목) ~ 2025.06.07(토)

## 🧑‍💻개발자 소개
- 박태훈 @Andrew4521 / Email: pthoon0605@naver.com
- 박호상@qtkqhg / Email: bakhosang@gmail.com
- 이규원@Leegyuone / Email: pakachu1994@chungbuk.ac.kr
- 정민준 @gisook / Email: mj5037885@gmail.com

## 💾 요구 플러그인 및 브라우저 설치법

```
우선 Chrome Brower를 최신 버전으로 설치

이후 PowerShell 을 열어서 아래 명령어들을 실행

- pip install pyautogui
- pip install selenium
- pip install webdriver-manager
```
*크롬이 없다면 webdriver-manager가 드라이버 다운로드에 실패할 수 있음.

## ✏️ 실행 방법

## 🎬 실행 화면
- 시작 GUI
  
- 결과 화면
  
- 매 실행마다 전공필수 과목을 제외한 교양과 전공선택 과목은 모종의 랜덤성을 갖고 결정됨

## 📁 의존성

```데이터 수집에 필요한 플러그인
PyAutoGUI                    0.9.54,
selenium                     4.32.0,
webdriver-manager            4.0.2,
chrome                       136.0.7103.49
```

## 📋 LICENSE
