# run_all.py

import subprocess
import sys

def main():
    # 1) scraper.py 실행 → student.json 갱신
    ret = subprocess.call([sys.executable, "scraper.py"])
    if ret != 0:
        print("❌ scraper.py 실행 중 오류 발생.")
        return

    # 2) make_time_table.py 실행 → 시간표 출력
    ret = subprocess.call([sys.executable, "make_time_table.py"])
    if ret != 0:
        print("❌ make_time_table.py 실행 중 오류 발생.")
        return

if __name__ == "__main__":
    main()