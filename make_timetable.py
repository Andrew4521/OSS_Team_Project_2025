import json
import random
import re
from pathlib import Path

# 1) Student 클래스 정의 
class Student:
    def __init__(self, data):
        # ── 기본 프로필 ──
        self.grade = int(data.get("학년", "0").replace("학년", "").strip())
        try:
            self.semester = int(data.get("이수학기", "1").strip())
        except ValueError:
            self.semester = 1
        self.major = data.get("전공", "").strip()
        self.doubleMajor = data.get("복수전공", "").strip()
        self.curriculumYear = int(data.get("교과적용년도", "0").strip())
                # ── 이미 수강한 강의 목록 ──
        self.taken_courses = data.get("수강강의", [])

        # ── 이수 학점(cp_credit) ──
        self.cp_credit = {
            "GenEdCommonCore":     int(data.get("교양[최소:0/최대:0]_공통_기초", 0)),
            "GenEdNaturalCore":    int(data.get("교양[최소:0/최대:0]_자연_기초", 0)),
            "GenEdAdvanced":       int(data.get("교양[최소:0/최대:0]_심화", 0)),
            "GenEdSpecialized":    int(data.get("교양[최소:0/최대:0]_특성", 0)),
            "MajorCore":           int(data.get("전공_필수", 0)),
            "MajorElective":       int(data.get("전공_선택", 0)),
            "SecondMajorCore":     int(data.get("다전공1_필수", 0)),
            "SecondMajorElective": int(data.get("다전공1_선택", 0)),
        }

        # ── 요구 학점(rq_credit) ──
        self.rq_credit = {
            "GenEdCommonCore":     int(data.get("기준학점_교양[최소:0/최대:0]_공통_기초", 0)),
            "GenEdNaturalCore":    int(data.get("기준학점_교양[최소:0/최대:0]_자연_기초", 0)),
            "GenEdAdvanced":       int(data.get("기준학점_교양[최소:0/최대:0]_심화", 0)),
            "GenEdSpecialized":    int(data.get("기준학점_교양[최소:0/최대:0]_특성", 0)),
            "MajorCore":           int(data.get("기준학점_전공_필수", 0)),
            "MajorElective":       int(data.get("기준학점_전공_선택", 0)),
            "SecondMajorCore":     int(data.get("기준학점_다전공1_필수", 0)),
            "SecondMajorElective": int(data.get("기준학점_다전공1_선택", 0)),
        }



    def major_prefix(self):
        """주전공명으로 파일 접두어 반환."""
        m = self.major
        if m == "컴퓨터공학과": return "CP_"
        if m == "천문학과":     return "AS_"
        if m == "철학과":       return "PH_"
        if m == "경영학과":     return "MA_"
        raise ValueError(f"지원하지 않는 전공(주전공): '{m}'")

    def second_major_prefix(self):
        """복수전공명으로 파일 접두어 반환."""
        dm = self.doubleMajor
        if dm == "": 
            return ""
        if dm == "컴퓨터공학과": return "CP_"
        if dm == "천문학과":     return "AS_"
        if dm == "철학과":       return "PH_"
        if dm == "경영학과":     return "MA_"
        raise ValueError(f"지원하지 않는 복수전공: '{dm}'")

    def major_filename(self):
        yy = 25
        return f"{self.major_prefix()}{yy}_{self.semester}.json"

    def second_major_filename(self):
        if not self.doubleMajor:
            return ""
        yy = 25
        return f"{self.second_major_prefix()}{yy}_{self.semester}.json"



# 2) Course & TimeSlot 클래스
class TimeSlot:
    def __init__(self, day: str, slot: int):
        self.day = day
        self.slot = slot

    def __repr__(self):
        return f"{self.day}{self.slot}"


class Course:
    def __init__(self, data: dict):
        # ── 과목코드 저장 ──
        raw_code = data.get("과목코드", "")
        self.code = str(raw_code).strip()

        # ── 학년 파싱  ──
        h = data.get("학년", "").strip()
        if h.endswith("학년"):
            num_part = h[:-len("학년")]
            self.year = int(num_part) if num_part.isdigit() else 0
        else:
            self.year = int(h) if h.isdigit() else 0

        # ── 나머지 필드 ──
        self.category = data.get("이수구분", "").strip()
        self.name     = data.get("과목명", "").strip()
        self.credits  = int(data.get("학점", 0))

        raw_time = data.get("수업시간", "").strip()
        self.raw_time = raw_time  # 출력용 원본 수업시간

        # ── 대괄호 제거 (강의실 정보 등) ──
        no_brackets = re.sub(r"\[.*?\]", "", raw_time)

        # ── 요일-교시 매핑 ──
        tokens = no_brackets.split()
        self.times = []
        current_day = None
        for tok in tokens:
            if tok in ("월", "화", "수", "목", "금", "토", "일"):
                current_day = tok
            else:
                parts = tok.split(",")
                for p in parts:
                    p = p.strip()
                    if p.isdigit():
                        slot = int(p)
                        if current_day:
                            self.times.append(TimeSlot(current_day, slot))

    def __repr__(self):
        return f"<Course {self.code} {self.name} ({self.category}, {self.credits}학점) [{self.raw_time}]>"



# 3) 주말(토/일) 강의 제외 
def is_weekend_course(course: Course) -> bool:
    """course.times에 '토' 또는 '일'이 하나라도 있으면 True."""
    for t in course.times:
        if t.day in ("토", "일"):
            return True
    return False

# 4) 10교시 이상인 강의 제외
def is_invalid_time_course(course: Course) -> bool:
    """course.times에 교시(slot)이 10 이상 있으면 True."""
    for t in course.times:
        if t.slot >= 10:
            return True
    return False

# 5) 스케줄러 함수들
def load_courses_from_file(fname: str) -> list[Course]:
    """
    JSON 배열 파일 열어서 Course 리스트로 반환.
    """
    path = Path(fname)
    if not path.exists():
        raise FileNotFoundError(f"파일이 존재하지 않음: {fname}")
    with open(path, encoding="utf-8") as fp:
        arr = json.load(fp)

    all_courses = [Course(item) for item in arr]
    # 주말 및 10교시 이상인 강의를 제외
    return [c for c in all_courses if not is_weekend_course(c) and not is_invalid_time_course(c)]


def is_conflict(a: Course, b: Course) -> bool:
    """a, b 두 강의가 동일 요일+교시를 공유하면 True."""
    for t1 in a.times:
        for t2 in b.times:
            if t1.day == t2.day and t1.slot == t2.slot:
                return True
    return False


def has_conflict(c: Course, scheduled: list[Course]) -> bool:
    """이미 스케줄된 강의(scheduled) 중 하나라도 c와 충돌하면 True."""
    for sc in scheduled:
        if is_conflict(c, sc):
            return True
    return False


def sum_credits(scheduled: list[Course]) -> int:
    """시간표에 들어간 모든 강의의 학점 합."""
    return sum(c.credits for c in scheduled)


def filter_by_year_and_category(courses: list[Course], year: int, category: str) -> list[Course]:
    """
    학년(year) 또는 '전학년'(year=0)이고, 이수구분(category)이 일치하는 과목만 반환.
    """
    return [c for c in courses if (c.year == year or c.year == 0) and c.category == category]


def select_random(candidates: list[Course], need: int) -> list[Course]:
    """
    candidates에서 need학점이 될 때까지 무작위로 반환.
    """
    pool = candidates.copy()
    random.shuffle(pool)
    chosen = []
    total = 0
    for c in pool:
        if total >= need:
            break
        chosen.append(c)
        total += c.credits
    return chosen


def schedule_major_required(student: Student, second: bool=False) -> list[Course]:
    """
    전공 필수(주전공 or 복수전공) 리스트 반환.
    second=False → 주전공, True → 복수전공.
    """
    fname = student.second_major_filename() if second else student.major_filename()
    if not fname:
        return []
    all_major = load_courses_from_file(fname)
    return filter_by_year_and_category(all_major, student.grade, "전공필수")


def schedule_major_elective(student: Student, second: bool=False) -> list[Course]:
    """
    전공 선택(주전공 or 복수전공) 리스트 반환.
    """
    fname = student.second_major_filename() if second else student.major_filename()
    if not fname:
        return []
    all_major = load_courses_from_file(fname)
    return filter_by_year_and_category(all_major, student.grade, "전공선택")


def schedule_general_education(student: Student) -> list[Course]:
    """
    교양 과목(공통→자연→심화→특성) 부족 학점만큼 무작위 선택하여 반환.
    """
    schedule = []

    # 공통 기초
    need = student.rq_credit["GenEdCommonCore"] - student.cp_credit["GenEdCommonCore"]
    if need > 0:
        pool = load_courses_from_file("GE_Common.json")
        chosen = select_random(pool, need)
        schedule.extend(chosen)

    # 자연 기초
    need = student.rq_credit["GenEdNaturalCore"] - student.cp_credit["GenEdNaturalCore"]
    if need > 0:
        pool = load_courses_from_file("GE_Natural.json")
        chosen = select_random(pool, need)
        schedule.extend(chosen)

    # 심화
    need = student.rq_credit["GenEdAdvanced"] - student.cp_credit["GenEdAdvanced"]
    if need > 0:
        pool = load_courses_from_file("GE_Advanced.json")
        chosen = select_random(pool, need)
        schedule.extend(chosen)

    # 특성
    need = student.rq_credit["GenEdSpecialized"] - student.cp_credit["GenEdSpecialized"]
    if need > 0:
        pool = load_courses_from_file("GE_Specialized.json")
        chosen = select_random(pool, need)
        schedule.extend(chosen)

    return schedule

# 최후의 보루
def schedule_bastion(student: Student) -> list[Course]:
    """
    GE_BASTION.json 파일에서 후보를 뽑아 반환.
    """
    try:
        pool = load_courses_from_file("GE_BASTION.json")
    except FileNotFoundError:
        return []
    return pool

# 6) main(): 전체 시간표 생성 
def main():
    # 1) student.json 열어 Student 초기화
    with open("student.json", encoding="utf-8-sig") as fp:
        student_data = json.load(fp)
    student = Student(student_data)

    # 2) 학기 1학기로 설정
    student.semester = 1
         
    # 3) 빈 시간표 & 이미 추가된 과목코드 집합 생성
    timetable: list[Course] = []
    scheduled_codes: set[str] = set()

    # ── 4-1) 주전공 전공 필수 추가  ──
    if student.cp_credit["MajorCore"] < student.rq_credit["MajorCore"]:
        for c in schedule_major_required(student, second=False):
            if c.name in student.taken_courses:
                continue
            if c.code in scheduled_codes:
                continue
            if not has_conflict(c, timetable):
                timetable.append(c)
                scheduled_codes.add(c.code)

    # ── 4-2) 복수전공 전공 필수 추가 (필요할 때만) ──
    if student.doubleMajor and student.cp_credit["SecondMajorCore"] < student.rq_credit["SecondMajorCore"]:
        for c in schedule_major_required(student, second=True):
            if c.name in student.taken_courses:
                continue
            if c.code in scheduled_codes:
                continue
            if not has_conflict(c, timetable):
                timetable.append(c)
                scheduled_codes.add(c.code)

    # ── 4-3) 교양 추가 (필요할 때만) ──
    current = sum_credits(timetable)
    MIN_CR, MAX_CR = 18, 21
    if current < MIN_CR:
        gen_candidates = schedule_general_education(student)
        random.shuffle(gen_candidates)
        for c in gen_candidates:
            if current >= MIN_CR:
                break
                continue
            if c.name in student.taken_courses:
                continue
            if c.code in scheduled_codes:
                continue
            new_sum = current + c.credits
            if new_sum > MAX_CR:
                continue
            if has_conflict(c, timetable):
                continue
            timetable.append(c)
            scheduled_codes.add(c.code)
            current = new_sum

    # ── 4-4) 주전공 전공 선택 추가  ──
    if student.cp_credit["MajorElective"] < student.rq_credit["MajorElective"] and current < MIN_CR:
        candidates = schedule_major_elective(student, second=False)
        random.shuffle(candidates)
        for c in candidates:
            if current >= MIN_CR:
                break
            if c.name in student.taken_courses:
                continue
            if c.code in scheduled_codes:
                continue
            new_sum = current + c.credits
            if new_sum > MAX_CR:
                continue
            if has_conflict(c, timetable):
                continue
            timetable.append(c)
            scheduled_codes.add(c.code)
            current = new_sum

    # ── 4-5) 복수전공 전공 선택 추가 (필요할 때만) ──
    if student.doubleMajor and student.cp_credit["SecondMajorElective"] < student.rq_credit["SecondMajorElective"] and current < MIN_CR:
        candidates = schedule_major_elective(student, second=True)
        random.shuffle(candidates)
        for c in candidates:
            if current >= MIN_CR:
                break
            if c.name in student.taken_courses:
                continue
            if c.code in scheduled_codes:
                continue
            new_sum = current + c.credits
            if new_sum > MAX_CR:
                continue
            if has_conflict(c, timetable):
                continue
            timetable.append(c)
            scheduled_codes.add(c.code)
            current = new_sum

    # ── 4-6) BASTION으로 부족 학점 채우기 ──
    if current < MIN_CR:
        bastion_candidates = schedule_bastion(student)
        random.shuffle(bastion_candidates)
        for c in bastion_candidates:
            if current >= MIN_CR:
                break
            if c.name in student.taken_courses:
                continue
            if c.code in scheduled_codes:
                continue
            new_sum = current + c.credits
            if new_sum > MAX_CR:
                continue
            if has_conflict(c, timetable):
                continue
            timetable.append(c)
            scheduled_codes.add(c.code)
            current = new_sum
            
    # 5) 최종 시간표 출력
    print("\n=== 생성된 시간표 ===\n")
    for c in timetable:
        print(f"{c.code} {c.name} ({c.category}, {c.credits}학점) → {c.raw_time}")
    print(f"\n총 학점: {sum_credits(timetable)}\n")


if __name__ == "__main__":
    main()
