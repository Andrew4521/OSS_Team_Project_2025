import tkinter as tk
from tkinter import messagebox, Toplevel, Label
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging

# 로그 파일 설정 (항상 같은 이름, 실행 시 덮어쓰기)
logging.basicConfig(filename="login_log.txt", filemode="w", level=logging.INFO, format="%(asctime)s - %(message)s")

def perform_login(school_num, pw):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # headless 다시 활성화
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        logging.info("웹사이트 접속 시작")
        driver.get("https://eis.cbnu.ac.kr/cbnuLogin")
        time.sleep(2)

        username_field = driver.find_element(By.NAME, "uid")
        password_field = driver.find_element(By.NAME, "pswd")
        username_field.send_keys(school_num)
        password_field.send_keys(pw)
        password_field.send_keys(Keys.RETURN)

        logging.info("로그인 정보 입력 완료")
        time.sleep(3)

        if "cbnuLogin" in driver.current_url:
            logging.warning("로그인 실패 감지 (로그인 페이지에 머무름)")
            driver.quit()
            return False, "아이디 혹은 비밀번호가 잘못되었습니다!"

        logging.info("로그인 성공, 학점 페이지 이동 시도")
        driver.get("https://eisn.cbnu.ac.kr/nxui/index.html?OBSC_YN=0&LNG=ko#14295")
        time.sleep(5)

        try:
            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="mainframe.WrapFrame.form.div_section.form.div_content.form.div_work.form.w_14295.form.div_work.form.tab_main.tabbutton_1"]'))
            )
            button.click()
            logging.info("학점 탭 클릭 완료")
        except Exception as e:
            logging.warning(f"학점 탭 클릭 실패: {e}")

        sub_credit = []
        for i in range(1, 44):
            if i == 22:
                continue
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, f"//*[@id='mainframe.WrapFrame.form.div_section.form.div_content.form.div_work.form.w_14295.form.div_work.form.tab_main.tpg_7.form.grd_tpg1Point.body.gridrow_0.cell_0_{i}']"))
                )
                sub_credit_value = element.get_attribute("aria-label")
                sub_credit.append(sub_credit_value)
            except:
                logging.warning(f"학점 항목 {i} 수집 실패")
                continue

        driver.quit()
        logging.info("학점 수집 완료")
        return True, sub_credit

    except Exception as e:
        logging.exception("예외 발생")
        return False, str(e)

def login():
    school_num = entry_id.get()
    pw = entry_pw.get()

    if not school_num or not pw:
        messagebox.showerror("입력 오류", "학번과 비밀번호를 모두 입력해주세요.")
        return

    loading_popup = Toplevel(root)
    loading_popup.title("로그인 중")
    tk.Label(loading_popup, text="로그인을 시도 중입니다. 잠시만 기다려주세요...").pack(padx=20, pady=20)
    loading_popup.update()
    root.after(2000, loading_popup.destroy)

    success, result = perform_login(school_num, pw)

    if success:
        result_popup = Toplevel(root)
        result_popup.title("학점 정보")
        row = 0
        col = 0
        for item in result:
            lbl = Label(result_popup, text=item, borderwidth=1, relief="solid", padx=5, pady=5)
            lbl.grid(row=row, column=col, padx=5, pady=5, sticky="w")
            col += 1
            if col >= 3:
                col = 0
                row += 1
    else:
        messagebox.showerror("로그인 실패", result)

root = tk.Tk()
root.title("개신누리 학점 수집기")
root.geometry("450x300")
root.resizable(False, False)

label_title = tk.Label(root, text="충북대 개신누리 로그인", font=("맑은 고딕", 16))
label_title.pack(pady=15)

label_id = tk.Label(root, text="학번:")
label_id.pack()
entry_id = tk.Entry(root, width=35)
entry_id.pack(pady=5)

label_pw = tk.Label(root, text="비밀번호:")
label_pw.pack()
entry_pw = tk.Entry(root, show='*', width=35)
entry_pw.pack(pady=5)

btn_login = tk.Button(root, text="로그인 및 학점 수집", width=25, height=2, command=login)
btn_login.pack(pady=20)

root.mainloop()