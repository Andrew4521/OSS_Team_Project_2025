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

