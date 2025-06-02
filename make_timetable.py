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

