// Credit.cpp
#include "Credit.h"

// Cp_Credit ����
Cp_Credit::Cp_Credit(const nlohmann::json& j)
    : GenEdCommonCore(j.value(u8"����[�ּ�:0/�ִ�:0]_����_����", 0))
    , GenEdNaturalCore(j.value(u8"����[�ּ�:0/�ִ�:0]_�ڿ�_����", 0))
    , GenEdAdvanced(j.value(u8"����[�ּ�:0/�ִ�:0]_��ȭ", 0))
    , GenEdSpecialized(j.value(u8"����[�ּ�:0/�ִ�:0]_Ư��", 0))
    , MajorCore(j.value(u8"����_�ʼ�", 0))
    , MajorElective(j.value(u8"����_����", 0))
    , SecondMajor1Core(j.value(u8"������1_�ʼ�", 0))
    , SecondMajor1Elective(j.value(u8"������1_����", 0))
    , GraduationCredits(j.value(u8"����_�̼�_����", 0))
{
}

// ������
int Cp_Credit::genEdCommonCore()  const { return GenEdCommonCore; }
int Cp_Credit::genEdNaturalCore() const { return GenEdNaturalCore; }
int Cp_Credit::genEdAdvanced()     const { return GenEdAdvanced; }
int Cp_Credit::genEdSpecialized()  const { return GenEdSpecialized; }
int Cp_Credit::majorCore()         const { return MajorCore; }
int Cp_Credit::majorElective()     const { return MajorElective; }
int Cp_Credit::secondMajor1Core()  const { return SecondMajor1Core; }
int Cp_Credit::secondMajor1Elective() const { return SecondMajor1Elective; }
int Cp_Credit::graduationCredits() const { return GraduationCredits; }

// Rq_Credit ����
Rq_Credit::Rq_Credit(const nlohmann::json& j)
    : GenEdCommonCore(j.value(u8"��������_����[�ּ�:0/�ִ�:0]_����_����", 0))
    , GenEdNaturalCore(j.value(u8"��������_����[�ּ�:0/�ִ�:0]_�ڿ�_����", 0))
    , GenEdAdvanced(j.value(u8"��������_����[�ּ�:0/�ִ�:0]_��ȭ", 0))
    , GenEdSpecialized(j.value(u8"��������_����[�ּ�:0/�ִ�:0]_Ư��", 0))
    , MajorCore(j.value(u8"��������_����_�ʼ�", 0))
    , MajorElective(j.value(u8"��������_����_����", 0))
    , SecondMajor1Core(j.value(u8"��������_������1_�ʼ�", 0))
    , SecondMajor1Elective(j.value(u8"��������_������1_����", 0))
    , GraduationCredits(j.value(u8"��������_����_�̼�_����", 0))
{
}

// ������
int Rq_Credit::genEdCommonCore()  const { return GenEdCommonCore; }
int Rq_Credit::genEdNaturalCore() const { return GenEdNaturalCore; }
int Rq_Credit::genEdAdvanced()     const { return GenEdAdvanced; }
int Rq_Credit::genEdSpecialized()  const { return GenEdSpecialized; }
int Rq_Credit::majorCore()         const { return MajorCore; }
int Rq_Credit::majorElective()     const { return MajorElective; }
int Rq_Credit::secondMajor1Core()  const { return SecondMajor1Core; }
int Rq_Credit::secondMajor1Elective() const { return SecondMajor1Elective; }
int Rq_Credit::graduationCredits() const { return GraduationCredits; }
