from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass

#최신 버전 크롬에 맞는 크롬드라이버 설치
service = Service(ChromeDriverManager(driver_version="136.0.7103.49").install())
driver = webdriver.Chrome(service=service)

#로그인 페이지 접속
driver.get("https://eis.cbnu.ac.kr/cbnuLogin")

#로그인
username_field = driver.find_element(By.NAME, "uid")
password_field = driver.find_element(By.NAME, "pswd")

#아이디, 비밀번호 입력
id = getpass.getpass()
pw = getpass.getpass()

username_field.send_keys(f"{id}")  #실제 아이디 입력
password_field.send_keys(f"{pw}")  #실제 비밀번호 입력
password_field.send_keys(Keys.RETURN)  #엔터 키 입력
time.sleep(20) #20초 대기

#로그인 후 학점 이수 내역 페이지로 이동
driver.get("https://eisn.cbnu.ac.kr/nxui/index.html?OBSC_YN=0&LNG=ko#14295")
time.sleep(10)

#입학년도, 전공, 복수전공 가져와 저장
#입학년도, 전공, 복수전공 가져와 저장
majors = {
    "학년":"",
    "이수학기":"",
    "전공":"",
    "입학년도":"",
    "복수전공":"",
    "복수전공 시작년도":""
    }

try:

    for i in ["11","12","05","03","16"]: #데이터 가져와 위 딕셔너리에 저장
        element = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, f'//*[@id="mainframe.WrapFrame.form.div_section.form.div_content.form.div_work.form.w_14295.form.div_work.form.tab_main.tpg_1.form.div_detail.form.edt_txt{i}:input"]'))
)
        if i == "11": #학년 저장
            grade = element.get_attribute("value")
            print(grade)
            majors["학년"] = grade

        elif i == "12": #이수학기 저장
            semester = element.get_attribute("value")
            print(semester)
            majors["이수학기"] = semester

        elif i == "05": #전공 저장
            major = element.get_attribute("value")
            print(major)
            majors["전공"] = major
        
        elif i == "03": #입학년도 저장
            welcome = element.get_attribute("value")
            print(welcome)
            majors["교과적용년도"] = welcome

        else: #복수전공 시작년도와 복수전공을 나눠서 저장
            year_second_major = element.get_attribute("value")
            print(year_second_major)
            year_major = year_second_major.split()
            majors["복수전공"] = year_major[1]
            majors["복수전공 시작년도"] = year_major[0]

    
    for key, value in majors.items():
        print(f"{key}, {value}")


except Exception as e:
    print(f"예외 {e}")

