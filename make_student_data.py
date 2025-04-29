from bs4 import BeautifulSoup
import requests

class Student: #클래스 선언
    def __init__(self, student_number, student_name):
        self.student_number = None
        self.student_name = None
        self.student_credit = {}

student = Student(school_num, name) #로그인 시 입력받은 정보로 객체 생성


credit_url = gaesin_url.replace("main","14295") #로그인 후 졸업학점 현황으로 넘어감
req = requests.get(credit_url)
soup = BeautifulSoup(req.text, "html.parser") #웹페이지 html 받아옴

sub_credit_values = [div["aria-label"] for div in soup.find_all("div")] #전공, 교양 별 이수 학점들이 있는 텍스트를 가져옴


for value in sub_credit_values:
    words = value.split()
    subject_credit = [words[1], words[-1]] #전공, 교양, 일선 구분과 학점 값만 가져옴
    student.student_credit[subject_credit[0]] = int(subject_credit[1]) #생성했던 학생 객체의 딕셔너리에 각 학점 구분 별 학점 저장을 반복 저장


