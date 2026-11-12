CREATE TABLE students (
student_id SERIAL PRIMARY KEY,
name VARCHAR(50) NOT NULL,
age INT CHECK(age>=18),
dept_id INT
);
CREATE TABLE departments(
dept_id SERIAL PRIMARY KEY,
dept_name VARCHAR(50) UNIQUE NOT NULL
);
INSERT INTO departments (dept_name)
VALUES
('Geoinformatics'),
('Computer Science'),
('Remote Sensing'),
('Geography'),
('Environmental Science');
INSERT INTO students (name, age, dept_id)
VALUES
('Arun', 22, 1),
('Priya', 24, 2),
('Karthik', 21, 3),
('Divya', 23, 2),
('Rahul', 20, 1),
('Sneha', 25, 4),
('Vijay', 22, 2);
SELECT name, age
FROM students
ORDER BY age DESC;

SELECT name
FROM students
WHERE age > 21 AND dept_id = 2;

SELECT students.name, departments.dept_name
FROM students
INNER JOIN departments
ON students.dept_id = departments.dept_id;

SELECT AVG(age) AS average_age
FROM students;

SELECT dept_id, COUNT(*) AS student_count
FROM students
GROUP BY dept_id;

SELECT dept_id, COUNT(*) AS student_count
FROM students
GROUP BY dept_id
HAVING COUNT(*) > 2;

SELECT departments.dept_name,
       COUNT(students.student_id) AS total_students
FROM departments
LEFT JOIN students
ON departments.dept_id = students.dept_id
GROUP BY departments.dept_name;

UPDATE students
SET age = 25
WHERE name = 'Arun';

DELETE FROM students
WHERE student_id = 5;

CREATE VIEW student_view AS
SELECT students.student_id,
       students.name,
       departments.dept_name,
       students.age
FROM students
INNER JOIN departments
ON students.dept_id = departments.dept_id;

SELECT *
FROM student_view
WHERE age > 22;
