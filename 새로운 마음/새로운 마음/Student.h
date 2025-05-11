// Student.h
#pragma once
#include <string>
#include "Credit.h"


class Student {
public:
    using Json = nlohmann::json;
    // JSON 객체로부터 completed/required credit을 초기화
    explicit Student(const Json& j);




public:
    Cp_Credit cp_credit;  // 이수 학점
    Rq_Credit rq_credit;  // 요구 학점
};
