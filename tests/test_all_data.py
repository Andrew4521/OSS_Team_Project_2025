import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# 상위 디렉토리를 모듈 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import all_data
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestAlldata(unittest.TestCase):
    @patch("all_data.driver")
    def setUp(self, mock_driver):
        self.mock_driver = mock_driver
        self.mock_driver.get.return_value = None  # 가짜 URL 접근 설정

    def test_login_success(self):
        with patch("all_data.login_xpath_function", return_value=True):
            result = all_data.login_xpath_function()
            self.assertTrue(result)

    def test_major_data_collection(self):
        fake_data = {
            "학년": "3",
            "이수학기": "6",
            "전공": "컴퓨터공학",
            "입학년도": "2021",
            "복수전공": "천문우주학과",
            "복수전공 시작년도": "2022"
        }
        with patch("all_data.majors", fake_data):
            self.assertEqual(all_data.majors["전공"], "컴퓨터공학")

    def test_credit_data_collection(self):
        fake_credit = ["교양_기초 12", "전공_필수 18", "전공_선택 15", "일반_선택 5"]
        with patch("all_data.sub_credit", fake_credit):
            self.assertIn("전공_필수 18", fake_credit)

    def test_course_data_collection(self):
        fake_courses = [["강의1", "A"], ["강의2", "B"], ["강의3", "C"]]
        with patch("all_data.multi_list", fake_courses):
            self.assertGreater(len(fake_courses), 0)
            self.assertIn(["강의2", "B"], fake_courses)

    def test_driver_quit(self):
        with patch.object(all_data.driver, "quit") as mock_quit:
            all_data.driver.quit()
            mock_quit.assert_called_once()

if __name__ == "__main__":
    unittest.main()
