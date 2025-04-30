from bs4 import BeautifulSoup
import requests
import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By

school_num = getpass.getpass() #학번 입력
pw = getpass.getpass() #개신누리 비밀번호 입력

class Student: #클래스 선언
    def __init__(self, student_number):
        self.student_number = None
        self.student_name = None
        self.student_credit = {}

gaesin_url = "https://eis.cbnu.ac.kr/cbnuLogin"
session = requests.Session()

payload = {
    "uid" : school_num,
    "pswd" : pw
}

respones = session.get(gaesin_url, data=payload) #개신누리 로그인

if respones.ok:
    login_url = "https://eisn.cbnu.ac.kr/nxui/index.html?OBSC_YN=0&LNG=ko#main"
    print("ok")
    print(respones.status_code)

else:
    print("실패",respones.status_code)


student = Student(school_num) #로그인 시 입력받은 정보로 객체 생성


credit_url = login_url.replace("main","14295") #로그인 후 졸업학점 현황으로 넘어감
driver = webdriver.Chrome()
driver.get(login_url)

targets_ids = []
raw_data = []
subject_credit = {}

for i in range(1,44): #웹에서 학점 내역의 정보를 가지고 있는 요소의 id를 저장
    id=f"mainframe.WrapFrame.form.div_section.form.div_content.form.div_work.form.w_14295.form.div_work.form.tab_main.tpg_7.form.grd_tpg1Point.body.gridrow_0.cell_0_{i}"
    targets_ids.append(id)

for id_value in targets_ids: #웹페이지의 전공, 교양별 학점 요소를 가져옴
    element = driver.find_element(By.ID, id_value)
    if element:
        raw_data.append(element.get_attribute("arial-label"))
    else:
        continue

for value in raw_data:
    words = value.split()
    subject_credit = [words[1], words[-1]] #전공, 교양, 일선 구분과 학점 값만 가져옴
    student.student_credit[subject_credit[0]] = int(subject_credit[1]) #생성했던 학생 객체의 딕셔너리에 각 학점 구분 별 학점 저장을 반복 저장