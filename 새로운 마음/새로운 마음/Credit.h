// Credit.h
#pragma once

#include <nlohmann/json.hpp>

// completed credit
class Cp_Credit {
public:
    // JSON 기반 생성자 선언
    explicit Cp_Credit(const nlohmann::json& j);

    // 멤버 접근자(getter) 선언
    int genEdCommonCore() const;
    int genEdNaturalCore() const;
    int genEdAdvanced() const;
    int genEdSpecialized() const;
    int majorCore() const;
    int majorElective() const;
    int secondMajor1Core() const;
    int secondMajor1Elective() const;
    int graduationCredits() const;

private:
    int GenEdCommonCore;     // 교양[최소:0/최대:0]_공통_기초
    int GenEdNaturalCore;    // 교양[최소:0/최대:0]_자연_기초
    int GenEdAdvanced;       // 교양[최소:0/최대:0]_심화
    int GenEdSpecialized;    // 교양[최소:0/최대:0]_특성
    int MajorCore;           // 전공_필수
    int MajorElective;       // 전공_선택
    int SecondMajor1Core;    // 다전공1_필수
    int SecondMajor1Elective;// 다전공1_선택
    int GraduationCredits;   // 졸업_이수_학점
};

// required credit
class Rq_Credit {
public:
    // JSON 기반 생성자 선언
    explicit Rq_Credit(const nlohmann::json& j);

    // 멤버 접근자(getter) 선언
    int genEdCommonCore() const;
    int genEdNaturalCore() const;
    int genEdAdvanced() const;
    int genEdSpecialized() const;
    int majorCore() const;
    int majorElective() const;
    int secondMajor1Core() const;
    int secondMajor1Elective() const;
    int graduationCredits() const;

private:
    int GenEdCommonCore;      // 기준학점_교양[최소:0/최대:0]_공통_기초
    int GenEdNaturalCore;     // 기준학점_교양[최소:0/최대:0]_자연_기초
    int GenEdAdvanced;        // 기준학점_교양[최소:0/최대:0]_심화
    int GenEdSpecialized;     // 기준학점_교양[최소:0/최대:0]_특성
    int MajorCore;            // 기준학점_전공_필수
    int MajorElective;        // 기준학점_전공_선택
    int SecondMajor1Core;     // 기준학점_다전공1_필수
    int SecondMajor1Elective; // 기준학점_다전공1_선택
    int GraduationCredits;    // 기준학점_졸업_이수_학점
};
