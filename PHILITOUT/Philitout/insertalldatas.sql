USE philitoutsystem;

INSERT INTO Personal_Details (
    Member_ID, Members_Name, Mothers_MaidenName, SpouseName, Birthdate, Birthplace, Sex, Civil_Status, Citizenship, Philsys_IDNum, TIN, Permanent_Address, Mailing_Address, Home_PhoneNum, Mobile_Number, Business_DL, Email_Address
) VALUES
('PH001', 'Dela Cruz, Juan Ponce', 'Garcia, Luzviminda Mendoza', NULL, '1947-05-15', 'Tondo, Manila', 'M', 'S', 'F', '1234-5678-8765-4321', '209-143-304', '123 Rizal St., Quezon City', '456 Bonifacio Ave., Makati', '(02) 123-4567', '0917-123-4567', NULL, 'juan.delacruz@gmail.com'),
('PH002', 'Lopez, Ana Natividad', 'Natividad, Yolanda Santos', 'Lopez, Nathaniel Sta. Maria', '1985-07-22', 'Cebu City, Cebu', 'F', 'M', 'F', '2345-6789-0123-0021', '876-543-210', '789 Mabini St., Cebu City, Cebu', '789 Mabini St., Cebu City, Cebu', '(02) 234-5678', '0928-234-5678', 'B2345678', 'ana.lopez@gmail.com'),
('PH003', 'Reyes, Michael Cruz', 'Aquino, Regina Diaz', 'Reyes, Clarissa Dela Cruz', '1971-10-05', 'Davao City, Davao del Sur', 'M', 'M', 'F', '3456-7890-1234-4567', '765-432-109', '654 Del Pilar St., Davao City, Davao del Sur', '987 Bonifacio Dr., Iloilo City, Iloilo', '(082) 345-6789', '0939-345-6789', NULL, 'michael.reyes@gmail.com'),
('PH004', 'Cruz, Erlinda Tolentino', 'Reyes, Imelda Salazar', 'Cruz, Francisco Rodriguez', '1949-08-04', 'Calbayog, Western Samar', 'F', 'M', 'F', '4567-8901-2345-6789', '654-321-098', '321 Rizal St., Quezon City', '321 Rizal St., Quezon City', NULL, '0947-456-7890', NULL, 'erlinda.cruz@gmail.com'),
('PH005', 'Santos, John Villanueva', 'Dela Rosa, Marissa Perez', 'Santos, Lucianna Mendoza', '1982-09-15', 'Iloilo City, Iloilo', 'M', 'M', 'F', '5678-9012-3456-7890', '543-210-987', '591 Teresa St., Sta. Mesa, Manila', '591 Teresa St., Sta. Mesa, Manila', NULL, '0958-567-8901', NULL, 'john.santos@gmail.com'),
('PH006', 'Hernandez, Janelle Garcia', 'Bautista, Rosario Santiago', NULL, '1955-11-10', 'Baguio City, Benguet', 'F', 'LS', 'F', NULL, '432-109-876', '789 Rizal Ave., Tagaytay, Cavite', '789 Rizal Ave., Tagaytay, Cavite', NULL, '0968-567-8902', NULL, 'janelle.hernandez@gmail.com'),
('PH007', 'Gutierrez, Lourdes Simon', 'Torres, Cristina Rivera', 'Gutierrez, Manuel Peralta', '1948-04-22', 'Vigan City, Ilocos Sur', 'F', 'W', 'F', NULL, NULL, '456 Mabini Ave., Laoag City, Ilocos Norte', '456 Mabini Ave., Laoag City, Ilocos Norte', NULL, '0978-678-9012', NULL, 'lourdes.gutierrez@gmail.com'),
('PH008', 'Romualdez, Cristy', 'Aguilar, Josefina Aquino', 'Romualdez, John Dale', '1990-09-09', 'Romblon, Romblon', 'F', 'LS', 'F', '5239-0912-6253-9027', '200-012-893', 'Roxas St., Brgy. 2, Romblon, Romblon, Philippines, 5500', 'Roxas St., Brgy. 2, Romblon, Romblon, Philippines, 5500', '(042) 123-4565', '0956-299-6035', NULL, 'cristyromualdez23@gmail.com'),
('PH009', 'Villafranca, Joshua', 'Morales, Juanita Mindo', 'Villafranca, Rica Mae', '2000-12-16', 'Bacoor City, Cavite', 'M', 'LS', 'F', '8921-8291-9027-6127', '560-250-890', '2nd Floor, SM City Bacoor, Block 1, Barangay Habay I, Bacoor City, Cavite, Philippines, 4102', '2nd Floor, SM City Bacoor, Block 1, Barangay Habay I, Bacoor City, Cavite, Philippines, 4102', '(046) 123-4567', '0912-345-6789', NULL, 'joshuav@gmail.com'),
('PH010', 'Zamora, Omar', 'Santiago, Myrna Corazon', 'Zamora, Claire', '1979-08-03', 'San Fernando City, La Union', 'M', 'W', 'DC', '1326-8927-9735-9617', '350-867-901', 'Room 301, San Fernando Building, Lot 10, Barangay Catbangen, San Fernando City, La Union, Philippines, 2500', 'Room 301, San Fernando Building, Lot 10, Barangay Catbangen, San Fernando City, La Union, Philippines, 2500', '(072) 234-5678', '0977-654-3210', NULL, 'zmar@gmail.com'),
('PH011', 'Zaragosa, Clarissa', 'Josol, Analiza Guilas', NULL, '1988-06-01', 'Legazpi City, Albay', 'F', 'A', 'DC', '1232-8910-9017-9254', '456-123-543', 'Landco Business Park, Barangay Capantawan, Legazpi City, Albay, Philippines, 4500', 'Landco Business Park, Barangay Capantawan, Legazpi City, Albay, Philippines, 4500', '(052) 345-6789', '0921-987-6543', '(052) 123-5531', 'clarissazara@gmail.com'),
('PH012', 'Smith, John Michael', 'Johnson, Laura Marie', NULL, '1999-01-01', 'Portland, Oregon', 'M', 'S', 'FN', NULL, NULL, 'The Addison Apartments, 123 NW 25th Ave, Neighborhood Alphabet District, Portland, Oregon, USA, 97210', 'Block 5, Lot 8, Phase 2, Maharlika Village, Taguig City, Metro Manila', '(503) 555-1234', '0971-345-6789', NULL, 'smithjohn21@gmail.com'),
('PH013', 'Flores, Joshua Jr. Fernandez', 'Fernandez, Maria Teresa Lopez', 'Fernandez, Maria Clara Cruz', '1985-04-15', 'Manila, Philippines', 'M', 'M', 'F', NULL, '895-135-312', 'Unit 101, Sunshine Residences, Lot 15, Sunflower St., Bloomfield Subdivision, Barangay San Isidro, Lipa City, Batangas, 4217', 'Unit 501, Skyline Residences, Block 10, Moonlight St., Celestial Subdivision, Barangay Malinta, Valenzuela City, Metro Manila, 1440', NULL, '0913-210-9876', NULL, 'joshuafernandezjr@gmail.com'),
('PH014', 'Garcia, Pedro III. Rodriguez', 'Rodriguez, Ana Isabel Cruz', NULL, '1978-06-23', 'Riyadh, Al Nisr', 'M', 'S', 'DC', '3246-4546-1232-4364', '569-316-659', 'Unit 201, Royal Towers, Block 3, Ruby St., Diamond Subdivision, Barangay San Antonio, Makati City, Metro Manila, 1200', 'Unit 201, Royal Towers, Block 3, Ruby St., Diamond Subdivision, Barangay San Antonio, Makati City, Metro Manila, 1200', NULL, '0925-678-1234', NULL, 'pedrorodrigueziii@yahoo.com'),
('PH015', 'De la Cruz, Vincent Jr. Santos', 'Santos, Elena Maria Reyes', 'Santos, Angela Maria Diaz', '1990-12-05', 'Davao City, Philippines', 'M', 'W', 'F', NULL, '659-411-754', 'Floor 4, Silver Plaza, Phase 2, Topaz St., Crystal Subdivision, Barangay Talon, Las Piñas City, Metro Manila, 1740', 'Floor 4, Silver Plaza, Phase 2, Topaz St., Crystal Subdivision, Barangay Talon, Las Piñas City, Metro Manila, 1740', NULL, '0930-987-6541', '+63 2 9876-5432', 'vincentjsantosjr@hotmail.com'),
('PH016', 'Santos, Desiree Sr. Lopez', 'Lopez, Carmen Julia Martinez', NULL, '1982-03-12', 'Singapore City, Marina Bay', 'F', 'LS', 'DC', NULL, '987-653-261', 'Unit A-1, Grandview Heights, Lot 8, Oak St., Greenfields Subdivision, Barangay Poblacion, Pasig City, Metro Manila, 1600', 'Unit A-1, Grandview Heights, Lot 8, Oak St., Greenfields Subdivision, Barangay Poblacion, Pasig City, Metro Manila, 1600', '(+63) 2 8765-4321', '0941-234-5678', NULL, 'desireelopezsr@outlook.com'),
('PH017', 'Reyes, Lana Marie Bautista', 'Bautista, Patricia Ann Garcia', 'Bautista, Miguel Antonio Reyes', '1995-09-30', 'Bacolod City, Philippines', 'F', 'M', 'F', '6965-9896-6561-5623', '133-897-133', 'Room B-2, Hillview Towers, Block 7, Pine St., Pinecrest Subdivision, Barangay Poblacion, Cainta, Rizal, 1900', 'Unit 302, Horizon Towers, Block 6, Sunrise St., Vista Verde Subdivision, Barangay Bagumbayan, Taguig City, Metro Manila, 1630', NULL, '0950-876-5432', NULL, 'lanareyesbautista@example.com'),
('PH018', 'Dela Cruz, Roberto Roxas', 'Roxas, Genenive', 'Dela Cruz, Pamela Quinto', '1960-12-16', 'Manila, Philippines', 'M', 'M', 'F', '1111-2222-3333-4444', '123-456-789', 'Unit 301, Sunrise Towers, Lot 15, Acacia Street, Greenfields Subdivision, Barangay Poblacion, Pasig City, Metro Manila, Philippines, 1600', 'Unit 301, Sunrise Towers, Lot 15, Acacia Street, Greenfields Subdivision, Barangay Poblacion, Pasig City, Metro Manila, Philippines, 1600', '+63(08)8123-4567', '+639123456789', '1239-6734', 'roberto21@gmail.com'),
('PH019', 'Chua, Daniela Machon', 'Machon, Pearl Joy', NULL, '1996-03-05', 'Toronto, Canada', 'F', 'S', 'DC', '1212-3434-5656-7878', '112-233-445', 'Room 102, Emerald Residences, Block 5, Ruby Street, Rosewood Subdivision, Barangay Malinta, Valenzuela City, Metro Manila, Philippines, 1440', 'Room 102, Emerald Residences, Block 5, Ruby Street, Rosewood Subdivision, Barangay Malinta, Valenzuela City, Metro Manila, Philippines, 1440', '+63(08)1267-2222', '+639246813579', '7832-8940', 'danielachua@gmail.com'),
('PH020', 'Smith, Joe Johnson', 'Johnson, Mary Jones', 'Smith, Cathy Gray', '1978-02-18', 'Syndey, Australia', 'M', 'W', 'FN', NULL, NULL, 'Unit 201, Diamond Plaza, Lot 10, Sapphire Avenue, Diamond Heights Subdivision, Barangay Western Bicutan, Taguig City, Metro Manila, Philippines, 1630', 'Unit 201, Diamond Plaza, Lot 10, Sapphire Avenue, Diamond Heights Subdivision, Barangay Western Bicutan, Taguig City, Metro Manila, Philippines, 1630', '+63(08)4567-8231', '+63960739638', '8897-0065', 'joesmith46@gmail.com');


INSERT INTO Member_Type (
    Member_ID, Direct_Contributor, Indirect_Contributor, Profession, Monthly_Income, Income_Proof
) VALUES
('PH001', NULL, 'SC', NULL, NULL, NULL),
('PH002', 'EP', NULL, 'Teacher', 25000, 'Certificate of Employment and Compensation'),
('PH003', 'PP', NULL, 'Nurse', 30000, 'Payslip'),
('PH004', NULL, 'SC', NULL, NULL, NULL),
('PH005', 'MWSB', NULL, 'Chef', 50000, 'Overseas Employment Certificate and Payslip'),
('PH006', NULL, 'PWD', NULL, NULL, NULL),
('PH007', NULL, 'SC', NULL, NULL, NULL),
('PH008', NULL, 'PWD', NULL, NULL, NULL),
('PH009', NULL, 'LGUS', NULL, NULL, NULL),
('PH010', 'FD', NULL, 'Private Driver', 15000, 'Income-Tax Return'),
('PH011', 'EP', NULL, 'Certified Public Accountant', 50000, 'Duly-notarized Affidavit of Income Declaration'),
('PH012', 'FN', NULL, 'Software Engineer', 80000, 'Duly-notarized affidavit of income declaration'),
('PH013', 'EG', NULL, 'Public School Teacher', 30000, 'Payslips from Department of Education (DepEd)'),
('PH014', 'EP', NULL, 'Marketing Executive', 65000, 'Duly-notarized Affidavit of Income Declaration'),
('PH015', 'SEII', NULL, 'Freelance Graphic Designer', 50000, 'Income Tax Return (ITR)'),
('PH016', 'SEII', NULL, 'Software Developer', 90000, 'Income Tax Return (ITR)'),
('PH017', 'EG', NULL, 'Registered Nurse', 30000, 'Payslips from hospital or healthcare institution'),
('PH018', 'EG', NULL, 'Professional Teacher', 23000, 'Payslips from Department of Education (DepEd)'),
('PH019', 'MWSB', NULL, 'Marine Engineer', 55000, 'Overseas Employment Certificate and Payslip'),
('PH020', 'PP', NULL, 'Entrepreneur', 36000, 'Income Tax Return (ITR)');

INSERT INTO Dependents_Declaration (
    Dependent_ID, Member_ID, Dependent_Name, Relationship, Dependent_Birthdate, Dependent_Citizenship, Dependent_Disability
) VALUES
('PHMD001', 'PH002', 'Natividad, Yolanda Santos', 'MO', '1950-03-15', 'Filipino', 0),
('PHMD002', 'PH002', 'Lopez, Miguel Natividad', 'CH', '2010-06-01', 'Filipino', 0),
('PHMD003', 'PH003', 'Reyes, Alliana Dela Cruz', 'CH', '2008-03-25', 'Filipino', 0),
('PHMD004', 'PH003', 'Magsalin, Regina Aquino', 'MO', '1945-08-30', 'Filipino', 0),
('PHMD005', 'PH003', 'Magsalin, Conrado Ramos', 'FA', '1942-11-20', 'Filipino', 0),
('PHMD006', 'PH005', 'Santos, Lucas Mendoza', 'CH', '2010-09-15', 'Filipino', 1),
('PHMD007', 'PH005', 'Santos, Carlo Mendoza', 'CH', '2012-08-08', 'Filipino', 0),
('PHMD008', 'PH005', 'Santos, Isabel Mendoza', 'CH', '2015-07-16', 'Filipino', 0),
('PHMD009', 'PH008', 'Romualdez, Carl', 'CH', '2017-12-17', 'Filipino', 0),
('PHMD010', 'PH008', 'Cruz, Juanito', 'FA', '1960-03-03', 'Filipino', 0),
('PHMD011', 'PH008', 'Cruz, Josefina Aguilar', 'MO', '1960-05-19', 'Filipino', 0),
('PHMD012', 'PH010', 'Zamora, Josefa', 'CH', '2006-01-14', 'Filipino', 0),
('PHMD013', 'PH010', 'Zamora, Kirsten', 'CH', '2007-11-21', 'Filipino', 0),
('PHMD014', 'PH010', 'Zamora, Kimberly', 'CH', '2008-11-13', 'Filipino', 1),
('PHMD015', 'PH011', 'Marquina, Pedro', 'FA', '1962-11-11', 'Filipino', 0),
('PHMD016', 'PH011', 'Marquina, Analiza Josol', 'MO', '1962-02-11', 'Filipino', 0),
('PHMD017', 'PH013', 'Flores, Maria De Jesus', 'LVSP', '1988-05-05', 'Filipino', 0),
('PHMD018', 'PH014', 'Garcia, Sofia Bernabe', 'CH', '2010-10-11', 'Filipino', 0),
('PHMD019', 'PH014', 'Garcia, Ernard Joseph Bernabe', 'CH', '2017-02-10', 'Filipino', 1),
('PHMD020', 'PH017', 'Reyes, Patricia Ann Bautista', 'MO', '1961-01-07', 'Filipino', 0),
('PHMD021', 'PH018', 'Dela Cruz, Gabriel Quinto', 'CH', '2005-09-09', 'Filipino', 0),
('PHMD022', 'PH020', 'Smith, Larah Gray', 'CH', '2008-11-23', 'Dual Citizen', 0),
('PHMD023', 'PH020', 'Smith, John Gray', 'CH', '2013-03-08', 'Dual Citizen', 0);