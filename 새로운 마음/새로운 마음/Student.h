#pragma once

#include <string>  

class Student {
public:    
    Student(const std::string& major, int minMaj, int maxMaj, int completedMaj, int minGenEd, int maxGenEd, int completedGenEd);
   

    const std::string& getMajor();                   // 학과 
    int getMinMajorCredits();                        // 최소 전공 학점 
    int getMaxMajorCredits();                        // 최대 전공 학점 
    int getCompletedMajorCredits();                  // 수강한 전공 학점 
    int getMinGenEdCredits();                        // 최소 교양 학점 
    int getMaxGenEdCredits();                        // 최대 교양 학점 
    int getCompletedGenEdCredits();                  // 수강한 교양 학점 



private:
    std::string major;                     // 학과
    std::string secondMajor;               // 복수 전공 학과
    int minMajorCredits;                   // 최소 전공 학점
    int maxMajorCredits;                   // 최대 전공 학점
    int completedMajorCredits;             // 수강한 전공 학점

    int minGenEdCredits;                   // 최소 교양 학점
    int maxGenEdCredits;                   // 최대 교양 학점
    int completedGenEdCredits;             // 수강한 교양 학점
};
