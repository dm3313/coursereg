#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 12:03:59 2024

@author: devin
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 21:32:21 2024

@author: devin
"""

# Student class - contains all methods pertaining to the student using the program


class Student:
    # Constructor for student class
    # Takes in the name of the student
    # Every student has no courses enrolled or completed at first, so this must be filled later
    def __init__(self, studentName, major, total_credits):
        self.studentName = studentName
        self.studentCourses = set()
        self.studentComplete = set()
        self.major = major
        self.total_credits = total_credits
        
    # Method for checking if a student has registered already
    def inCourse(self, courseObject):
        # Initially, a student is assumed not to be in a course
        inCourse = False
        # If the student is in the student set in the course object
        if self in courseObject.studentSet:
            # Then the student is in the course
            inCourse = True
        # Return finding
        return(inCourse)
    
    # Method for adding to a set of a student's courses
    def addToStudentCourses(self, course):
        self.studentCourses.add(course)

    # Method for printing the student courses set
    def printStudentCourses(self):
        # If student has currently not registered for any courses
        if len(self.studentCourses) == 0:
            # Print that
            courses = "You have no courses"
        else: 
            courses = "Your current courses are: "
            # Else, iterate over the student courses set and print it in a string
            for course in self.studentCourses:
                courses += course.name + " "
        # Return the string
        return(courses)
    
    # Method for dropping a class from a student's schedule
    def removeStudentCourses(self, course):
        self.studentCourses.remove(course)
    
    # Method for adding a course to the student's list of already completed courses
    def studentComp(self, course):
        if self.inCourse(course):
            print("You are registered for this course currently. If you have already taken it, please drop the course")
        else:
            self.studentComplete.add(course)
        
    # Method for printing the courses a student has already taken
    def takenAlr(self):
        taken = "You have taken: "
        # Iterate over the student's completed courses list
        for course in self.studentComplete:
            # Since we add the entire course object to this list, we must 
            # Only print the course name 
            taken += course.name + " "
        return(taken)

# Course class
class Course:
    # Initialized with the name of the course, seats available, and any prerequisites
    def __init__(self, name, seatAvail, prereq, start, end):
        self.name = name
        self.seatAvail = seatAvail
        # We also want a set of the students in the course
        # This is not a parameter of the constructor, though, because it starts empty
        # and must be added to
        self.studentSet = set()
        self.prereq = prereq
        self.start = start
        self.end = end
        
    # Method for determining if a student has completed the prereqs
    def goForward(self, student):
        # Initially, we assume they have not
        goForward = False
        # Iterate over the student's completed courses
        for course in student.studentComplete:
            # If the course name matches the course prerequisite
            if course.name == self.prereq:
                # Allow registration to go forward
                goForward = True
        if self.prereq == '':
            goForward = True
        # Return go forward
        return(goForward)
    
    # Method for determining if a students classes overlap with the student's class.
    def doCoursesOverlap(self, student):
        for course in student.studentCourses:
            if (self.start >= course.start and self.start < course.end) or (self.end > course.start and self.end <= course.end):
                return True
            else:
                return False
    
    # Method for adding a student to a course
    def addCourse(self, student, type_course):
        # If student is already in the course
        if student.inCourse(self):
            # Print that
            print(f"{student.studentName} is already in {self.name}")
        # If no seats are left
        elif self.seatAvail == 0:
            # Print that
            print(f"{self.name} is full! Please register for another course")
        # If the course has already been completed
        elif self in student.studentComplete:
            # Print that
            print("You've taken this class already. Please try again")
        # If the courses overlap
        elif self.doCoursesOverlap(student):
            # Print that
            print("This class overlaps with one of yours. Please try again")
        # If credits exceeded
        elif (type_course == "major" and student.total_credits > 12):
            # Print that
            print("You cannot exceed 16 credits. Please try again")
        elif (type_course == "elective" and student.total_credits > 14):
            # Print that
            print("You cannot exceed 16 credits. Please try again")
        else:
            # Run go forward method for the given student
            # If true, run the below commands
            if self.goForward(student):
                # Add student to the course's student set
                self.studentSet.add(student)
                # Decrease the available seats by 1
                self.seatAvail -= 1
                # Add this course to the student's courses
                student.addToStudentCourses(self)
                # Update credits
                if type_course == "major":
                    student.total_credits += 4
                else:
                    student.total_credits += 2
                # Print a success message
                print("Success!")
            # Else, throw error--the student needs to take the prereq
            else:
                print(f"You must take the prereq for this course, {self.prereq}")

    
    # Method for printing the list of students in a given course
    def printStudents(self):
        # Will not iterate if there is no students in the class
        if len(self.studentSet) == 0:
            students = "There are no students in this course"
        else: 
            students = "The students in the course are: "
            # Iterate over the students in the student set
            for student in self.studentSet:
                # Add their names to a string
                students += student.studentName + " "
        # Return the string
        return(students)
    
    # Method for dropping a student from a course
    def dropCourse(self, student):
        # If the in course method returns true (i.e., a student is in the course passed)
        if student.inCourse(self):
            # Remove the student object from the student set
            self.studentSet.remove(student)
            # Drop the seat availability by 1
            self.seatAvail += 1
            # Calls the method in student class to remove this course from the student's courses
            student.removeStudentCourses(self)
        # Else, deny the student from dropping the course
        else:
            print("You cannot remove yourself from a class you are not in")
            

class Major:
    def __init__(self):
        self.core_course=[]
        self.Elective_course=[]

class EEMajor(Major):
    def __init__(self):
        self.EEmajorCourses = ['EECE2140','EECE2150','EECE2160']
        self.EEelectives = ['EECE3140']
    
    def EECheck(self, course):
        check = False
        if course.name in self.EEmajorCourses or course.name in self.EEelectives:
            check = True
        return(check)
    
    def isMajor(self, course):
        if course.name in self.EEmajorCourses:
            return True
        else:
           return False
    
    def EEregister(self, course, student):
        if self.EECheck(course) and self.isMajor(course):
            course.addCourse(student, "major")
        elif self.EECheck(course) and (not self.isMajor(course)):
            course.addCourse(student, "elective")
        else: print("Error: this course is not in your major.")
        
class CSMajor(Major):
    def __init__(self):
        self.CSmajorCourses = ['CS1242','CS1243','CS1244','CS1245','CS1246']
        self.CSElectives = ['CS2242','EECE2140']
        
    def CSCheck(self, course):
        check = False
        if course.name in self.CSmajorCourses or course.name in self.CSElectives:
            check = True
        return(check)
    
    def isMajor(self, course):
        if course.name in self.CSmajorCourses:
            return True
        else:
           return False
    
    def CSregister(self, course, student):
        if self.CSCheck(course) and self.isMajor(course):
            course.addCourse(student, "major")
        elif self.CSCheck(course) and (not self.isMajor(course)):
            course.addCourse(student, "elective")
        else: print("Error: this course is not in your major.")
        
class EECSMajor(EEMajor,CSMajor):
    def __init__(self):
        EEMajor.__init__(self)
        CSMajor.__init__(self)
    
    def register(self, course, student):
        if self.EECheck(course):
            self.EEregister(course,student)
        elif self.CSCheck(course):
            self.CSregister(course,student)
        else: print("Error: this course is not in your major.")



def main():
    # Define course 
    CSmajorObj = CSMajor()
    EEmajorObj = EEMajor()
    EECSmajorObj = EECSMajor()
    math1241 = Course('MATH1241',6, 'MATH1120', 2, 4)
    math1242 = Course('MATH1242',4,'MATH1241', 4, 6)
    eece2140 = Course('EECE2140', 3, '', 6, 8)
    cs1242 = Course('CS1242',4,'', 10, 12)
    cs1243 = Course('CS1243',4,'', 0, 2)
    cs1244 = Course('CS1244',4,'', 2, 4)
    cs1245 = Course('CS1245',4,'', 4,6)
    cs1246 = Course('CS1246',4,'', 6,8)
    cs2242 = Course('CS2242',4,'', 11,12)
    
    
    # Test 1
    print("Test 1:")
    print("An EE major registers for EECE2140")
    print("System Output:")
    testStudent1 = Student('Devin',EEmajorObj,0)
    EEmajorObj.EEregister(eece2140,testStudent1)
    current = testStudent1.printStudentCourses()
    print(current)
    print("")
    
    #Test 2
    print("Test 2:")
    print("An EECS major registers for CS1242")
    print("System Output:")
    testStudent1 = Student('Devin',EECSmajorObj,0)
    EECSmajorObj.register(cs1242,testStudent1)
    current = testStudent1.printStudentCourses()
    print(current)
    print("")
    
    #Test 3
    print("Test 3:")
    print("A CS major registers for CS2242 (elective class)")
    print("Elective classes are only 2 credits in our system")
    print("System Output:")
    testStudent2 = Student('Ashnu',CSmajorObj,0)
    CSmajorObj.CSregister(cs2242,testStudent2)
    current = testStudent2.printStudentCourses()
    print(f"Your total credits are: {testStudent2.total_credits}")
    print(current)
    print("")
    
    #Test 4
    print("Test 4:")
    print("A CS major tries to register for CS1242 and CS2242 (overlap)")
    print("System Output:")
    testStudent3 = Student('Jon',CSmajorObj,0)
    CSmajorObj.CSregister(cs1242,testStudent3)
    CSmajorObj.CSregister(cs2242,testStudent3)
    current = testStudent3.printStudentCourses()
    print(current)
    print("")
    
    # Test 5
    print("Test 5:")
    print("Student tries to register for MATH1242 without having taken MATH1241")
    print("System Output:")
    testStudent5 = Student('Devin',EEmajorObj,0)
    # Using math1241 and math1242
    math1242.addCourse(testStudent5, "major")
    print("")
    
    # Test 6
    print("Test 6:")
    print("Student tries to register for too many credits (over 16)")
    print("System Output:")
    testStudent6 = Student('Devin',CSmajorObj,0)
    CSmajorObj.CSregister(cs1242,testStudent6)
    CSmajorObj.CSregister(cs1243,testStudent6)
    CSmajorObj.CSregister(cs1244,testStudent6)
    CSmajorObj.CSregister(cs1245,testStudent6)
    CSmajorObj.CSregister(cs1246,testStudent6)
    current = testStudent6.printStudentCourses()
    print(current)
    print("")
    
    print("Test 7")
    print("Two students register for EECE2140. For one, it is elective.")
    print("For the other, it is a major course.")
    testStudent7 = Student('Ashnu', EEmajorObj,0)
    testStudent8 = Student('Ben',CSmajorObj,0)
    print("System Output: EECE2140 for an EE Major (MAJOR class)")
    EEmajorObj.EEregister(eece2140,testStudent7)
    current = testStudent7.printStudentCourses()
    print(current)
    print(f"Your total credits are: {testStudent7.total_credits}")
    print("System Output: EECE2140 for a CS Major (ELECTIVE class)")
    CSmajorObj.CSregister(eece2140,testStudent8)
    current2 = testStudent8.printStudentCourses()
    print(current2)
    print(f"Your total credits are: {testStudent8.total_credits}")



main()