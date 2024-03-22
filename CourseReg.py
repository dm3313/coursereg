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
    def __init__(self, studentName, major):
        self.studentName = studentName
        self.studentCourses = set()
        self.studentComplete = set()
        self.major = major
        
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
    def __init__(self, name, seatAvail, prereq):
        self.name = name
        self.seatAvail = seatAvail
        # We also want a set of the students in the course
        # This is not a parameter of the constructor, though, because it starts empty
        # and must be added to
        self.studentSet = set()
        self.prereq = prereq
        
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
    
    # Method for adding a student to a course
    def addCourse(self, student):
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
        self.EEmajorCourses = ['EECE2140']
    
    def EECheck(self, course):
        check = False
        if course.name in self.EEmajorCourses:
            check = True
        return(check)
    
    def EEregister(self, course, student):
        if self.EECheck(course):
            course.addCourse(student)
        else: print("Error: this course is not in your major.")
        
class CSMajor(Major):
    def __init__(self):
        self.CSmajorCourses = ['CS1242']
        
    def CSCheck(self, course):
        check = False
        if course.name in self.CSmajorCourses:
            check = True
        return(check)
    
    def CSregister(self, course, student):
        if self.CSCheck(course):
            course.addCourse(student)
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
    # Info
    # This is how you would use this program when there was a user interface
    courseFormatted = """
    Welcome to registration! Here are the courses offered for this semester:
        MATH1241: Calculus 1
        MATH1242: Calculus 2
        ENG1111: First Year Writing
        PHYS1151: Physics 1
        
    To register, type the name of the course with no spaces!
    EXAMPLE: MATH1241
    --> To complete registration, type "Done"
    --> To view your current registered courses, type "My Courses"
    --> To view the students currently registered for a course, type "Students"
    --> To drop a course, type "Drop"
    --> To add a course you've already taken, type "Taken"
    --> To view your already taken courses, type "Print Taken"
    """
    
    
    # Define course objects
    EEmajorObj = EEMajor()
    EECSmajorObj = EECSMajor()
    sampleStudent = Student('Devin',EEmajorObj)
    math1120 = Course('MATH1120', 4, '')
    math1241 = Course('MATH1241',6, 'MATH1120')
    math1242 = Course('MATH1242',4,'MATH1241')
    eece2140 = Course('EECE2140', 3, '')
    phys1151 = Course('PHYS1151', 2, 'MATH1241')
    cs1242 = Course('CS1242',4,'')
    # Define list of courses -- will be used for iteration later
    
    
    # Test 1
    print("Test 1:")
    print("An EE major registers for EECE2140")
    print("System Output:")
    testStudent1 = Student('Devin',EEmajorObj)
    EEmajorObj.EEregister(eece2140,testStudent1)
    current = testStudent1.printStudentCourses()
    print(current)
    print("")
    
    print("Test 2:")
    print("An EECS major registers for CS2142")
    print("System Output:")
    testStudent1 = Student('Devin',EECSmajorObj)
    EECSmajorObj.register(cs1242,testStudent1)
    current = testStudent1.printStudentCourses()
    print(current)
    print("")
    
    
    # Test 5
    print("Test 5:")
    print("Student tries to register for MATH1242 without having taken MATH1241")
    print("System Output:")
    testStudent5 = Student('Devin',EEmajorObj)
    # Using math1241 and math1242
    math1242.addCourse(testStudent5)
    
    
    
main()