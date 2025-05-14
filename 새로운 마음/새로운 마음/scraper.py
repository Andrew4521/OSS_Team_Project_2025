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
id = getpass.getpass("학번: ")
pw = getpass.getpass("비밀번호: ")

username_field.send_keys(f"{id}")  #실제 아이디 입력
password_field.send_keys(f"{pw}")  #실제 비밀번호 입력
password_field.send_keys(Keys.RETURN)  #엔터 키 입력
time.sleep(20) #20초 대기

#로그인 후 학점 이수 내역 페이지로 이동
driver.get("https://eisn.cbnu.ac.kr/nxui/index.html?OBSC_YN=0&LNG=ko#14295")
time.sleep(10)


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

# 수강한 강의 가져오는 부분
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

# multi_list 필터링
filtered_courses = []
for row in multi_list:
    for tok in row:
        tok = tok.strip()
        if tok.startswith("교과목명"):
            name = tok[len("교과목명"):].strip()
            filtered_courses.append(name)
            break


# 학점 가져오는 부분
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


# 새 딕셔너리 생성
student_data = {}

# majors
student_data.update(majors)

# sub_credit
for entry in sub_credit:
    text  = entry.replace("\n", " ").strip()
    parts = text.split()
    if len(parts) < 2:
        continue
    key_tokens = parts[:-1]
    val_str    = parts[-1]
    key = "_".join(tok.strip() for tok in key_tokens)
    try:
        val = int(val_str)
    except ValueError:
        val = 0
    student_data[key] = val

   
# 필요없는 데이터 필터링
def filter_unwanted(data: dict) -> dict:
    unwanted = [
        "기준학점_교양[최소:0/최대:0]_OCU_기타",
        "기준학점_일반_선택",
        "기준학점_부전공_필수",
        "기준학점_부전공_선택",
        "기준학점_전공_교직_복수",
        "기준학점_다전공1_교직_복수",
        "기준학점_다전공2_선택",
        "기준학점_다전공2_교직_복수",
        "기준학점_다전공2_필수",
        "기준학점_교직_이론",
        "기준학점_교직_소양",
        "기준학점_교직_교육실습I,Ⅱ_교육봉사",
        "교양[최소:0/최대:0]_OCU_기타",
        "일반_선택",
        "전공_교직_복수",
        "부전공_필수",
        "부전공_선택",
        "다전공1_교직_복수",
        "다전공2_필수",
        "다전공2_선택",
        "다전공2_교직_복수",
        "교직_이론",
        "교직_소양",
        "교직_교육실습I,Ⅱ_교육봉사",
    ]
    return {k: v for k, v in data.items()
            if not any(k.startswith(p) for p in unwanted)}

student_data = filter_unwanted(student_data)
student_data["수강강의"] = filtered_courses

# student.json 으로 덮어쓰기
import json
with open("student.json", "w", encoding="utf-8") as fp:
    json.dump(student_data, fp, ensure_ascii=False, indent=2)

print("✅ student.json 생성 완료:")
print(json.dumps(student_data, ensure_ascii=False, indent=2))
