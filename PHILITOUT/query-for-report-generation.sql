-- Simple:
-- 1. Display all female members who are 60 years old and above (senior citizen), order by age asc
SELECT Member_ID, Members_Name, Birthdate, Sex, TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS Age
FROM personal_details
WHERE Sex = 'F' AND TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) >= 60
ORDER BY Age ASC;

-- 2. Display all male members who are 60 years old and above (senior citizen), order by age asc
SELECT Member_ID, Members_Name, Birthdate, Sex, TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS Age
FROM personal_details
WHERE Sex = 'M' AND TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) >= 60
ORDER BY Age ASC;

-- 3. Display all members who are below 60 years old (not senior citizen), order by age asc
SELECT Member_ID, Members_Name, Birthdate, Sex, TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS Age
FROM personal_details
WHERE TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) < 60
ORDER BY Age ASC;

-- 4. Display all dependents who are 21 years old and below and are Filipino.  Order by name asc, age asc
SELECT Dependent_Name, Dependent_Birthdate, TIMESTAMPDIFF(YEAR, Dependent_Birthdate, CURDATE()) AS Age
FROM dependents_declaration
WHERE TIMESTAMPDIFF(YEAR, Dependent_Birthdate, CURDATE()) <= 21
AND Dependent_Citizenship = 'Filipino'
ORDER BY Dependent_Name ASC, Age ASC;

-- 5. Display all dependents who have disabilities, ordered by name
SELECT *
FROM dependents_declaration
WHERE Dependent_Disability = true
ORDER BY Dependent_Name ASC;

-- Moderate:
-- 1. Display all members' id, name, birthdate, and sex for those who are 60 years old and above and living in Manila
SELECT Member_ID, Members_Name, Birthdate, Sex, TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS Age
FROM personal_details
WHERE Permanent_Address LIKE '%Manila%'
GROUP BY Member_ID, Members_Name, Birthdate, Sex
HAVING Age >= 60;

-- 2. Display all members' id, name, birthdate, and sex for those who are 60 years old and above and living outside Manila
SELECT Member_ID, Members_Name, Birthdate, Sex, TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS Age
FROM personal_details
WHERE Permanent_Address NOT LIKE '%Manila%'
GROUP BY Member_ID, Members_Name, Birthdate, Sex
HAVING Age >= 60;

-- 3. Display the citizenship of dependents born before 2000 and count how many dependents are in that citizenship
SELECT Dependent_Citizenship, COUNT(Dependent_Citizenship) AS Dependent_Count
FROM dependents_declaration
WHERE YEAR(Dependent_Birthdate) < 2000
GROUP BY Dependent_Citizenship;

-- 4. Count Filipino dependents with disabilities and group by relationship type
SELECT Relationship, COUNT(*) AS Count_Disabled_Dependents
FROM Dependents_Declaration
WHERE Dependent_Disability = true AND Dependent_Citizenship = 'Filipino'
GROUP BY Relationship
ORDER BY Count_Disabled_Dependents DESC;

-- 5. Display sex then count how many members are there per sex
SELECT Sex, COUNT(Sex) AS Count_Sex
FROM personal_details
GROUP BY Sex;

-- Difficult:
-- 1. Display all records from all tables
SELECT *
FROM personal_details AS p, member_type AS m, dependents_declaration AS d
WHERE p.Member_ID = m.Member_ID = d.Member_ID;

-- 2. Count how many dependents are below 21 years old and display members' id and name with the result
SELECT p.Member_ID, Members_Name, COUNT(*) AS Dependents_Below21
FROM personal_details AS p, dependents_declaration AS d
WHERE p.Member_ID = d.Member_ID
AND TIMESTAMPDIFF(YEAR, Dependent_Birthdate, CURDATE()) < 21
GROUP BY p.Member_ID, Members_Name;

-- 3. Count how many dependents are 60 years old and above and display members' id and name with the result
SELECT p.Member_ID, Members_Name, COUNT(*) AS Senior_Dependents
FROM personal_details AS p, dependents_declaration AS d
WHERE p.Member_ID = d.Member_ID
AND TIMESTAMPDIFF(YEAR, Dependent_Birthdate, CURDATE()) >= 60
GROUP BY p.Member_ID, Members_Name;

-- 4. Display all members' id, name, birthdate, sex, and their dependents' name for those who are living in Manila
SELECT p.Member_ID, Members_Name, Birthdate, Sex, Dependent_Name
FROM personal_details AS p, dependents_declaration AS d
WHERE p.Member_ID = d.Member_ID
AND Permanent_Address LIKE '%Manila%'
GROUP BY Member_ID, Members_Name, Birthdate, Sex, Dependent_Name;

-- 5. Display members' id, name, and monthly income between 10000 and 50000
SELECT p.Member_ID, Members_Name, Monthly_Income
FROM personal_details AS p, member_type AS m
WHERE p.Member_ID = m.Member_ID
GROUP BY Member_ID, Members_Name, Monthly_Income
HAVING Monthly_Income BETWEEN 10000 AND 50000;
