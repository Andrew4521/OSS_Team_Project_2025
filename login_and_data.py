from bs4 import BeautifulSoup
import requests
import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

school_num = getpass.getpass("학번을 입력해주세요 : ") #학번 입력
pw = getpass.getpass("비밀번호를 입력해주세요 : ") #개신누리 비밀번호 입력

gaesin_url = "https://eis.cbnu.ac.kr/cbnuLogin"
session = requests.Session()

payload = {
    "uid" : school_num,
    "pswd" : pw
}

respones = session.get(gaesin_url, data=payload) #개신누리 로그인

if respones.ok:
    print("로그인 성공")
    print(respones.status_code)
    

    new_session = requests.Session()
    
    login_url = "https://eisn.cbnu.ac.kr/nxui/index.html?OBSC_YN=0&LNG=ko#main"
    credit_url = login_url.replace("main","14295") #로그인 후 졸업학점 현황으로 넘어감

    driver =webdriver.Chrome()
    driver.get(credit_url)

    time.sleep(3)

    sub_credit_dict ={}

    for i in range(1,44):
        element_subject = driver.find_element(By.ID, f"mainframe.WrapFrame.form.div_section.form.div_content.form.div_work.form.w_14295.form.div_work.form.tab_main.tpg_7.form.grd_tpg1Point.body.gridrow_0.cell_0_{i}")
        subject_credit = element_subject.find_element(By.XPATH, ".//*[@aria-label]")
        sub_credit_value = subject_credit.text.split()
        sub_credit_dict[sub_credit_value[0]+sub_credit_value[1]] =sub_credit_value[2]

    for key in sub_credit_value:
        print(sub_credit_value[i])


    driver.quit()
    


else:
    print("로그인 실패",respones.status_code)
