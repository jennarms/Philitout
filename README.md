![Philitout Logo]([https://github.com/jennarms/IskoCards/blob/main/assets/LogoHeader.png](https://raw.githubusercontent.com/jennarms/Philitout/refs/heads/main/PHILITOUT/pictures/Landscape%20logo%20(500%20x%20300%20px).png))

**PHIL it out!** A Python-based **CRUD (Create, Read, Update, Delete) system** that digitizes the traditional **PhilHealth Member Registration Form**, making the registration process more efficient and user-friendly. This system is built using **Python Tkinter** for the interface and **MySQL** for database management.

## Features

### General
- **Splash Screen & Welcome Page**
  - Instructions button for form guidelines
  - Access to the main application
- **User-Friendly Interface**
  - Form validation with input restrictions
  - "?" button for formatting guidance
  - Required & optional fields marked

### Main Functionalities
✔ **Member & Dependent Management**  
   - Registration of new members and dependents  
   - Update, delete, and view records  
   - Search functionality (by name, ID)  
   - Real-time table view of records  

✔ **Data Validation & Restrictions**  
   - Ensures correct data entry (e.g., name length, required fields)  
   - Validates dependent eligibility (e.g., age restrictions)  

✔ **Database Operations (Embedded SQL)**  
   - Uses **JOIN, SELECT, INSERT, UPDATE, DELETE** queries  
   - Generates unique **Member ID** and **Dependent ID**  
   - Ensures dependent records are linked to existing members  

✔ **Additional Features**  
   - **Query Execution Panel** (for SQL commands)  
   - **Report Generation** (customized database reports)  

## Technologies Used
- **Python** (Tkinter for GUI)
- **MySQL** (for data storage and management)

## Installation & Setup
1. Install **Python** and required libraries (`tkinter`, `mysql-connector`)
2. Set up a **MySQL database** and import the necessary tables
3. Run the Python script to launch the application

## Future Enhancements
- Improve UI/UX for better user experience
- Add authentication/login system
- Implement export options for reports

