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
        m = self.major
        if m == "컴퓨터공학과": return "CP_"
        if m == "천문학과":     return "AS_"
        if m == "철학과":       return "PH_"
        if m == "경영학과":     return "MA_"
        raise ValueError(f"지원하지 않는 전공(주전공): '{m}'")

def second_major_prefix(self):
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


