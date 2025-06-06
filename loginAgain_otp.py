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

#id, pw 입력
while True:
    id = getpass.getpass("학번 입력 : ")
    pw = getpass.getpass("개신누리 비밀번호 입력 : ")

    try:
        username_field.send_keys(f"{id}")  #실제 아이디 입력
        password_field.send_keys(f"{pw}")  #실제 비밀번호 입력
        password_field.send_keys(Keys.RETURN)  #엔터 키 입력
        
        if driver.current_url in ['https://eisn.cbnu.ac.kr/nxui/index.html?OBSC_YN=0&LNG=ko#main','https://eisn.cbnu.ac.kr/nxui/index.html?OBSC_YN=0&LNG=ko']:
            break

    except:
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
