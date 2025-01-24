CREATE DATABASE School;

USE School;

-- Table for storing student information
CREATE TABLE Students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    grade CHAR(1) NOT NULL,
    status VARCHAR(20) NOT NULL,
    contact VARCHAR(15),
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

-- Table for storing subjects
CREATE TABLE Subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL
);

-- Junction table for student-subject relationships
CREATE TABLE StudentSubjects (
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES Subjects(id) ON DELETE CASCADE,
    PRIMARY KEY (student_id, subject_id)
);