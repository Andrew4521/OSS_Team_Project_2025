import tkinter as tk
from tkinter import messagebox, Toplevel, Label
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def perform_login(school_num, pw):
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        driver.get("https://eis.cbnu.ac.kr/cbnuLogin")
        time.sleep(2)

        username_field = driver.find_element(By.NAME, "uid")
        password_field = driver.find_element(By.NAME, "pswd")

        username_field.send_keys(school_num)
        password_field.send_keys(pw)
        password_field.send_keys(Keys.RETURN)

        time.sleep(5)

        # 학점 페이지 이동
        driver.get("https://eisn.cbnu.ac.kr/nxui/index.html?OBSC_YN=0&LNG=ko#14295")

        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="mainframe.WrapFrame.form.div_section.form.div_content.form.div_work.form.w_14295.form.div_work.form.tab_main.tabbutton_1"]'))
        )
        button.click()

        sub_credit = []

        for i in range(1, 44):
            if i == 22:
                continue
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//*[@id='mainframe.WrapFrame.form.div_section.form.div_content.form.div_work.form.w_14295.form.div_work.form.tab_main.tpg_7.form.grd_tpg1Point.body.gridrow_0.cell_0_{i}']"))
                )
                sub_credit_value = element.get_attribute("aria-label")
                sub_credit.append(sub_credit_value)
            except Exception as e:
                print(f"요소 {i}를 찾을 수 없음: {e}")
                continue

        driver.quit()
        return True, sub_credit

    except Exception as e:
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
        for idx, item in enumerate(result):
            lbl = Label(result_popup, text=item, borderwidth=1, relief="solid", padx=5, pady=5)
            lbl.grid(row=row, column=col, padx=5, pady=5, sticky="w")
            col += 1
            if col >= 3:  # 3열 구성
                col = 0
                row += 1
    else:
        messagebox.showerror("로그인 실패", f"문제가 발생했습니다:\n{result}")


# Tkinter GUI 생성
root = tk.Tk()
root.title("개신누리 로그인")
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
