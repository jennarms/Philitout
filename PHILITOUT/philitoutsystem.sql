CREATE DATABASE philitoutsystem;
USE philitoutsystem;

CREATE TABLE Personal_Details (
    Member_ID VARCHAR(15) PRIMARY KEY,
    Members_Name VARCHAR(100),
    Mothers_MaidenName VARCHAR(100),
    SpouseName VARCHAR(100),
    Birthdate DATE,
    Birthplace VARCHAR(100),
    Sex CHAR(10),
    Civil_Status CHAR(20),
    Citizenship CHAR(20),
    Philsys_IDNum VARCHAR(25),
    TIN VARCHAR(25),
    Permanent_Address VARCHAR(300),
    Mailing_Address VARCHAR(300),
    Home_PhoneNum VARCHAR(25),
    Mobile_Number VARCHAR(25),
    Business_DL VARCHAR(15),
    Email_Address VARCHAR(50)
);

CREATE TABLE Dependents_Declaration (
    Dependent_ID VARCHAR(15) PRIMARY KEY,
    Member_ID VARCHAR(15),
    Dependent_Name VARCHAR(100),
    Relationship VARCHAR(25),
    Dependent_Birthdate DATE,
    Dependent_Citizenship VARCHAR(20),
    Dependent_Disability BOOLEAN,
    FOREIGN KEY (Member_ID) REFERENCES Personal_Details(Member_ID) ON DELETE CASCADE
);

CREATE TABLE Member_Type (
    Member_ID VARCHAR(15),
    Direct_Contributor VARCHAR(50),
    Indirect_Contributor VARCHAR(20),
    Profession VARCHAR(50),
    Monthly_Income DECIMAL(10, 2),
    Income_Proof VARCHAR(255),
    PRIMARY KEY (Member_ID),
    FOREIGN KEY (Member_ID) REFERENCES Personal_Details(Member_ID) ON DELETE CASCADE
);