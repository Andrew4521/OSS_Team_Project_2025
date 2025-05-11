#include <cstdlib> 
#include <iostream>
#include <fstream>
#include "Student.h"
#include <nlohmann/json.hpp>

int main() {
    // Python 스크립트를 실행하여 student.json 초기화 
    if (std::system("python scraper.py") != 0) {
        std::cerr << "Python 스크래핑 실패!" << std::endl;
        return 1;
    }

    // student.json 파일 열기
    std::ifstream ifs("student.json");


    // JSON 파싱
    nlohmann::json j;
    ifs >> j;

    // student 생성
    Student student(j);



    return 0;
}