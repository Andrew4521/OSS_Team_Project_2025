#include <iostream>
#include "Student.h"
#include <fstream>
#include <nlohmann/json.hpp>
#include <windows.h>



using json = nlohmann::json;

int main() {
    // 받아온 데이터 파일 열기
    std::ifstream in("student.json");
    if (!in.is_open()) {
        std::cerr << "student.json 파일을 열 수 없습니다.\n";
        return 1;
    }

    json j;
    in >> j; 

  // 받아온 데이터로 초기화
    Student student(
        j.at("major").get<std::string>(),
        j.at("minMajor").get<int>(),
        j.at("maxMajor").get<int>(),
        j.at("completedMajor").get<int>(),
        j.at("minGenEd").get<int>(),
        j.at("maxGenEd").get<int>(),
        j.at("completedGenEd").get<int>()
    );

    SetConsoleOutputCP(CP_UTF8);
    std::ios::sync_with_stdio(false);

    std::cout << student.getMajor() << std::endl;

    return 0;
}