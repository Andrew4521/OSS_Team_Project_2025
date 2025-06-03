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

id = getpass.getpass()
pw = getpass.getpass()

username_field.send_keys(f"{id}")  #실제 아이디 입력
password_field.send_keys(f"{pw}")  #실제 비밀번호 입력
password_field.send_keys(Keys.RETURN)  #엔터 키 입력
time.sleep(20) #20초 대기

xpath = '//*[@id="mainframe.login.form.btn_yes"]'

def New_login_check(xpath):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return True
    except:
        return False

if New_login_check:
    New_login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    New_login.click()

time.sleep(5)
driver.quit()
