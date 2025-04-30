#include "Student.h"

Student::Student(const std::string& major,
    int minMaj, int maxMaj, int completedMaj,
    int minGenEd, int maxGenEd, int completedGenEd)
    : major(major)
    , minMajorCredits(minMaj)
    , maxMajorCredits(maxMaj)
    , completedMajorCredits(completedMaj)
    , minGenEdCredits(minGenEd)
    , maxGenEdCredits(maxGenEd)
    , completedGenEdCredits(completedGenEd)
{
}

const std::string& Student::getMajor() {
    return major;
}


int Student::getMinMajorCredits() {
    return minMajorCredits;
}

int Student::getMaxMajorCredits() {
    return maxMajorCredits;
}

int Student::getCompletedMajorCredits() {
    return completedMajorCredits;
}

int Student::getMinGenEdCredits() {
    return minGenEdCredits;
}

int Student::getMaxGenEdCredits() {
    return maxGenEdCredits;
}

int Student::getCompletedGenEdCredits() {
    return completedGenEdCredits;
}
