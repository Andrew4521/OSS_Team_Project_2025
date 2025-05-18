import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import re

def select_excel_file():
    Tk().withdraw()
    return askopenfilename(
        title="엑셀 파일을 선택하세요",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )

def filter_courses_by_grade(df: pd.DataFrame, grade: str) -> pd.DataFrame:
    df = df[df['과목명'].notna()]
    return df[df['학년'].isin([grade, '전학년'])]

def parse_class_time(raw: str, lecture_type: str):
    """
    수업시간 문자열에서 요일/교시/강의실 정보를 추출.
    예:
    '월 01 ,02 ,03 [N14-202(56-202)]  수 04 ,05 [N14-202(56-202)]'
    →
    '월 01,02,03교시 (N14-202) / 수 04,05교시 (N14-202)'
    """
    if pd.isna(raw):
        if lecture_type == "OCU":
            return "온라인 수강"
        return "정보 없음"

    pattern = r"([월화수목금토일])\s*((?:\d{2}\s*,?\s*)+)\s*\[([^\[(]+)"
    matches = re.findall(pattern, raw)

    if not matches:
        return "정보 없음"

    result = []
    for day, times, room in matches:
        clean_times = ",".join([t.strip() for t in re.findall(r"\d{2}", times)])
        clean_room = room.strip()
        result.append(f"{day} {clean_times}교시 ({clean_room})")

    return " / " .join(result)

def main():
    file_path = select_excel_file()
    if not file_path:
        print("❗ 파일을 선택하지 않았습니다.")
        input("아무 키나 누르면 종료됩니다...")
        return

    try:
        df = pd.read_excel(file_path)

        print("필터링할 학년을 숫자로 입력하세요 (예: 1, 2, 3, 4)")
        num = input("학년 번호 입력: ").strip()

        if num not in {"1", "2", "3", "4"}:
            print("⚠️ 유효한 학년 번호는 1 ~ 4 입니다.")
            input("아무 키나 누르면 종료됩니다...")
            return

        grade_input = f"{num}학년"

        df = df[df['과목명'].notna()]
        total_courses = len(df)

        filtered_df = filter_courses_by_grade(df, grade_input)
        filtered_count = len(filtered_df)

        print(f"=== 필터링 이전 과목 수: {total_courses}개 ===")
        print(f"=== {grade_input} + 전학년 과목 수: {filtered_count}개 ===")

        if filtered_df.empty:
            print(f"⚠️ '{grade_input}'에 해당하는 과목이 없습니다.")
        else:
            for _, row in filtered_df.iterrows():
                course = row['과목명']
                category = row['이수구분']
                credit = int(row['학점'])
                year = row['학년']
                raw_time = row.get('수업시간', None)
                lecture_type = row.get('강의구분', '')
                time_and_place = parse_class_time(raw_time, lecture_type)

                print(f"- {course} | {category} | {credit}학점 | {year} | {time_and_place}")

        print("=== 필터링 완료 ===")
    except Exception as e:
        print(f"[오류 발생] {e}")

    input("아무 키나 누르면 종료됩니다...")

if __name__ == "__main__":
    main()
