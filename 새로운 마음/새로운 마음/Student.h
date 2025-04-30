#pragma once

#include <string>  

class Student {
public:    
    Student(const std::string& major, int minMaj, int maxMaj, int completedMaj, int minGenEd, int maxGenEd, int completedGenEd);
   

    const std::string& getMajor();                   // �а� 
    int getMinMajorCredits();                        // �ּ� ���� ���� 
    int getMaxMajorCredits();                        // �ִ� ���� ���� 
    int getCompletedMajorCredits();                  // ������ ���� ���� 
    int getMinGenEdCredits();                        // �ּ� ���� ���� 
    int getMaxGenEdCredits();                        // �ִ� ���� ���� 
    int getCompletedGenEdCredits();                  // ������ ���� ���� 



private:
    std::string major;                     // �а�
    std::string secondMajor;               // ���� ���� �а�
    int minMajorCredits;                   // �ּ� ���� ����
    int maxMajorCredits;                   // �ִ� ���� ����
    int completedMajorCredits;             // ������ ���� ����

    int minGenEdCredits;                   // �ּ� ���� ����
    int maxGenEdCredits;                   // �ִ� ���� ����
    int completedGenEdCredits;             // ������ ���� ����
};
