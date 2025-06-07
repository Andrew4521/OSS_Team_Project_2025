import unittest
import subprocess
import os
import json
import sys

# 현재 파일(test_scraper.py)의 위치에서 상위 폴더 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestScraperOutput(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # (1) 환경 변수에서 학번과 비밀번호를 읽어오기
        cbnu_id = os.environ.get("CBNU_ID")
        cbnu_pw = os.environ.get("CBNU_PW")

        # (2) 없으면 오류 발생시키기
        if not cbnu_id or not cbnu_pw:
            raise RuntimeError("환경 변수 CBNU_ID와 CBNU_PW가 설정되어 있지 않습니다.")  # pragma: no cover

        # (3) 줄바꿈으로 구분하여 stdin에 전달될 문자열 생성
        credentials = f"{cbnu_id}\n{cbnu_pw}\n"

        # (4) scraper.py 경로 지정 및 실행
        scraper_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scraper.py')
        process = subprocess.run(
            [sys.executable, scraper_path],
            input=credentials,
            capture_output=True,
            text=True
        )

        # (5) scraper.py가 실패하면 예외 발생
        if process.returncode != 0:
            raise RuntimeError(f"scraper.py 실행 실패:\n{process.stderr}")

    def test_student_json_exists(self):
        self.assertTrue(os.path.exists("student.json"), "student.json 파일이 존재하지 않습니다.")

    def test_student_json_format(self):
        with open("student.json", encoding="utf-8-sig") as f:
            data = json.load(f)

        required_keys = [
            "학년", "이수학기", "전공", "교과적용년도",
            "수강강의", "교양[최소:0/최대:0]_공통_기초",
            "기준학점_전공_필수", "전공_필수"
        ]

        for key in required_keys:
            self.assertIn(key, data, f"'{key}' 항목이 student.json에 없습니다.")

    def test_student_json_course_list(self):
        with open("student.json", encoding="utf-8-sig") as f:
            data = json.load(f)

        self.assertIn("수강강의", data)
        self.assertIsInstance(data["수강강의"], list)
        for course in data["수강강의"]:
            self.assertIsInstance(course, str)

if __name__ == '__main__':
    unittest.main()  # pragma: no cover
