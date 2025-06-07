# tests/test_make_timetable.py
import sys
import os
import json
import random
import re
import pytest
from pathlib import Path

# 프로젝트 루트를 import 경로에 추가
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import make_timetable as mt

# ─── Helper Function Tests ─────────────────────────

def test_is_weekend_and_invalid_time():
    c_weekend = mt.Course({"과목코드":"W","학년":"0","이수구분":"","과목명":"","학점":1,"수업시간":"토 01"})
    c_late    = mt.Course({"과목코드":"L","학년":"0","이수구분":"","과목명":"","학점":1,"수업시간":"월 10"})
    assert mt.is_weekend_course(c_weekend)
    assert mt.is_invalid_time_course(c_late)


def test_conflict_and_has_conflict():
    cA = mt.Course({"과목코드":"A","학년":"2학년","이수구분":"","과목명":"","학점":3,"수업시간":"월 01"})
    cB = mt.Course({"과목코드":"B","학년":"2학년","이수구분":"","과목명":"","학점":3,"수업시간":"월 01"})
    cC = mt.Course({"과목코드":"C","학년":"2학년","이수구분":"","과목명":"","학점":3,"수업시간":"화 01"})
    assert mt.is_conflict(cA, cB)
    assert not mt.is_conflict(cA, cC)
    assert mt.has_conflict(cB, [cA])
    assert not mt.has_conflict(cC, [cA])


def test_filter_and_select_random():
    c0 = mt.Course({"과목코드":"0","학년":"0학년","이수구분":"X","과목명":"","학점":3,"수업시간":"월 01"})
    c2 = mt.Course({"과목코드":"2","학년":"2학년","이수구분":"X","과목명":"","학점":3,"수업시간":"월 02"})
    out = mt.filter_by_year_and_category([c0, c2], 2, "X")
    assert c0 in out and c2 in out
    pool = [mt.Course({"과목코드":str(i),"학년":"0","이수구분":"","과목명":"","학점":3,"수업시간":"월 01"}) for i in range(4)]
    sel = mt.select_random(pool, 7)
    assert sum(c.credits for c in sel) >= 7

# ─── Student Methods Tests ─────────────────────────

def test_student_prefix_and_filename():
    data = {"학년":"1학년","이수학기":"2","전공":"컴퓨터공학과","복수전공":"철학과","교과적용년도":"2025","수강강의":[]}
    stu = mt.Student(data)
    assert stu.major_prefix() == "CP_"
    assert stu.second_major_prefix() == "PH_"
    stu.semester = 2
    assert stu.major_filename() == "CP_25_2.json"
    assert stu.second_major_filename() == "PH_25_2.json"
    stu.major = "Unknown"
    with pytest.raises(ValueError):
        stu.major_prefix()


def test_student_semester_invalid_value():
    data = {"학년":"1학년","이수학기":"abc","전공":"경영학과","복수전공":"","교과적용년도":"2025","수강강의":[]}
    stu = mt.Student(data)
    assert stu.semester == 1

# ─── CP & RQ Credit Parsing Tests ───────────────────

def test_credit_parsing():
    data = {"학년":"1학년","이수학기":"1","전공":"철학과","복수전공":"","교과적용년도":"2025","수강강의":[]}
    data.update({
        "교양[최소:0/최대:0]_공통_기초": "5",
        "교양[최소:0/최대:0]_자연_기초": "4",
        "교양[최소:0/최대:0]_심화": "3",
        "교양[최소:0/최대:0]_특성": "2",
        "전공_필수": "6",
        "전공_선택": "1",
        "다전공1_필수": "3",
        "다전공1_선택": "2",
        "기준학점_교양[최소:0/최대:0]_공통_기초": "6",
        "기준학점_교양[최소:0/최대:0]_자연_기초": "5",
        "기준학점_교양[최소:0/최대:0]_심화": "4",
        "기준학점_교양[최소:0/최대:0]_특성": "3",
        "기준학점_전공_필수": "7",
        "기준학점_전공_선택": "2",
        "기준학점_다전공1_필수": "4",
        "기준학점_다전공1_선택": "1",
    })
    stu = mt.Student(data)
    assert stu.cp_credit["GenEdCommonCore"] == 5
    assert stu.cp_credit["MajorElective"] == 1
    assert stu.cp_credit["SecondMajorCore"] == 3
    assert stu.rq_credit["GenEdSpecialized"] == 3
    assert stu.rq_credit["MajorCore"] == 7

# ─── Course Parsing Tests ──────────────────────────

def test_course_bracket_removal_and_repr():
    raw = "월[강의실] 1,2 화[실험실] 3"
    data = {"과목코드":"B","학년":"0학년","이수구분":"","과목명":"BracketTest","학점":2,"수업시간":raw}
    course = mt.Course(data)
    assert course.raw_time == raw
    dayslots = [(t.day, t.slot) for t in course.times]
    assert ("월",1) in dayslots and ("월",2) in dayslots and ("화",3) in dayslots
    rep = repr(course)
    assert "BracketTest" in rep and "B" in rep

# ─── load_courses_from_file Tests ────────────────────

def test_load_courses_file(tmp_path):
    arr = [
        {"과목코드":"W","학년":"0학년","이수구분":"X","과목명":"","학점":1,"수업시간":"토 01"},
        {"과목코드":"G","학년":"0학년","이수구분":"X","과목명":"","학점":1,"수업시간":"수 03"}
    ]
    file = tmp_path / "courses.json"
    file.write_text(json.dumps(arr), encoding="utf-8")
    courses = mt.load_courses_from_file(str(file))
    assert len(courses) == 1 and courses[0].code == "G"
    with pytest.raises(FileNotFoundError):
        mt.load_courses_from_file(str(tmp_path / "none.json"))

# ─── Scheduling Functions Tests ─────────────────────

@pytest.fixture

def base_student(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    student = {"학년":"2학년","이수학기":"1","전공":"천문학과","복수전공":"경영학과","교과적용년도":"2025","수강강의":[]}
    for k in ["전공_필수","전공_선택","다전공1_필수","다전공1_선택","교양[최소:0/최대:0]_공통_기초","교양[최소:0/최대:0]_자연_기초","교양[최소:0/최대:0]_심화","교양[최소:0/최대:0]_특성"]:
        student[k] = 0
    for k in ["기준학점_전공_필수","기준학점_전공_선택","기준학점_다전공1_필수","기준학점_다전공1_선택","기준학점_교양[최소:0/최대:0]_공통_기초","기준학점_교양[최소:0/최대:0]_자연_기초","기준학점_교양[최소:0/최대:0]_심화","기준학점_교양[최소:0/최대:0]_특성"]:
        student[k] = 3
    Path("student.json").write_text(json.dumps(student, ensure_ascii=False), encoding="utf-8-sig")
    return mt.Student(student)


def test_schedule_required_and_elective(base_student):
    majors = [
        {"과목코드":"P1","학년":"2학년","이수구분":"전공필수","과목명":"R1","학점":3,"수업시간":"월 01"},
        {"과목코드":"P2","학년":"2학년","이수구분":"전공선택","과목명":"E1","학점":3,"수업시간":"화 02"}
    ]
    Path("AS_25_1.json").write_text(json.dumps(majors), encoding="utf-8")
    Path("MA_25_1.json").write_text(json.dumps(majors), encoding="utf-8")  # 복수전공 파일 생성
    req = mt.schedule_major_required(base_student)
    ele = mt.schedule_major_elective(base_student)
    assert req and all(c.category == "전공필수" for c in req)
    assert ele and all(c.category == "전공선택" for c in ele)
    sec_req = mt.schedule_major_required(base_student, second=True)
    sec_ele = mt.schedule_major_elective(base_student, second=True)
    assert sec_req and sec_ele


def test_schedule_general_education_and_bastion(base_student):
    for fname in ["GE_Common.json","GE_Natural.json","GE_Advanced.json","GE_Specialized.json"]:
        c = {"과목코드":fname,"학년":"0학년","이수구분":"교양","과목명":fname,"학점":3,"수업시간":"수 03"}
        Path(fname).write_text(json.dumps([c]), encoding="utf-8")
    Path("GE_BASTION.json").write_text(json.dumps([{"과목코드":"B0","학년":"0학년","이수구분":"특성","과목명":"B0","학점":3,"수업시간":"목 04"}]), encoding="utf-8")
    ge = mt.schedule_general_education(base_student)
    bast = mt.schedule_bastion(base_student)
    assert len(ge) == 4
    assert bast and bast[0].code == "B0"


def test_sum_credits_and_conflict():
    c1 = mt.Course({"과목코드":"X","학년":"0학년","이수구분":"","과목명":"","학점":2,"수업시간":"월 01"})
    c2 = mt.Course({"과목코드":"Y","학년":"0학년","이수구분":"","과목명":"","학점":3,"수업시간":"화 02"})
    assert mt.sum_credits([c1, c2]) == 5
    assert not mt.has_conflict(c1, [c2])

# ─── Main Function Tests ────────────────────────────

def test_main_excludes_taken_and_duplicates(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    student = {"학년":"2학년","이수학기":"1","전공":"천문학과","복수전공":"경영학과","교과적용년도":"2025","수강강의":["R1"]}
    for k in ["전공_필수","전공_선택","교양[최소:0/최대:0]_공통_기초"]: student[k] = 0
    for k in ["기준학점_전공_필수","기준학점_전공_선택","기준학점_교양[최소:0/최대:0]_공통_기초"]: student[k] = 3
    Path("student.json").write_text(json.dumps(student, ensure_ascii=False), encoding="utf-8-sig")
    majors = [
        {"과목코드":"P1","학년":"2학년","이수구분":"전공필수","과목명":"R1","학점":3,"수업시간":"월 01"},
        {"과목코드":"P1","학년":"2학년","이수구분":"전공선택","과목명":"R1","학점":3,"수업시간":"화 02"}
    ]
    Path("AS_25_1.json").write_text(json.dumps(majors), encoding="utf-8")
    Path("GE_Common.json").write_text(json.dumps([{"과목코드":"G0","학년":"0학년","이수구분":"교양","과목명":"G0","학점":3,"수업시간":"수 03"}]), encoding="utf-8")
    mt.main()
    out, _ = capsys.readouterr()
    assert "R1" not in out and "G0" in out


def test_main_full_schedule_range(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    student = {"학년":"2학년","이수학기":"1","전공":"천문학과","복수전공":"경영학과","교과적용년도":"2025","수강강의":[]}
    for k in ["전공_필수","전공_선택","교양[최소:0/최대:0]_공통_기초","교양[최소:0/최대:0]_자연_기초","교양[최소:0/최대:0]_심화","교양[최소:0/최대:0]_특성"]:
        student[k] = 0
    for k in ["기준학점_전공_필수","기준학점_전공_선택","기준학점_교양[최소:0/최대:0]_공통_기초","기준학점_교양[최소:0/최대:0]_자연_기초","기준학점_교양[최소:0/최대:0]_심화","기준학점_교양[최소:0/최대:0]_특성"]:
        student[k] = 6
    Path("student.json").write_text(json.dumps(student, ensure_ascii=False), encoding="utf-8-sig")
    majors = [
        {"과목코드":"P1","학년":"2학년","이수구분":"전공필수","과목명":"R1","학점":6,"수업시간":"월 01"},
        {"과목코드":"P2","학년":"2학년","이수구분":"전공선택","과목명":"E1","학점":6,"수업시간":"화 02"}
    ]
    Path("AS_25_1.json").write_text(json.dumps(majors), encoding="utf-8")
    for fname in ["GE_Common.json","GE_Natural.json","GE_Advanced.json","GE_Specialized.json"]:
        arr = [{"과목코드":fname,"학년":"0학년","이수구분":"교양","과목명":fname,"학점":6,"수업시간":"수 03"}]
        Path(fname).write_text(json.dumps(arr), encoding="utf-8")
    random.seed(42)
    mt.main()
    out, _ = capsys.readouterr()
    total = int(re.search(r"총 학점: (\d+)", out).group(1))
    assert 18 <= total <= 21

#추가

  # ─── 추가 커버리지 테스트 ───────────────────────────

def test_second_major_prefix_empty():
    data = {"학년":"1학년","이수학기":"2","전공":"철학과","복수전공":"","교과적용년도":"2025","수강강의":[]}
    stu = mt.Student(data)
    assert stu.second_major_prefix() == ""
    assert stu.second_major_filename() == ""

def test_schedule_bastion_file_not_found(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    data = {"학년":"1학년","이수학기":"1","전공":"컴퓨터공학과","복수전공":"","교과적용년도":"2025","수강강의":[]}
    stu = mt.Student(data)
    # GE_BASTION.json 파일이 없으면 빈 리스트를 반환해야 함
    assert mt.schedule_bastion(stu) == []

def test_schedule_general_education_no_need(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    data = {"학년":"1학년","이수학기":"1","전공":"컴퓨터공학과","복수전공":"","교과적용년도":"2025","수강강의":[]}
    # 교양 이미 기준학점 충족
    for k in ["교양[최소:0/최대:0]_공통_기초",
              "교양[최소:0/최대:0]_자연_기초",
              "교양[최소:0/최대:0]_심화",
              "교양[최소:0/최대:0]_특성"]:
        data[k] = "3"
        data[f"기준학점_{k}"] = "3"
    stu = mt.Student(data)
    # 교양 과목이 불필요하므로 빈 리스트
    assert mt.schedule_general_education(stu) == []

def test_main_only_major_elective(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    # 전공필수 충족, 전공선택만 필요
    student = {"학년":"2학년","이수학기":"1","전공":"컴퓨터공학과",
               "복수전공":"","교과적용년도":"2025","수강강의":[]}
    student["전공_필수"], student["기준학점_전공_필수"] = 3, 3
    student["전공_선택"], student["기준학점_전공_선택"] = 0, 3
    # 교양 불필요
    for k in ["교양[최소:0/최대:0]_공통_기초",
              "교양[최소:0/최대:0]_자연_기초",
              "교양[최소:0/최대:0]_심화",
              "교양[최소:0/최대:0]_특성"]:
        student[k] = 0; student[f"기준학점_{k}"] = 0
    Path("student.json").write_text(json.dumps(student, ensure_ascii=False), encoding="utf-8-sig")
    # 전공선택 과목 파일 생성
    elective = [{"과목코드":"E1","학년":"2학년",
                  "이수구분":"전공선택","과목명":"ELECTIVE",
                  "학점":3,"수업시간":"수 03"}]
    Path("CP_25_1.json").write_text(json.dumps(elective), encoding="utf-8")
    mt.main()
    out, _ = capsys.readouterr()
    assert "E1" in out and "ELECTIVE" in out

def test_main_only_bastion(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    # 전공필수·선택·교양 전부 충족 → BASTION만 필요
    student = {"학년":"2학년","이수학기":"1","전공":"컴퓨터공학과",
               "복수전공":"","교과적용년도":"2025","수강강의":[]}
    student["전공_필수"], student["기준학점_전공_필수"] = 3, 3
    student["전공_선택"], student["기준학점_전공_선택"] = 2, 2
    # 교양 전부 불필요
    for k in ["교양[최소:0/최대:0]_공통_기초",
              "교양[최소:0/최대:0]_자연_기초",
              "교양[최소:0/최대:0]_심화",
              "교양[최소:0/최대:0]_특성"]:
        student[k] = 0; student[f"기준학점_{k}"] = 0
    Path("student.json").write_text(json.dumps(student, ensure_ascii=False), encoding="utf-8-sig")
    # BASTION 파일 생성
    bastion = [{"과목코드":"B1","학년":"0학년",
                 "이수구분":"교양","과목명":"BASTION",
                 "학점":3,"수업시간":"금 04"}]
    Path("GE_BASTION.json").write_text(json.dumps(bastion), encoding="utf-8")
    mt.main()
    out, _ = capsys.readouterr()
    assert "B1" in out and "BASTION" in out
