import tkinter as tk
from tkinter import ttk, messagebox
from mysql.connector import Error
import mysql.connector
from PIL import Image, ImageTk
import subprocess
import os

class GenReport(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Generate Report")
        self.geometry("1500x600")
        self.create_header()
        self.create_ui()
        self.center_window()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    #WHEN USER CLICKED X BUTTON
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you really want to leave PHIL it out?"):
            self.destroy()

    #FOR HEADER
    def create_header(self):
        self.header_canvas = tk.Canvas(self, bg="#D4E7C5", height=80)
        self.header_canvas.pack(fill=tk.X)

        logo_path = 'D:\\2nd Sem\\Information Management\\PHILITOUT\\pictures\\App Logo (70 x 70 px).png'
        logo = Image.open(logo_path)
        self.logo_image = ImageTk.PhotoImage(logo)
        self.header_canvas.create_image(20, 40, anchor=tk.W, image=self.logo_image)

        header_label = tk.Label(self.header_canvas, text="PHIL it out! > Report Generation", font=("Arial", 24, "bold"), bg="#D4E7C5")
        header_label.place(x=100, y=20)

        back_button = tk.Button(self.header_canvas, text="Back", command=self.go_back, bg="#D84839", fg="white", font=("Helvetica", 12), padx=10, pady=5, borderwidth=2)
        back_button.pack(side=tk.RIGHT, padx=20, pady=20)

    #BACK BUTTON
    def go_back(self):
        script_path = os.path.join(os.path.dirname(__file__), 'Philitout.py')
        print(f"Opening {script_path}...")
        self.destroy()
        try:
            subprocess.run(["python", script_path], check=True)
        except FileNotFoundError:
            print(f"File {script_path} not found")
        except subprocess.CalledProcessError as e:
            print(f"Failed to run {script_path}: {e}")

    #WIDGETS FOR UI
    def create_ui(self):
        tk.Label(self, text="Select Level:", font=("Helvetica", 12, "italic bold")).pack(pady=10)

        style = ttk.Style()
        style.configure('TCombobox', font=('Helvetica', 12))
        style.configure('TComboboxPopdownFrame', font=('Helvetica', 12))

        self.level_combobox = ttk.Combobox(self, state="readonly", width=30, font=('Helvetica', 12))
        self.level_combobox['values'] = ("Simple", "Moderate", "Difficult")
        self.level_combobox.pack(pady=10)
        self.level_combobox.bind("<<ComboboxSelected>>", self.update_statement_combobox)

        tk.Label(self, text="Select Statement:", font=("Helvetica", 12, "italic bold")).pack(pady=10)

        self.statement_combobox = ttk.Combobox(self, state="readonly", width=80, font=('Helvetica', 12))
        self.statement_combobox.pack(pady=10)
        self.statement_combobox.bind("<<ComboboxSelected>>", self.execute_query)

        self.result_tree = ttk.Treeview(self)
        self.result_tree.pack(fill="both", expand=True, pady=20)

    #WHEN LEVEL IN COMBOBOX IS SELECTED
    def update_statement_combobox(self, event):
        selected_level = self.level_combobox.get()
        query_dict = {
            "Simple": {
                "Display all female members who are 60 years old and above (senior citizen), order by age asc ": 
                "SELECT Member_ID, Members_Name, Birthdate, Sex, TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS Age "
                "FROM personal_details "
                "WHERE Sex = 'F' AND TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) >= 60 "
                "ORDER BY Age ASC; ",

                "Display all male members who are 60 years old and above (senior citizen), order by age asc ": 
                "SELECT Member_ID, Members_Name, Birthdate, Sex, TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS Age "
                "FROM personal_details "
                "WHERE Sex = 'M' AND TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) >= 60 "
                "ORDER BY Age ASC; ",

                "Display all members who are below 60 years old (not senior citizen), order by age asc ": 
                "SELECT Member_ID, Members_Name, Birthdate, Sex, TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS Age"
                "FROM personal_details"
                "WHERE TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) < 60"
                "ORDER BY Age ASC;",

                "Display all dependents who are 21 years old and below and are Filipino.  Order by name asc, age asc ": 
                "SELECT Dependent_Name, Dependent_Birthdate, TIMESTAMPDIFF(YEAR, Dependent_Birthdate, CURDATE()) AS Age "
                "FROM dependents_declaration "
                "WHERE TIMESTAMPDIFF(YEAR, Dependent_Birthdate, CURDATE()) <= 21 "
                "AND Dependent_Citizenship = 'Filipino' "
                "ORDER BY Dependent_Name ASC, Age ASC; ",

                "Display all dependents who have disabilities, ordered by name ": 
                "SELECT * "
                "FROM dependents_declaration "
                "WHERE Dependent_Disability = true "
                "ORDER BY Dependent_Name ASC; "
            },
            "Moderate": {
                "Display all members' id, name, birthdate, and sex for those who are 60 years old and above and living in Manila ": 
                "SELECT Member_ID, Members_Name, Birthdate, Sex, TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS Age "
                "FROM personal_details "
                "WHERE Permanent_Address LIKE '%Manila%' "
                "GROUP BY Member_ID, Members_Name, Birthdate, Sex "
                "HAVING Age >= 60; ",

                "Display all members' id, name, birthdate, and sex for those who are 60 years old and above and living outside Manila ": 
                "SELECT Member_ID, Members_Name, Birthdate, Sex, TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS Age "
                "FROM personal_details "
                "WHERE Permanent_Address NOT LIKE '%Manila%' "
                "GROUP BY Member_ID, Members_Name, Birthdate, Sex "
                "HAVING Age >= 60; ",

                "Display the citizenship of dependents born before 2000 and count how many dependents are in that citizenship ": 
                "SELECT Dependent_Citizenship, COUNT(Dependent_Citizenship) AS Dependent_Count "
                "FROM dependents_declaration "
                "WHERE YEAR(Dependent_Birthdate) < 2000 "
                "GROUP BY Dependent_Citizenship; ",

                "Count Filipino dependents with disabilities and group by relationship type ": 
                "SELECT Relationship, COUNT(*) AS Count_Disabled_Dependents "
                "FROM Dependents_Declaration "
                "WHERE Dependent_Disability = true AND Dependent_Citizenship = 'Filipino' "
                "GROUP BY Relationship "
                "ORDER BY Count_Disabled_Dependents DESC; ",

                "Display sex then count how many members are there per sex ": 
                "SELECT Sex, COUNT(Sex) AS Count_Sex "
                "FROM personal_details "
                "GROUP BY Sex; "
            },
            "Difficult": {
                "Display all records from all tables ": 
                "SELECT * "
                "FROM personal_details AS p, member_type AS m, dependents_declaration AS d "
                "WHERE p.Member_ID = m.Member_ID = d.Member_ID; ",

                "Count how many dependents are below 21 years old and display members' id and name with the result ": 
                "SELECT p.Member_ID, Members_Name, COUNT(*) AS Dependents_Below21 "
                "FROM personal_details AS p, dependents_declaration AS d "
                "WHERE p.Member_ID = d.Member_ID "
                "AND TIMESTAMPDIFF(YEAR, Dependent_Birthdate, CURDATE()) < 21 "
                "GROUP BY p.Member_ID, Members_Name; ",

                "Count how many dependents are 60 years old and above and display members' id and name with the result ": 
                "SELECT p.Member_ID, Members_Name, COUNT(*) AS Senior_Dependents "
                "FROM personal_details AS p, dependents_declaration AS d "
                "WHERE p.Member_ID = d.Member_ID "
                "AND TIMESTAMPDIFF(YEAR, Dependent_Birthdate, CURDATE()) >= 60 "
                "GROUP BY p.Member_ID, Members_Name; ",

                "Display all members' id, name, birthdate, sex, and their dependents' name for those who are living in Manila ": 
                "SELECT p.Member_ID, Members_Name, Birthdate, Sex, Dependent_Name "
                "FROM personal_details AS p, dependents_declaration AS d "
                "WHERE p.Member_ID = d.Member_ID "
                "AND Permanent_Address LIKE '%Manila%' "
                "GROUP BY Member_ID, Members_Name, Birthdate, Sex, Dependent_Name; ",

                "Display members' id, name, and monthly income between 10000 and 50000 ": 
                "SELECT p.Member_ID, Members_Name, Monthly_Income "
                "FROM personal_details AS p, member_type AS m "
                "WHERE p.Member_ID = m.Member_ID "
                "GROUP BY Member_ID, Members_Name, Monthly_Income "
                "HAVING Monthly_Income BETWEEN 10000 AND 50000; "
            }
        }

        statements = list(query_dict[selected_level].keys())
        self.statement_combobox['values'] = statements

    #WHEN STATEMENT IN COMBOBOX IS SELECTED - WILL GENERATE THIS QUERY
    def execute_query(self, event):
        selected_level = self.level_combobox.get()
        selected_statement = self.statement_combobox.get()
        query_dict = {
            "Simple": {
                "Display all female members who are 60 years old and above (senior citizen), order by age asc ": 
                "SELECT Member_ID, Members_Name, Birthdate, Sex, TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS Age "
                "FROM personal_details "
                "WHERE Sex = 'F' AND TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) >= 60 "
                "ORDER BY Age ASC; ",

                "Display all male members who are 60 years old and above (senior citizen), order by age asc ": 
                "SELECT Member_ID, Members_Name, Birthdate, Sex, TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS Age "
                "FROM personal_details "
                "WHERE Sex = 'M' AND TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) >= 60 "
                "ORDER BY Age ASC; ",

                "Display all members who are below 60 years old (not senior citizen), order by age asc ": 
                "SELECT Member_ID, Members_Name, Birthdate, Sex, TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS Age "
                "FROM personal_details "
                "WHERE TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) < 60 "
                "ORDER BY Age ASC; ",

                "Display all dependents who are 21 years old and below and are Filipino.  Order by name asc, age asc ": 
                "SELECT Dependent_Name, Dependent_Birthdate, TIMESTAMPDIFF(YEAR, Dependent_Birthdate, CURDATE()) AS Age "
                "FROM dependents_declaration "
                "WHERE TIMESTAMPDIFF(YEAR, Dependent_Birthdate, CURDATE()) <= 21 "
                "AND Dependent_Citizenship = 'Filipino' "
                "ORDER BY Dependent_Name ASC, Age ASC; ",

                "Display all dependents who have disabilities, ordered by name ": 
                "SELECT * "
                "FROM dependents_declaration "
                "WHERE Dependent_Disability = true "
                "ORDER BY Dependent_Name ASC; "
            },
            "Moderate": {
                "Display all members' id, name, birthdate, and sex for those who are 60 years old and above and living in Manila ": 
                "SELECT Member_ID, Members_Name, Birthdate, Sex, TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS Age "
                "FROM personal_details "
                "WHERE Permanent_Address LIKE '%Manila%' "
                "GROUP BY Member_ID, Members_Name, Birthdate, Sex "
                "HAVING Age >= 60; ",

                "Display all members' id, name, birthdate, and sex for those who are 60 years old and above and living outside Manila ": 
                "SELECT Member_ID, Members_Name, Birthdate, Sex, TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS Age "
                "FROM personal_details "
                "WHERE Permanent_Address NOT LIKE '%Manila%' "
                "GROUP BY Member_ID, Members_Name, Birthdate, Sex "
                "HAVING Age >= 60; ",

                "Display the citizenship of dependents born before 2000 and count how many dependents are in that citizenship ": 
                "SELECT Dependent_Citizenship, COUNT(Dependent_Citizenship) AS Dependent_Count "
                "FROM dependents_declaration "
                "WHERE YEAR(Dependent_Birthdate) < 2000 "
                "GROUP BY Dependent_Citizenship; ",

                "Count Filipino dependents with disabilities and group by relationship type ": 
                "SELECT Relationship, COUNT(*) AS Count_Disabled_Dependents "
                "FROM Dependents_Declaration "
                "WHERE Dependent_Disability = true AND Dependent_Citizenship = 'Filipino' "
                "GROUP BY Relationship "
                "ORDER BY Count_Disabled_Dependents DESC; ",

                "Display sex then count how many members are there per sex ": 
                "SELECT Sex, COUNT(Sex) AS Count_Sex "
                "FROM personal_details "
                "GROUP BY Sex; "
            },
            "Difficult": {
                "Display all records from all tables ": 
                "SELECT * "
                "FROM personal_details AS p, member_type AS m, dependents_declaration AS d "
                "WHERE p.Member_ID = m.Member_ID = d.Member_ID; ",

                "Count how many dependents are below 21 years old and display members' id and name with the result ": 
                "SELECT p.Member_ID, Members_Name, COUNT(*) AS Dependents_Below21 "
                "FROM personal_details AS p, dependents_declaration AS d "
                "WHERE p.Member_ID = d.Member_ID "
                "AND TIMESTAMPDIFF(YEAR, Dependent_Birthdate, CURDATE()) < 21 "
                "GROUP BY p.Member_ID, Members_Name; ",

                "Count how many dependents are 60 years old and above and display members' id and name with the result ": 
                "SELECT p.Member_ID, Members_Name, COUNT(*) AS Senior_Dependents "
                "FROM personal_details AS p, dependents_declaration AS d "
                "WHERE p.Member_ID = d.Member_ID "
                "AND TIMESTAMPDIFF(YEAR, Dependent_Birthdate, CURDATE()) >= 60 "
                "GROUP BY p.Member_ID, Members_Name; ",

                "Display all members' id, name, birthdate, sex, and their dependents' name for those who are living in Manila ": 
                "SELECT p.Member_ID, Members_Name, Birthdate, Sex, Dependent_Name "
                "FROM personal_details AS p, dependents_declaration AS d "
                "WHERE p.Member_ID = d.Member_ID "
                "AND Permanent_Address LIKE '%Manila%' "
                "GROUP BY Member_ID, Members_Name, Birthdate, Sex, Dependent_Name; ",

                "Display members' id, name, and monthly income between 10000 and 50000 ": 
                "SELECT p.Member_ID, Members_Name, Monthly_Income "
                "FROM personal_details AS p, member_type AS m "
                "WHERE p.Member_ID = m.Member_ID "
                "GROUP BY Member_ID, Members_Name, Monthly_Income "
                "HAVING Monthly_Income BETWEEN 10000 AND 50000; "
            }
        }

        query = query_dict[selected_level][selected_statement]

        try:
            connection = self.connect_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                # Clear previous results
                for i in self.result_tree.get_children():
                    self.result_tree.delete(i)
                self.result_tree["columns"] = columns
                self.result_tree["show"] = "headings"

                for col in columns:
                    self.result_tree.heading(col, text=col)
                    self.result_tree.column(col, width=100)

                for row in rows:
                    self.result_tree.insert("", "end", values=row)
        except Error as e:
            messagebox.showerror("Error", f"Error executing query: {e}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection and connection.is_connected():
                connection.close()

    #DATABASE CONNECTION
    def connect_db(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='philitoutsystem',
                user='root',
                password='wynettecute@1'
            )
            if connection.is_connected():
                return connection
        except Error as e:
            messagebox.showerror("Error", f"Error connecting to MySQL: {e}")
            return None
        
    #TO CENTER GENERATE REPORT WINDOW
    def center_window(self):
        self.update_idletasks()
        window_width = self.winfo_width()
        window_height = self.winfo_height()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    gen_report = GenReport(root)
    root.mainloop()