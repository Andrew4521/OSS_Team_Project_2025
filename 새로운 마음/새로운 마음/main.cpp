#include <cstdlib> 
#include <iostream>
#include <fstream>
#include "Student.h"
#include <nlohmann/json.hpp>

int main() {
    // Python ��ũ��Ʈ�� �����Ͽ� student.json �ʱ�ȭ 
    if (std::system("python scraper.py") != 0) {
        std::cerr << "Python ��ũ���� ����!" << std::endl;
        return 1;
    }

    // student.json ���� ����
    std::ifstream ifs("student.json");


    // JSON �Ľ�
    nlohmann::json j;
    ifs >> j;

    // student ����
    Student student(j);



    return 0;
}