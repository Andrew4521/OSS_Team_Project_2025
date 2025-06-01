import pandas as pd
import os
import re

def filter_courses_by_grade(df: pd.DataFrame, grade: str) -> pd.DataFrame:
    df = df[df['과목명'].notna()]
    return df[df['학년'].isin([grade, '전학년'])]

def parse_class_time(raw: str, lecture_type: str):
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

    return " / ".join(result)

def main():
    # 사용자 입력 받기
    major = input("전공 학과명을 입력하세요 (예: 컴퓨터공학과): ").strip()
    num = input("필터링할 학년을 숫자로 입력하세요 (예: 1, 2, 3, 4): ").strip()

    if num not in {"1", "2", "3", "4"}:
        print("⚠️ 유효한 학년 번호는 1 ~ 4 입니다.")
        input("아무 키나 누르면 종료됩니다...")
        return

    grade_input = f"{num}학년"
    filename = f"{major}.xlsx"
    file_path = os.path.join(os.getcwd(), filename)

    if not os.path.exists(file_path):
        print(f"❗ 엑셀 파일 '{filename}' 을(를) 찾을 수 없습니다. 동일 폴더 내에 존재해야 합니다.")
        input("아무 키나 누르면 종료됩니다...")
        return

    try:
        df = pd.read_excel(file_path)

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
