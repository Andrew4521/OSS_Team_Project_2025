import requests
from bs4 import BeautifulSoup

def fetch_credit_info(student_id, password):
    try:
        login_url = "https://eis.cbnu.ac.kr/sso/login/check"
        credit_url = "https://eisn.cbnu.ac.kr/nxui/index.html?OBSC_YN=0&LNG=ko#14295"

        session = requests.Session()

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://eis.cbnu.ac.kr/cbnuLogin"
        }

        payload = {
            "id": student_id,
            "password": password,
            "redirectUrl": "https://eis.cbnu.ac.kr/main"
        }

        res = session.post(login_url, headers=headers, data=payload)
        if res.status_code != 200 or "main" not in res.text:
            return False, "로그인 실패 또는 페이지 이동 실패"

        credit_page = session.get(credit_url, headers=headers)
        soup = BeautifulSoup(credit_page.text, "html.parser")

        # 현재는 예시 데이터 (추후 실제 구조 분석 필요)
        dummy_data = [
            "전공 33학점", "교양 20학점", "일선 12학점",
            "기초 6학점", "핵심 8학점", "심화 9학점"
        ]

        return True, dummy_data

    except Exception as e:
        return False, f"에러 발생: {e}"
