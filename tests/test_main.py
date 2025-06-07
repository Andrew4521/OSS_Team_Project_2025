import unittest
import subprocess
import sys
import os

# 현재 파일(test_main.py)의 위치에서 상위 폴더 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestMainPy(unittest.TestCase):
    def test_main_runs_and_outputs(self):
        # 상위 폴더에 있는 main.py의 전체 경로 설정
        main_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'main.py')

        # main.py를 subprocess로 실행하여 출력 캡처
        result = subprocess.run(
            [sys.executable, main_path],
            capture_output=True,
            text=True
        )

        # 정상 종료 확인
        self.assertEqual(result.returncode, 0, msg=f"프로그램 실행 실패: {result.stderr}")

        # 출력 결과 확인 (예: timetable 출력 여부)
        self.assertIn("=== timetable_output ===", result.stdout)

if __name__ == '__main__':
    unittest.main()
