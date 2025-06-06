# scraper.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui
import json

# ── (1) ChromeDriver 설치 및 브라우저 실행 ──
service = Service(ChromeDriverManager(driver_version="136.0.7103.49").install())
driver = webdriver.Chrome(service=service)

# ── (2) 로그인 페이지로 이동 ──
driver.get("https://eis.cbnu.ac.kr/cbnuLogin")

# ── (3) 아이디/비밀번호 입력 ──
username_field = driver.find_element(By.NAME, "uid")
password_field = driver.find_element(By.NAME, "pswd")

id = input("학번: ")
pw = input("비밀번호: ")

username_field.send_keys(id)
password_field.send_keys(pw)
password_field.send_keys(Keys.RETURN)

# ── (4) 추가 확인 버튼이 있을 경우 클릭 ──
login_xpath = '//*[@id="mainframe.login.form.btn_yes"]'
try:
    New_login = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, login_xpath))
    )
    New_login.click()
except:
    pass

time.sleep(5)

# ── (5) 학점 이수 내역 페이지로 이동 ──
driver.get("https://eisn.cbnu.ac.kr/nxui/index.html?OBSC_YN=0&LNG=ko#14295")

# ── (6) 학년·이수학기·전공·입학년도·복수전공 정보 수집 ──
majors = {
    "학년":"",
    "이수학기":"",
    "전공":"",
    "입학년도":"",
    "복수전공":"",
    "복수전공 시작년도":""
    }

try:
    time.sleep(2)
    for i in range(7):
        pyautogui.hotkey('ctrl', '-') 
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

# ── (7) 학점 이수 내역 탭으로 이동 ──
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.XPATH,
         '//*[@id="mainframe.WrapFrame.form.div_section.form.div_content.form.div_work.form.w_14295.form.div_work.form.tab_main.tabbutton_1"]')
    )
)
button.click()

# ── (8) 각 구분별 이수 학점 정보 수집 ──
sub_credit = []

for i in range(1, 44):
    if i == 22:
        continue
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 f"//*[@id='mainframe.WrapFrame.form.div_section.form.div_content.form.div_work.form.w_14295.form.div_work.form.tab_main.tpg_7.form.grd_tpg1Point.body.gridrow_0.cell_0_{i}']")
            )
        )
        sub_credit_value = element.get_attribute("aria-label").strip()
        sub_credit.append(sub_credit_value)
        print(sub_credit[-1])
    except Exception as e:
        print(f"요소를 찾을 수 없음(i={i}): {e}")
        continue

# ── (9) 수강강의 탭으로 이동 ──
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.XPATH,
         '//*[@id="mainframe.WrapFrame.form.div_section.form.div_content.form.div_work.form.w_14295.form.div_work.form.tab_main.tabbutton_3"]')
    )
)
button.click()
time.sleep(10)

# ── (10) 테이블 전체 로드 대기 ──
table_xpath = '//*[@id="mainframe.WrapFrame.form.div_section.form.div_content.form.div_work.form.w_14295.form.div_work.form.tab_main.tpg_3.form.grd_tpg3List.body"]'
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, table_xpath)))

# ── (11) 화면 축소 (스크롤바 없이 모든 열 보이도록) ──
actions = ActionChains(driver)
driver.switch_to.window(driver.current_window_handle)
for _ in range(7):
    pyautogui.hotkey('ctrl', '-')

# ── (12) multi_list에 각 행 단위로 10개 셀 수집 ──
multi_list = []
row = 0
col = 0
while True:
    inner_list = []
    try:
        for i in range(10):
            xpath = (
                f'//*[@id="mainframe.WrapFrame.form.div_section.form.div_content.form.div_work.form.w_14295'
                f'.form.div_work.form.tab_main.tpg_3.form.grd_tpg3List.body.gridrow_{row}'
                f'.cell_{row}_{col}"]'
            )
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            inner_list.append(element.get_attribute("aria-label").strip())
            col += 1
            if col == 10:
                col = 0
        multi_list.append(inner_list)
        row += 1
        col = 0
    except:
        break

for row_data in multi_list:
    print(row_data)

# ── (13) 브라우저 종료 ──
driver.quit()

# ── (14) multi_list에서 “교과목명”으로 시작하는 항목만 필터링 ──
filtered_courses = []
for row_data in multi_list:
    for cell in row_data:
        cell = cell.strip()
        if cell.startswith("교과목명"):
            name = cell[len("교과목명"):].strip()
            if name:
                filtered_courses.append(name)
            break

# ── (15) sub_credit 항목을 키-값으로 파싱 ──
#      예: "교양[최소:0/최대:0]_공통_기초 12" → key="교양[최소:0/최대:0]_공통_기초", val=12
credit_dict = {}
for entry in sub_credit:
    text = entry.replace("\n", " ").strip()
    parts = text.split()
    if len(parts) < 2:
        continue
    key_tokens = parts[:-1]
    val_str = parts[-1]
    key = "_".join(tok.strip() for tok in key_tokens)
    try:
        val = int(val_str)
    except ValueError:
        val = 0
    credit_dict[key] = val

# ── (16) majors, credit_dict, filtered_courses 합쳐서 student_data 딕셔너리 생성 ──
student_data = {}
student_data.update(majors)
student_data.update(credit_dict)
student_data["수강강의"] = filtered_courses

# ── (17) 불필요한 키 필터링 함수 정의 ──
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
    return {k: v for k, v in data.items() if not any(k.startswith(p) for p in unwanted)}

student_data = filter_unwanted(student_data)

# ── (18) student.json으로 저장 (UTF-8 with BOM) ──
with open("student.json", "w", encoding="utf-8-sig") as fp:
    json.dump(student_data, fp, ensure_ascii=False, indent=2)

print("✅ student.json 생성 완료:")
print(json.dumps(student_data, ensure_ascii=False, indent=2))
