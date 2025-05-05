#pip install selenium webdriver-manager time 설치

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#최신 버전 크롬에 맞는 크롬드라이버 설치
service = Service(ChromeDriverManager(driver_version="136.0.7103.49").install())
driver = webdriver.Chrome(service=service)

#로그인 페이지 접속
driver.get("https://eis.cbnu.ac.kr/cbnuLogin")

#로그인
username_field = driver.find_element(By.NAME, "uid")
password_field = driver.find_element(By.NAME, "pswd")

username_field.send_keys("")  #실제 아이디 입력
password_field.send_keys("")  #실제 비밀번호 입력
password_field.send_keys(Keys.RETURN)  #엔터 키 입력
time.sleep(20) #20초 대기

#로그인 후 학점 이수 내역 페이지로 이동
driver.get("https://eisn.cbnu.ac.kr/nxui/index.html?OBSC_YN=0&LNG=ko#14295")
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="mainframe.WrapFrame.form.div_section.form.div_content.form.div_work.form.w_14295.form.div_work.form.tab_main.tabbutton_1"]'))
)
button.click()

#데이터 저장용 리스트
sub_credit = []

for i in range(1, 44):
    print(f"검색 중: id_{i}")

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
        driver.switch_to.default_content()

    except Exception as e:
        print(f"요소를 찾을 수 없음: {e}")
        continue  


#결과 출력
for k in sub_credit:
    print(k)

#브라우저 종료
driver.quit()
