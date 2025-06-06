from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui

#최신 버전 크롬에 맞는 크롬드라이버 설치
service = Service(ChromeDriverManager(driver_version="136.0.7103.49").install())
driver = webdriver.Chrome(service=service)

#로그인 페이지 접속
driver.get("https://eis.cbnu.ac.kr/cbnuLogin")

#로그인
username_field = driver.find_element(By.NAME, "uid")
password_field = driver.find_element(By.NAME, "pswd")

#otp 존재 유무 확인
def otp_xpath_function(xpath):
    try:
        driver.find_element(By.XPATH, '//*[@id="user_otpCode_login"]')
        return True
    
    except:
        return False

#id, pw 입력
while True:
    id = getpass.getpass("학번 입력 : ")
    pw = getpass.getpass("개신누리 비밀번호 입력 : ")

    username_field.send_keys(f"{id}")  #실제 아이디 입력
    password_field.send_keys(f"{pw}")  #실제 비밀번호 입력
    password_field.send_keys(Keys.RETURN)  #엔터 키 입력

    if otp_xpath_function('//*[@id="user_otpCode_login"]') or (driver.current_url in ['https://eisn.cbnu.ac.kr/nxui/index.html?OBSC_YN=0&LNG=ko#', 'https://eisn.cbnu.ac.kr/nxui/index.html?OBSC_YN=0&LNG=ko#main']):
        break

    else:
        username_field.clear()
        password_field.clear()
        print("다시 입력해주세요.")

time.sleep(2) #로그인이 오래 걸릴 경우, 웹페이지가 닫기는 문제 해결

#2초 대기 후 otp 입력받음
if otp_xpath_function('//*[@id="user_otpCode_login"]'):
    otp_input = driver.find_element(By.XPATH, '//*[@id="user_otpCode_login"]')

    while True:
        otp = getpass.getpass("otp 번호를 입력해주세요 : ")
        otp_input.send_keys(f"{otp}")
        otp_input.send_keys(Keys.RETURN)

        try:
            if driver.current_url == 'https://eisn.cbnu.ac.kr/nxui/index.html?OBSC_YN=0&LNG=ko#main':
                break

            if driver.current_url == 'https://eisn.cbnu.ac.kr/nxui/index.html?OBSC_YN=0&LNG=ko':
                login_xpath = '//*[@id="mainframe.login.form.btn_yes"]'
                time.sleep(2)

                try:
                    New_login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, login_xpath)))
                    New_login.click()
                    break

                except:
                    print("프로그램을 다시 실행해주세요")
                    break

        except:
            otp_input.clear()
            print("다시 입력해주세요")
            continue

time.sleep(5) #웹페이지 유지용

#로그인 후 학점 이수 내역 페이지로 이동
driver.get("https://eisn.cbnu.ac.kr/nxui/index.html?OBSC_YN=0&LNG=ko#14295")
time.sleep(1)
for i in range(7):
    pyautogui.hotkey('ctrl', '-')

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

button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="mainframe.WrapFrame.form.div_section.form.div_content.form.div_work.form.w_14295.form.div_work.form.tab_main.tabbutton_1"]'))
)
button.click()

#데이터 저장용 리스트
sub_credit = []

for i in range(1, 44):
    if i == 22: #학점과 관련 없는 내용
        continue

    try:
        #각 구분별 요소
        element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, f"//*[@id='mainframe.WrapFrame.form.div_section.form.div_content.form.div_work.form.w_14295.form.div_work.form.tab_main.tpg_7.form.grd_tpg1Point.body.gridrow_0.cell_0_{i}']"))
)

        #구분별 학점 이수내역
        sub_credit_value = element.get_attribute("aria-label")
        sub_credit.append(sub_credit_value)
        print(sub_credit[-1])

    except Exception as e:
        print(f"요소를 찾을 수 없음: {e}")
        continue  


#결과 출력
for k in sub_credit:
    print(k)

button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="mainframe.WrapFrame.form.div_section.form.div_content.form.div_work.form.w_14295.form.div_work.form.tab_main.tabbutton_3"]'))
)
button.click()
time.sleep(10)

# 요소가 로드될 때까지 기다림 (테이블 전체)
table_xpath = '//*[@id="mainframe.WrapFrame.form.div_section.form.div_content.form.div_work.form.w_14295.form.div_work.form.tab_main.tpg_3.form.grd_tpg3List.body"]'
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, table_xpath)))

#웹 페이지 크기를 줄여 모든 요소 표시
actions = ActionChains(driver)
driver.switch_to.window(driver.current_window_handle)

for i in range(7):
    pyautogui.hotkey('ctrl', '-')

row = 0
col = 0
multi_list = []
xpath = f'//*[@id="mainframe.WrapFrame.form.div_section.form.div_content.form.div_work.form.w_14295.form.div_work.form.tab_main.tpg_3.form.grd_tpg3List.body.gridrow_{row}.cell_{row}_{col}"]'


try:
    while True: #만약 XPATH가 존재한다면 해당 데이터를 가져오고 다음 행렬 위치 값을 XPATH에 넣어줌.
        inner_list = [] #각 행을 저장할 리스트

        for i in range(10):
            element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
    )
        
            inner_list.append(element.get_attribute("aria-label"))
            col += 1

            if col == 10: #열의 범위를 넘어가면 초기화
                col = 0
        
            xpath = f'//*[@id="mainframe.WrapFrame.form.div_section.form.div_content.form.div_work.form.w_14295.form.div_work.form.tab_main.tpg_3.form.grd_tpg3List.body.gridrow_{row}.cell_{row}_{col}"]'

        multi_list.append(inner_list)

        row += 1
        xpath = f'//*[@id="mainframe.WrapFrame.form.div_section.form.div_content.form.div_work.form.w_14295.form.div_work.form.tab_main.tpg_3.form.grd_tpg3List.body.gridrow_{row}.cell_{row}_{col}"]' #다음 요소의 XPATH 저장

except:
    print("오류 발생")
    

for i in multi_list:
    print(i)

#브라우저 닫기
driver.quit()
