// Credit.cpp
#include "Credit.h"

// Cp_Credit 구현
Cp_Credit::Cp_Credit(const nlohmann::json& j)
    : GenEdCommonCore(j.value(u8"교양[최소:0/최대:0]_공통_기초", 0))
    , GenEdNaturalCore(j.value(u8"교양[최소:0/최대:0]_자연_기초", 0))
    , GenEdAdvanced(j.value(u8"교양[최소:0/최대:0]_심화", 0))
    , GenEdSpecialized(j.value(u8"교양[최소:0/최대:0]_특성", 0))
    , MajorCore(j.value(u8"전공_필수", 0))
    , MajorElective(j.value(u8"전공_선택", 0))
    , SecondMajor1Core(j.value(u8"다전공1_필수", 0))
    , SecondMajor1Elective(j.value(u8"다전공1_선택", 0))
    , GraduationCredits(j.value(u8"졸업_이수_학점", 0))
{
}

// 접근자
int Cp_Credit::genEdCommonCore()  const { return GenEdCommonCore; }
int Cp_Credit::genEdNaturalCore() const { return GenEdNaturalCore; }
int Cp_Credit::genEdAdvanced()     const { return GenEdAdvanced; }
int Cp_Credit::genEdSpecialized()  const { return GenEdSpecialized; }
int Cp_Credit::majorCore()         const { return MajorCore; }
int Cp_Credit::majorElective()     const { return MajorElective; }
int Cp_Credit::secondMajor1Core()  const { return SecondMajor1Core; }
int Cp_Credit::secondMajor1Elective() const { return SecondMajor1Elective; }
int Cp_Credit::graduationCredits() const { return GraduationCredits; }

// Rq_Credit 구현
Rq_Credit::Rq_Credit(const nlohmann::json& j)
    : GenEdCommonCore(j.value(u8"기준학점_교양[최소:0/최대:0]_공통_기초", 0))
    , GenEdNaturalCore(j.value(u8"기준학점_교양[최소:0/최대:0]_자연_기초", 0))
    , GenEdAdvanced(j.value(u8"기준학점_교양[최소:0/최대:0]_심화", 0))
    , GenEdSpecialized(j.value(u8"기준학점_교양[최소:0/최대:0]_특성", 0))
    , MajorCore(j.value(u8"기준학점_전공_필수", 0))
    , MajorElective(j.value(u8"기준학점_전공_선택", 0))
    , SecondMajor1Core(j.value(u8"기준학점_다전공1_필수", 0))
    , SecondMajor1Elective(j.value(u8"기준학점_다전공1_선택", 0))
    , GraduationCredits(j.value(u8"기준학점_졸업_이수_학점", 0))
{
}

// 접근자
int Rq_Credit::genEdCommonCore()  const { return GenEdCommonCore; }
int Rq_Credit::genEdNaturalCore() const { return GenEdNaturalCore; }
int Rq_Credit::genEdAdvanced()     const { return GenEdAdvanced; }
int Rq_Credit::genEdSpecialized()  const { return GenEdSpecialized; }
int Rq_Credit::majorCore()         const { return MajorCore; }
int Rq_Credit::majorElective()     const { return MajorElective; }
int Rq_Credit::secondMajor1Core()  const { return SecondMajor1Core; }
int Rq_Credit::secondMajor1Elective() const { return SecondMajor1Elective; }
int Rq_Credit::graduationCredits() const { return GraduationCredits; }
