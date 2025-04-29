from bs4 import BeautifulSoup
import requests
import getpass

school_num = getpass.getpass() #학번 입력
pw = getpass.getpass() #개신누리 비밀번호 입력

gaesin_url = "https://eis.cbnu.ac.kr/cbnuLogin"
session = requests.Session()



payload = {
    "uid" : school_num,
    "pswd" : pw
}

respones = session.get(gaesin_url, data=payload) #개신누리 로그인

if respones.ok:
    print("ok")
    print(respones.status_code)

else:
    print("실패",respones.status_code)







