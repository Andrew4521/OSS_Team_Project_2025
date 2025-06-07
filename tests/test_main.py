import unittest
import subprocess
import sys

class TestMainPy(unittest.TestCase):
    def test_main_runs_and_outputs(self):
        # main.py를 subprocess로 실행해서 출력 결과 캡처
        result = subprocess.run(
            [sys.executable, 'main.py'],
            capture_output=True,
            text=True
        )

        # 프로그램이 정상 종료되었는지 확인
        self.assertEqual(result.returncode, 0, msg=f"프로그램 실행 실패: {result.stderr}")

        # 출력 결과에 특정 키워드가 포함되었는지 테스트
        # 예: timetable 출력 로그가 나오면 통과
        self.assertIn("=== timetable_output ===", result.stdout)

if __name__ == '__main__':
    unittest.main()
