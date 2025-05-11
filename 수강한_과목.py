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
password_field.send_keys(Keys.RETURN)  #엔터 키 입력time.sleep(20) #20초 대기

#로그인 후 학점 이수 내역 페이지로 이동
driver.get("https://eisn.cbnu.ac.kr/nxui/index.html?OBSC_YN=0&LNG=ko#14295")
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="mainframe.WrapFrame.form.div_section.form.div_content.form.div_work.form.w_14295.form.div_work.form.tab_main.tabbutton_3"]'))
)
button.click()
time.sleep(10)

#모든 데이터를 받아올 때 까지 기다림
table_xpath = '//*[@id="mainframe.WrapFrame.form.div_section.form.div_content.form.div_work.form.w_14295.form.div_work.form.tab_main.tpg_3.form.grd_tpg3List.body"]'
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, table_xpath)))

row = 0
col = 0
xpath = f'//*[@id="mainframe.WrapFrame.form.div_section.form.div_content.form.div_work.form.w_14295.form.div_work.form.tab_main.tpg_3.form.grd_tpg3List.body.gridrow_{row}.cell_{row}_{col}"]'

#XPATH 존재 우뮤 확인 함수
def xpath_t_f(driver, xapth):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xapth)))
        return True

    except:
        return False
    
is_xpath_row = xpath_t_f(driver, xpath)
multi_list = []

while is_xpath_row: #만약 XPATH가 존재한다면 해당 데이터를 가져오고 다음 행렬 위치 값을 XPATH에 넣어줌.
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
    is_xpath_row = xpath_t_f(driver, xpath) #존재유무 확인
    

for i in multi_list:
    print(i)

#브라우저 닫기
driver.quit()
