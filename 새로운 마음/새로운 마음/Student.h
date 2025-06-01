// Student.h
#pragma once
#include <string>
#include "Credit.h"


class Student {
public:
    using Json = nlohmann::json;
    // JSON ��ü�κ��� completed/required credit�� �ʱ�ȭ
    explicit Student(const Json& j);




public:
    Cp_Credit cp_credit;  // �̼� ����
    Rq_Credit rq_credit;  // �䱸 ����
};
