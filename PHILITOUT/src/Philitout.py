import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import subprocess
import os
from SplashandWelcome import WelcomePage
import mysql.connector
from mysql.connector import Error
from datetime import datetime, date

# DATABASE CONNECTION
def connect_db():
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

class PhilitoutForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PHIL it out!")
        self.configure(bg="white")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # DATA DICTIONARY
        self.sex_map = {"Male": "M", "Female": "F"}
        self.reverse_sex_map = {v: k for k, v in self.sex_map.items()}
        self.civilstatus_map = {"Single": "S", "Married": "M", "Legally Seperated": "LS", "Annuled": "A", "Widow/er": "W"}
        self.reverse_civilstatus_map = {v: k for k, v in self.civilstatus_map.items()}
        self.citizenship_map = {"Filipino" : "F", "Dual Citizen": "DC", "Foreign National": "FN"}
        self.reverse_citizenship_map = {v: k for k, v in self.citizenship_map.items()}
        self.directcontributor_map = {"Employed Private" : "EP", "Employed Government" : " EG", "Professional Practitioner": "PP", "Self-Earning Individual": "SEII", "Self-Earning Individual Sole Proprietor": "SEISP", "Self-Earning Individual Group Enrollment Scheme": "SEIGES", 
                                                        "Kasambahay": "K", "Family Driver": "FD", "Migrant Worker Land Based": "MWLB", "Migrant Worker Sea Based": "MWSB", "Lifetime Member": "LM", "Filipinos with Dual Citizenship": "FWDC", "Foreign National": "FN"}
        self.reverse_directcontributor_map = {v: k for k, v in self.directcontributor_map.items()}
        self.indirectcontributor_map = {"Listahan": "L", "4Ps/MCCT": "PM", "Senior Citizen": "SC", "PAMANA": "P", "KIA/KIPO": "KK", "Bangsamoro Normalization": "BN", "LGU-Sponsored": "LGUS", "NGA-Sponsored": "NGAS", "Private-Sponsored": "PS", "Person with Disability": "PWD" }
        self.reverse_indirectcontributor_map = {v: k for k, v in self.indirectcontributor_map.items()}
        self.relationship_map = {"Living Spouse" : "LVSP", "Mother": "MO", "Father": "FA", "Child": "CH"}
        self.reverse_relationship_map = {v: k for k, v in self.relationship_map.items()}
     
    #HEADER
        self.header_canvas = tk.Canvas(bg="#D4E7C5", height=80)
        self.header_canvas.pack(fill=tk.X)

        logo_path = 'D:\\2nd Sem\\Information Management\\PHILITOUT\\pictures\\App Logo (70 x 70 px).png'
        logo = Image.open(logo_path)
        logo_image = ImageTk.PhotoImage(logo)

        self.header_canvas.create_image(20, 40, anchor=tk.W, image=logo_image)

        header_label = tk.Label(self.header_canvas, text="PHIL it out!", font=("Arial", 24, "bold"), bg="#D4E7C5")
        header_label.place(x=100, y=20)

        self.header_canvas.image = logo_image

        back_button = tk.Button(self.header_canvas, text="Back", command=self.go_back, bg="#D84839", fg="white", font=("Helvetica", 12), padx=10, pady= 5, borderwidth=2)
        back_button.pack(side=tk.RIGHT, padx=20, pady=20)

        # Create instructions button
        instructions_button = tk.Button(self.header_canvas, text="Instructions", command=self.show_instructions, bg="#4285F4", fg="white", font=("Helvetica", 12), padx=10, pady= 5, borderwidth=2)
        instructions_button.pack(side=tk.RIGHT, padx=20, pady=20)

        # Create do query button
        doquerybtn = tk.Button(self.header_canvas, text="Do Query", command=self.do_query, bg="#FDF7C3", fg="#000000", font=("Helvetica", 12), padx=10, pady= 5, borderwidth=2)
        doquerybtn.pack(side=tk.RIGHT, padx=20, pady=20)

        # Create report generation button
        reportgenbtn = tk.Button(self.header_canvas, text="Report Generation", command=self.report_generation, bg="#E1AFD1", fg="#000000", font=("Helvetica", 12), padx=10, pady= 5, borderwidth=2)
        reportgenbtn.pack(side=tk.RIGHT, padx=20, pady=20)

        self.form_center_window()

    #FORM
        # Create a frame to hold the scrollable input form
        input_scroll_frame = tk.Frame(self)
        input_scroll_frame.pack(side="left", padx=20, pady=20)

        # Create a canvas with a vertical scrollbar for the input form
        self.input_canvas = tk.Canvas(input_scroll_frame, borderwidth=0, width=400, height=700, highlightthickness=2, highlightbackground="#1F8D16")
        self.input_frame = tk.Frame(self.input_canvas)
        self.vsb = tk.Scrollbar(input_scroll_frame, orient="vertical", command=self.input_canvas.yview)
        self.input_canvas.configure(yscrollcommand=self.vsb.set)

        # Pack the scrollbar and canvas
        self.vsb.pack(side="right", fill="y")
        self.input_canvas.pack(side="left", fill="both", expand=True)

        # Configure the canvas to contain the input frame
        self.input_canvas.create_window((0,0), window=self.input_frame, anchor="nw")
        self.input_frame.bind("<Configure>", self.on_frame_configure)

        # Left Frame for Input Form inside the scrollable frame
        self.left_frame = tk.Frame(self.input_frame)

        self.create_personal_details()
        self.create_member_type()

    #TABLE USERS
        # Frame for Displaying Users
        self.middle_frame = tk.Frame(self, bg="#D4E7C5", highlightthickness=2, highlightbackground="#1F8D16")
        self.middle_frame.pack(side="top", padx=20, pady=20, fill="both", expand=False)

        users_label_button_frame = tk.Frame(self.middle_frame, bg="#D4E7C5")
        users_label_button_frame.pack(fill="x", padx=5, pady=(10, 0))

        # Label for "User"
        label = tk.Label(users_label_button_frame, text="User", bg="#D4E7C5", font=("Helvetica", 16, "bold"), anchor="w")
        label.grid(row=0, column=0, padx=5, pady=5)

        # Label, Text, and Button before the Edit User button
        self.user_id_text = tk.Text(users_label_button_frame, width=25, height=1)
        self.user_id_text.grid(row=0, column=1, padx=5, pady=5)
        self.usersearch_id_button = tk.Button(users_label_button_frame, text="Search", command =self.usersearch_record, bg="#FFFFFF", fg="#1F8D16", font=("Helvetica", 12), padx=5, pady=5, borderwidth=2)
        self.usersearch_id_button.grid(row=0, column=2, padx=5, pady=5)
        self.userviewall_id_button = tk.Button(users_label_button_frame, text="View All", bg="#4285F4", command =self.userview_all_records, fg="#FFFFFF", font=("Helvetica", 12), padx=5, pady=5, borderwidth=2)
        self.userviewall_id_button.grid(row=0, column=3, padx=5, pady=5)

        self.save_button = tk.Button(users_label_button_frame, text="Edit User", command=self.edit_user, bg="#FBC687", fg="black", font=("Helvetica", 12), padx=10, pady=5, borderwidth=2)
        self.save_button.grid(row=0, column=4, pady=0, padx=20)
        
        # Create a frame for the Treeview with scrollbars
        treeview_frame = tk.Frame(self.middle_frame)
        treeview_frame.pack(fill="both", padx=5, pady=5, expand=True)

        # Create a Treeview with columns and scrollbars
        self.data_tree = ttk.Treeview(treeview_frame, columns=(
            "Member ID", "Name", "Mother's Maiden Name", "Spouse", "Birthdate", "Birthplace", "Sex", "Civil Status",
            "Citizenship", "PhilSys ID Number", "TIN", "Permanent Address", "Mailing Address", "Home Phone Number",
            "Mobile Number", "Business Directline", "Email Address", "Direct Contributor", "Indirect Contributor", "Profession", "Monthly Income", "Income Proof"), show="headings", height=15)

        for col in self.data_tree["columns"]:
            self.data_tree.heading(col, text=col)

        # Create vertical scrollbar
        vsb_tree = ttk.Scrollbar(treeview_frame, orient="vertical", command=self.data_tree.yview)
        self.data_tree.configure(yscrollcommand=vsb_tree.set)
        vsb_tree.pack(side="right", fill="y")

        # Create horizontal scrollbar
        hsb_tree = ttk.Scrollbar(treeview_frame, orient="horizontal", command=self.data_tree.xview)
        self.data_tree.configure(xscrollcommand=hsb_tree.set)
        hsb_tree.pack(side="bottom", fill="x")

        # Grid layout for Treeview
        self.data_tree.pack(expand=True, fill="both")  # Pack the Treeview widget
        self.load_userdata()

    #TABLE DEPENDENTS
        dep_label_button_frame = tk.Frame(self.middle_frame, bg="#D4E7C5")
        dep_label_button_frame.pack(fill="x", padx=5, pady=(10, 0))

        # Label for "User's Dependents"
        label = tk.Label(dep_label_button_frame, text="User's Dependents",  bg="#D4E7C5", font=("Helvetica", 16, "bold"), anchor="w")
        label.grid(row=0, column=0, padx=5, pady=5)

        # Button beside the label
        self.dep_id_text = tk.Text(dep_label_button_frame, width=25, height=1)
        self.dep_id_text.grid(row=0, column=1, padx=5, pady=5)
        self.depsearch_id_button = tk.Button(dep_label_button_frame, text="Search", command=self.dep_search_record, bg="#FFFFFF", fg="#1F8D16", font=("Helvetica", 12), padx=5, pady=5, borderwidth=2)
        self.depsearch_id_button.grid(row=0, column=2, padx=5, pady=5)
        self.depviewall_id_button = tk.Button(dep_label_button_frame, text="View All", command=self.dep_view_all_records, bg="#4285F4", fg="#FFFFFF", font=("Helvetica", 12), padx=5, pady=5, borderwidth=2)
        self.depviewall_id_button.grid(row=0, column=3, padx=5, pady=5)

        # Add a spacer column
        tk.Label(dep_label_button_frame, text="", bg="#D4E7C5").grid(row=0, column=4, padx=10)

        dep_button = tk.Button(dep_label_button_frame, text="Add Dependents", command = self.add_dependents, bg="#1F8D16", fg="white", font=("Helvetica", 12), padx=10, pady=5, borderwidth=2)
        dep_button.grid(row=0, column=5, padx=5, pady=5)

        self.editdep_button = tk.Button(dep_label_button_frame, text="Edit Dependents", command = self.edit_dep, bg="#FBC687", fg="black", font=("Helvetica", 12), padx=10, pady= 5, borderwidth=2)
        self.editdep_button.grid(row=0, column=6, padx=5, pady=5)
    
        # Create a frame for the Treeview with scrollbars
        dep_treeview_frame = tk.Frame(self.middle_frame)
        dep_treeview_frame.pack(fill="both", padx=5, pady=5, expand=True)

        # Create a Treeview with columns and scrollbars
        self.data_tree_dependents = ttk.Treeview(dep_treeview_frame, columns=(
            "Dependent ID", "Member ID", "Dependent Name", "Relationship", "Dependent Birthdate", 
            "Dependent Citizenship", "Dependent Disability"), show="headings", height=15)

        for col in self.data_tree_dependents["columns"]:
            self.data_tree_dependents.heading(col, text=col)

        # Create vertical scrollbar
        vsb_tree = ttk.Scrollbar(dep_treeview_frame, orient="vertical", command=self.data_tree_dependents.yview)
        self.data_tree_dependents.configure(yscrollcommand=vsb_tree.set)
        vsb_tree.pack(side="right", fill="y")

        # Create horizontal scrollbar
        hsb_tree = ttk.Scrollbar(dep_treeview_frame, orient="horizontal", command=self.data_tree_dependents.xview)
        self.data_tree_dependents.configure(xscrollcommand=hsb_tree.set)
        hsb_tree.pack(side="bottom", fill="x")

        # Grid layout for Treeview
        self.data_tree_dependents.pack(side="left", fill="both", expand=True)
        self.load_dependents()

    # USER SEARCH
    def usersearch_record(self):
            search_term = self.user_id_text.get("1.0", tk.END).strip()
            if not search_term:
                messagebox.showwarning("Warning", "You did not search any name.")
                return

            # Clear existing entries in the data tree
            for item in self.data_tree.get_children():
                self.data_tree.delete(item)

            try:
                connection = connect_db()
                if connection:
                    cursor = connection.cursor()
                    query = """
                        SELECT pd.Member_ID, pd.Members_Name, pd.Mothers_MaidenName, pd.SpouseName, pd.Birthdate, pd.Birthplace, pd.Sex, pd.Civil_Status, pd.Citizenship, pd.Philsys_IDNum, pd.TIN, pd.Permanent_Address, pd.Mailing_Address, pd.Home_PhoneNum, pd.Mobile_Number, pd.Business_DL, pd.Email_Address, 
                            mt.Direct_Contributor, mt.Indirect_Contributor, mt.Profession, mt.Monthly_Income, mt.Income_Proof
                        FROM Personal_Details pd
                        LEFT JOIN Member_Type mt ON pd.Member_ID = mt.Member_ID
                        WHERE pd.Members_Name LIKE %s
                    """
                    cursor.execute(query, (f"%{search_term}%",))
                    rows = cursor.fetchall()
                    if not rows:
                        messagebox.showinfo("Info", "No matching records found.")
                    else:
                        for row in rows:
                            row_list = list(row)
                            # Apply mappings to the appropriate columns with index checks
                            if len(row_list) > 6:
                                row_list[6] = self.reverse_sex_map.get(row_list[6], row_list[6])
                            if len(row_list) > 7:
                                row_list[7] = self.reverse_civilstatus_map.get(row_list[7], row_list[7])
                            if len(row_list) > 8:
                                row_list[8] = self.reverse_citizenship_map.get(row_list[8], row_list[8])
                            if len(row_list) > 17:
                                row_list[17] = self.reverse_directcontributor_map.get(row_list[17], row_list[17])
                            if len(row_list) > 18:
                                row_list[18] = self.reverse_indirectcontributor_map.get(row_list[18], row_list[18])
                            # Insert the modified row into the data tree
                            self.data_tree.insert('', 'end', values=tuple(row_list))
            except Error as e:
                messagebox.showerror("Error", f"Error searching record: {e}")
            finally:
                if 'cursor' in locals() and cursor:
                    cursor.close()
                if 'connection' in locals() and connection and connection.is_connected():
                    connection.close()

    #DELETE THE PREVIOUS USER SEARCH
    def userview_all_records(self):
        self.user_id_text.delete(1.0, 'end')  # Clear the search entry

        # Clear existing entries in the data tree
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)

        try:
            connection = connect_db()
            if connection:
                cursor = connection.cursor()
                query = """
                    SELECT pd.Member_ID, pd.Members_Name, pd.Mothers_MaidenName, pd.SpouseName, pd.Birthdate, pd.Birthplace, pd.Sex, pd.Civil_Status, pd.Citizenship, pd.Philsys_IDNum, pd.TIN, pd.Permanent_Address, pd.Mailing_Address, pd.Home_PhoneNum, pd.Mobile_Number, pd.Business_DL, pd.Email_Address, 
                        mt.Direct_Contributor, mt.Indirect_Contributor, mt.Profession, mt.Monthly_Income, mt.Income_Proof
                    FROM Personal_Details pd
                    LEFT JOIN Member_Type mt ON pd.Member_ID = mt.Member_ID
                """
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    row_list = list(row)
                    # Apply mappings to the appropriate columns with index checks
                    if len(row_list) > 6:
                        row_list[6] = self.reverse_sex_map.get(row_list[6], row_list[6])
                    if len(row_list) > 7:
                        row_list[7] = self.reverse_civilstatus_map.get(row_list[7], row_list[7])
                    if len(row_list) > 8:
                        row_list[8] = self.reverse_citizenship_map.get(row_list[8], row_list[8])
                    if len(row_list) > 17:
                        row_list[17] = self.reverse_directcontributor_map.get(row_list[17], row_list[17])
                    if len(row_list) > 18:
                        row_list[18] = self.reverse_indirectcontributor_map.get(row_list[18], row_list[18])
                    # Insert the modified row into the data tree
                    self.data_tree.insert('', 'end', values=tuple(row_list))
        except Error as e:
            messagebox.showerror("Error", f"Error loading all records: {e}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection and connection.is_connected():
                connection.close()

    #SEARCH IN DEPENDENTS TABLE
    def dep_search_record(self):
        search_term = self.dep_id_text.get("1.0", tk.END).strip()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a dependent name.")
            return

        for item in self.data_tree_dependents.get_children():
            self.data_tree_dependents.delete(item)

        try:
            connection = connect_db()
            if connection:
                cursor = connection.cursor()
                query = "SELECT * FROM Dependents_Declaration WHERE Dependent_Name LIKE %s"
                cursor.execute(query, (f"%{search_term}%",))
                rows = cursor.fetchall()
                if not rows:
                    messagebox.showinfo("Info", "No matching dependents found.")
                else:
                    for row in rows:
                        row_list = list(row)
                        if len(row_list) > 3:
                            row_list[3] = self.reverse_relationship_map.get(row_list[3], row_list[3]) 
                        self.data_tree_dependents.insert('', 'end', values=tuple(row_list))
        except Error as e:
            messagebox.showerror("Error", f"Error searching record: {e}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection and connection.is_connected():
                connection.close()
    
    #DELETE THE PREVIOUS SEARCH
    def dep_view_all_records(self):
        self.dep_id_text.delete(1.0, 'end')  # Clear the search entry

        for item in self.data_tree_dependents.get_children():
            self.data_tree_dependents.delete(item)

        try:
            connection = connect_db()
            if connection:
                cursor = connection.cursor()
                query = "SELECT * FROM Dependents_Declaration"
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    row_list = list(row)
                    if len(row_list) > 3:
                        row_list[3] = self.reverse_relationship_map.get(row_list[3], row_list[3]) 
                    self.data_tree_dependents.insert('', 'end', values=tuple(row_list))
        except Error as e:
            messagebox.showerror("Error", f"Error loading all records: {e}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection and connection.is_connected():
                connection.close()

    # WHEN USER CLICKED X BUTTON
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you really want to leave PHIL it out?"):
            self.destroy()

    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.input_canvas.configure(scrollregion=self.input_canvas.bbox("all"))
    
    #FOR SHOW INSTRUCTIONS BUTTON
    def show_instructions(self):
        instructions_window = tk.Toplevel(self)
        instructions_window.title("Instructions")
        instructions_window.attributes("-topmost", True)
        instructions_window.overrideredirect(True)

        try:
            instructions_image_path = "D:\\2nd Sem\\Information Management\\PHILITOUT\\pictures\\Instructions (1300 x 500 px).png"
            instructions_image = Image.open(instructions_image_path)
            instructions_photo = ImageTk.PhotoImage(instructions_image)

            # Create a label to display the image
            instructions_label = tk.Label(instructions_window, image=instructions_photo)
            instructions_label.image = instructions_photo  # Keep a reference
            instructions_label.pack()

        except Exception as e:
            messagebox.showerror("Error", f"Error displaying instructions: {e}")

        style = ttk.Style()
        style.configure('Close.TButton', font=('Helvetica', 14), padding=10)

        close_button = ttk.Button(instructions_window, text="Close", style='Close.TButton', command=instructions_window.destroy)
        close_button.pack(pady=10, padx=20)

        instructions_window.configure(borderwidth=5)
        instructions_window.update_idletasks()
        window_width = instructions_window.winfo_width()
        window_height = instructions_window.winfo_height()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        instructions_window.geometry(f"+{x}+{y}")

    #FOR BACK BUTTON
    def go_back(self):
        self.destroy()
        welcome_root = tk.Tk()
        welcome_page = WelcomePage(welcome_root)
        welcome_root.mainloop()

    #DO QUERY BUTTON
    def do_query(self):
        script_path = os.path.join(os.path.dirname(__file__), 'DoQuery.py')
        print(f"Opening {script_path}...")
        self.destroy()
        try:
            subprocess.run(["python", script_path], check=True)
        except FileNotFoundError:
            print(f"File {script_path} not found")
        except subprocess.CalledProcessError as e:
            print(f"Failed to run {script_path}: {e}")
    
    #REPORT GENERATION BUTTON
    def report_generation(self):
        script_path = os.path.join(os.path.dirname(__file__), 'GenReport.py')
        print(f"Opening {script_path}...")
        self.destroy()
        try:
            subprocess.run(["python", script_path], check=True)
        except FileNotFoundError:
            print(f"File {script_path} not found")
        except subprocess.CalledProcessError as e:
            print(f"Failed to run {script_path}: {e}")

    #EDIT DEPENDENTS BUTTON
    def edit_dep(self):
        script_path = os.path.join(os.path.dirname(__file__), 'EditDeps.py')
        print(f"Opening {script_path}...")
        self.destroy()
        try:
            subprocess.run(["python", script_path], check=True)
        except FileNotFoundError:
            print(f"File {script_path} not found")
        except subprocess.CalledProcessError as e:
            print(f"Failed to run {script_path}: {e}")

    #EDIT USER BUTTON 
    def edit_user(self):
        script_path = os.path.join(os.path.dirname(__file__), 'EditUsers.py')
        print(f"Opening {script_path}...")
        self.destroy()
        try:
            subprocess.run(["python", script_path], check=True)
        except FileNotFoundError:
            print(f"File {script_path} not found")
        except subprocess.CalledProcessError as e:
            print(f"Failed to run {script_path}: {e}")

    #WIDGETS FOR FORM - USER
    def create_personal_details(self):
        tk.Label(self.left_frame, text="Personal Details", font=("Helvetica", 16)).grid(row=0, columnspan=2, sticky="w", padx=5, pady=5)

        tk.Label(self.left_frame, text="Name").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.name_entry = tk.Entry(self.left_frame)
        self.name_entry.grid(row=2, column=1, padx=5, pady=5)
        self.namebtn = tk.Button(self.left_frame, text="?", font=("Helvetica", 10, "bold"), bg = "#D4E7C5", fg="#000000", command = self.show_name)
        self.namebtn.grid(row=2, column=2, padx=5, pady=5)

        tk.Label(self.left_frame, text="Mother's Maiden Name").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.maiden_name_entry = tk.Entry(self.left_frame)
        self.maiden_name_entry.grid(row=3, column=1, padx=5, pady=5)
        self.maidennamebtn = tk.Button(self.left_frame, text="?", font=("Helvetica", 10, "bold"), bg = "#D4E7C5", fg="#000000", command = self.show_name)
        self.maidennamebtn.grid(row=3, column=2, padx=5, pady=5)

        tk.Label(self.left_frame, text="Spouse:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.spouse_entry = tk.Entry(self.left_frame)
        self.spouse_entry.grid(row=4, column=1, padx=5, pady=5)
        self.spousenamebtn = tk.Button(self.left_frame, text="?", font=("Helvetica", 10, "bold"), bg = "#D4E7C5", fg="#000000", command = self.show_name)
        self.spousenamebtn.grid(row=4, column=2, padx=5, pady=5)
        tk.Label(self.left_frame, text="~", font=("Helvetica", 15, "italic bold"), fg="#1F8D16").grid(row=4, column=3, sticky="w", padx=5, pady=5)

        tk.Label(self.left_frame, text="Birthdate").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.birthdate_entry = DateEntry(self.left_frame, width=12, background='darkgreen', foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.birthdate_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self.left_frame, text="Birthplace").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.birthplace_entry = tk.Entry(self.left_frame)
        self.birthplace_entry.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(self.left_frame, text="Sex").grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.sex_var = tk.StringVar(self.left_frame)
        self.sex_dropdown = ttk.Combobox(self.left_frame, textvariable=self.sex_var, values=["Male", "Female"], state ="readonly")
        self.sex_dropdown.grid(row=7, column=1, padx=5, pady=5)

        self.sex_dropdown = ttk.Combobox(self.left_frame, textvariable=self.sex_var, values=list(self.sex_map.keys()), state ="readonly")
        self.sex_dropdown.grid(row=7, column=1, padx=5, pady=5)

        tk.Label(self.left_frame, text="Civil Status").grid(row=8, column=0, sticky="w", padx=5, pady=5)
        self.civil_status_var = tk.StringVar(self.left_frame)
        self.civil_status_dropdown = ttk.Combobox(self.left_frame, textvariable=self.civil_status_var, values=["Single", "Married", "Legally Seperated", "Annuled", "Widow/er"], state ="readonly")
        self.civil_status_dropdown.grid(row=8, column=1, padx=5, pady=5)

        tk.Label(self.left_frame, text="Citizenship").grid(row=9, column=0, sticky="w", padx=5, pady=5)
        self.citizenship_var = tk.StringVar(self.left_frame)
        self.citizenship_dropdown = ttk.Combobox(self.left_frame, textvariable=self.citizenship_var, values=["Filipino", "Dual Citizen", "Foreign National"], state ="readonly")
        self.citizenship_dropdown.grid(row=9, column=1, padx=5, pady=5)

        tk.Label(self.left_frame, text="PhilSys ID Number:").grid(row=10, column=0, sticky="w", padx=5, pady=5)
        self.philsys_id_entry = tk.Entry(self.left_frame)
        self.philsys_id_entry.grid(row=10, column=1, padx=5, pady=5)
        tk.Label(self.left_frame, text="~", font=("Helvetica", 15, "italic bold"), fg="#1F8D16").grid(row=10, column=2, sticky="w", padx=5, pady=5)

        tk.Label(self.left_frame, text="TIN:").grid(row=11, column=0, sticky="w", padx=5, pady=5)
        self.tin_entry = tk.Entry(self.left_frame)
        self.tin_entry.grid(row=11, column=1, padx=5, pady=5)
        tk.Label(self.left_frame, text="~", font=("Helvetica", 15, "italic bold"), fg="#1F8D16").grid(row=11, column=2, sticky="w", padx=5, pady=5)

        tk.Label(self.left_frame, text="Permanent Address").grid(row=12, column=0, sticky="w", padx=5, pady=5)
        self.permanent_address_entry = tk.Entry(self.left_frame)
        self.permanent_address_entry.grid(row=12, column=1, padx=5, pady=5)
        self.permaddbtn = tk.Button(self.left_frame, text="?", font=("Helvetica", 10, "bold"), bg = "#D4E7C5", fg="#000000", command = self.show_address)
        self.permaddbtn.grid(row=12, column=2, padx=5, pady=5)

        tk.Label(self.left_frame, text="Mailing Address").grid(row=13, column=0, sticky="w", padx=5, pady=5)
        self.mailing_address_entry = tk.Entry(self.left_frame)
        self.mailing_address_entry.grid(row=13, column=1, padx=5, pady=5)
        self.mailaddbtn = tk.Button(self.left_frame, text="?", font=("Helvetica", 10, "bold"), bg = "#D4E7C5", fg="#000000", command = self.show_address)
        self.mailaddbtn.grid(row=13, column=2, padx=5, pady=5)

        tk.Label(self.left_frame, text="Home Phone Number:").grid(row=14, column=0, sticky="w", padx=5, pady=5)
        self.home_phone_entry = tk.Entry(self.left_frame)
        self.home_phone_entry.grid(row=14, column=1, padx=5, pady=5)
        tk.Label(self.left_frame, text="~", font=("Helvetica", 15, "italic bold"), fg="#1F8D16").grid(row=14, column=2, sticky="w", padx=5, pady=5)

        tk.Label(self.left_frame, text="Mobile Number").grid(row=15, column=0, sticky="w", padx=5, pady=5)
        self.mobile_entry = tk.Entry(self.left_frame)
        self.mobile_entry.grid(row=15, column=1, padx=5, pady=5)

        tk.Label(self.left_frame, text="Business Directline:").grid(row=16, column=0, sticky="w", padx=5, pady=5)
        self.business_directline_entry = tk.Entry(self.left_frame)
        self.business_directline_entry.grid(row=16, column=1, padx=5, pady=5)
        tk.Label(self.left_frame, text="~", font=("Helvetica", 15, "italic bold"), fg="#1F8D16").grid(row=16, column=2, sticky="w", padx=5, pady=5)

        tk.Label(self.left_frame, text="Email Address").grid(row=17, column=0, sticky="w", padx=5, pady=5)
        self.email_entry = tk.Entry(self.left_frame)
        self.email_entry.grid(row=17, column=1, padx=5, pady=5)

    def update_contributor_type(self):
        if self.contributor_type_var.get() == "Direct":
            self.direct_contributor_dropdown.config(state="readonly")
            self.indirect_contributor_dropdown.config(state="disabled")
            self.indirect_contributor_dropdown.set("")
        else:
            self.direct_contributor_dropdown.config(state="disabled")
            self.indirect_contributor_dropdown.config(state="readonly")
            self.direct_contributor_dropdown.set("")

    def create_member_type(self):
        tk.Label(self.left_frame, text="").grid(row=26, columnspan=2)

        tk.Label(self.left_frame, text="Member Type", font=("Helvetica", 16)).grid(row=18, columnspan=2, sticky="w", padx=5, pady=5)

        self.contributor_type_var = tk.StringVar(value=0)  # No default

        tk.Radiobutton(self.left_frame, text="Direct Contributor", variable=self.contributor_type_var, value="Direct", command=self.update_contributor_type).grid(row=19, column=0, sticky="w", padx=5, pady=5)
        tk.Radiobutton(self.left_frame, text="Indirect Contributor", variable=self.contributor_type_var, value="Indirect", command=self.update_contributor_type).grid(row=19, column=1, sticky="w", padx=5, pady=5)

        # Direct Contributor dropdown
        self.direct_contributor_var = tk.StringVar(self.left_frame)
        self.direct_contributor_dropdown = ttk.Combobox(self.left_frame, textvariable=self.direct_contributor_var, values=list(self.directcontributor_map.keys()))
        self.direct_contributor_dropdown.grid(row=20, column=0, padx=5, pady=5)

        # Indirect Contributor dropdown
        self.indirect_contributor_var = tk.StringVar(self.left_frame)
        self.indirect_contributor_dropdown = ttk.Combobox(self.left_frame, textvariable=self.indirect_contributor_var, values=list(self.indirectcontributor_map.keys()))
        self.indirect_contributor_dropdown.grid(row=20, column=1, padx=5, pady=5)

        # Initially, enable Direct Contributor and disable Indirect Contributor
        self.update_contributor_type()

        tk.Label(self.left_frame, text="Profession").grid(row=21, column=0, sticky="w", padx=5, pady=5)
        self.profession_entry = tk.Entry(self.left_frame)
        self.profession_entry.grid(row=21, column=1, padx=5, pady=5)

        tk.Label(self.left_frame, text="Monthly Income").grid(row=22, column=0, sticky="w", padx=5, pady=5)
        self.monthly_income_entry = tk.Entry(self.left_frame)
        self.monthly_income_entry.grid(row=22, column=1, padx=5, pady=5)

        tk.Label(self.left_frame, text="Income Proof").grid(row=23, column=0, sticky="w", padx=5, pady=5)
        self.income_proof_entry = tk.Entry(self.left_frame)
        self.income_proof_entry.grid(row=23, column=1, padx=5, pady=5)
        self.incomeproofbtn = tk.Button(self.left_frame, text="?", font=("Helvetica", 10, "bold"), bg = "#D4E7C5", fg="#000000", command = self.show_incomeproof)
        self.incomeproofbtn.grid(row=23, column=2, padx=5, pady=5)

    #SUBMIT
        self.submit_button = tk.Button(self.left_frame, text="Submit", command=self.submit_userdata, bg="#1F8D16", fg="#FFFFFF", font=("Helvetica", 12), padx=10, pady= 5, borderwidth=2)
        self.submit_button.grid(row=33, column=0, padx=5, pady=10)
        self.left_frame.pack(padx=20, pady=20)

        self.clear_button = tk.Button(self.left_frame, text="Clear", command=self.clear_fields, bg="#D84839", fg="white", font=("Helvetica", 12), padx=10, pady= 5, borderwidth=2)
        self.clear_button.grid(row=33, column=1, padx=5, pady=10)
        self.left_frame.pack(padx=20, pady=20)
    
    #FOR ? BUTTON, ADDRESS FORMAT
    def show_address(self):
        philitoutaddress_window = tk.Toplevel(self)
        philitoutaddress_window.title("Address Format")
        philitoutaddress_window.attributes("-topmost", True)
        philitoutaddress_window.overrideredirect(True)

        try:
            philitoutaddress_image_path = "D:\\2nd Sem\\Information Management\\PHILITOUT\\pictures\\Address Format (1300 x 500 px).png"
            philitoutaddress_image = Image.open(philitoutaddress_image_path)
            philitoutaddress_photo = ImageTk.PhotoImage(philitoutaddress_image)

            philitoutaddress_label = tk.Label(philitoutaddress_window, image=philitoutaddress_photo)
            philitoutaddress_label.image = philitoutaddress_photo
            philitoutaddress_label.pack()

        except Exception as e:
            messagebox.showerror("Error", f"Error displaying instructions: {e}")

        style = ttk.Style()
        style.configure('Close.TButton', font=('Helvetica', 14), padding=10)

        close_button = ttk.Button(philitoutaddress_window, text="Close", style='Close.TButton', command=philitoutaddress_window.destroy)
        close_button.pack(pady=10, padx=20)

        philitoutaddress_window.configure(borderwidth=5)  
        philitoutaddress_window.update_idletasks()
        window_width =philitoutaddress_window.winfo_width()
        window_height = philitoutaddress_window.winfo_height()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        philitoutaddress_window.geometry(f"+{x}+{y}")

    #FOR ? BUTTON, NAME FORMAT
    def show_name(self):
        philitoutname_window = tk.Toplevel(self)
        philitoutname_window.title("Name Format")
        philitoutname_window.attributes("-topmost", True)
        philitoutname_window.overrideredirect(True)

        try:
            philitoutname_image_path = "D:\\2nd Sem\\Information Management\\PHILITOUT\\pictures\\Name Format (1300 x 500 px).png"
            philitoutname_image = Image.open(philitoutname_image_path)
            philitoutname_photo = ImageTk.PhotoImage(philitoutname_image)

            philitoutname_label = tk.Label(philitoutname_window, image=philitoutname_photo)
            philitoutname_label.image = philitoutname_photo
            philitoutname_label.pack()

        except Exception as e:
            messagebox.showerror("Error", f"Error displaying instructions: {e}")

        style = ttk.Style()
        style.configure('Close.TButton', font=('Helvetica', 14), padding=10)

        close_button = ttk.Button(philitoutname_window, text="Close", style='Close.TButton', command=philitoutname_window.destroy)
        close_button.pack(pady=10, padx=20)

        philitoutname_window.configure(borderwidth=5)  
        philitoutname_window.update_idletasks()
        window_width =philitoutname_window.winfo_width()
        window_height = philitoutname_window.winfo_height()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        philitoutname_window.geometry(f"+{x}+{y}")

    #FOR ? BUTTON, ACCEPTED INCOME PROOF
    def show_incomeproof(self):
        incomeproof_window = tk.Toplevel(self)
        incomeproof_window.title("Accepted Income Proof")
        incomeproof_window.attributes("-topmost", True)
        incomeproof_window.overrideredirect(True)

        try:
            incomeproof_image_path = "D:\\2nd Sem\\Information Management\\PHILITOUT\\pictures\\Proof of Income (1300 x 500 px).png"
            incomeproof_image = Image.open(incomeproof_image_path)
            incomeproof_photo = ImageTk.PhotoImage(incomeproof_image)

            instructions_label = tk.Label(incomeproof_window, image=incomeproof_photo)
            instructions_label.image = incomeproof_photo
            instructions_label.pack()

        except Exception as e:
            messagebox.showerror("Error", f"Error displaying Proof of Income Guidelines: {e}")

        style = ttk.Style()
        style.configure('Close.TButton', font=('Helvetica', 14), padding=10)

        close_button = ttk.Button(incomeproof_window, text="Close", style='Close.TButton', command=incomeproof_window.destroy)
        close_button.pack(pady=10, padx=20)

        incomeproof_window.configure(borderwidth=5)  
        incomeproof_window.update_idletasks() 
        window_width =incomeproof_window.winfo_width()
        window_height = incomeproof_window.winfo_height()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        incomeproof_window.geometry(f"+{x}+{y}")

    #SUBMIT BUTTON
    def submit_userdata(self):
        member_id = self.generate_member_id()
        member_name = self.name_entry.get()
        maidenname = self.maiden_name_entry.get()
        spouse = self.spouse_entry.get()
        birthdate = self.birthdate_entry.get_date().strftime('%Y-%m-%d')
        birthplace = self.birthplace_entry.get()
        sex_display = self.sex_var.get()
        sex= self.sex_map.get(sex_display, "")
        civilstatus_display = self.civil_status_var.get()
        civilstatus = self.civilstatus_map.get(civilstatus_display, "")
        citizenship_display = self.citizenship_var.get()
        citizenship = self.citizenship_map.get(citizenship_display, "")
        philsys = self.philsys_id_entry.get()
        tin = self.tin_entry.get()
        permanentaddress = self.permanent_address_entry.get()
        mailingaddres = self.mailing_address_entry.get()
        homephone = self.home_phone_entry.get()
        mobile = self.mobile_entry.get()
        businessdl = self.business_directline_entry.get()
        email = self.email_entry.get()
        directcontributor_display = self.direct_contributor_var.get()
        directcontributor = self.directcontributor_map.get(directcontributor_display, "")
        indirectcontributor_display = self.indirect_contributor_var.get()
        indirectcontributor = self.indirectcontributor_map.get(indirectcontributor_display, "") 
        profession = self.profession_entry.get()
        monthly_income_str = self.monthly_income_entry.get()
        incomeproof = self.income_proof_entry.get()

    #RESTRICTIONS
        if not member_name:
            messagebox.showwarning("Warning", "Please fill in the member name.")
            return
        elif len(member_name) < 5:
            messagebox.showwarning("Insufficient Characters", "Name should be at least 5 characters.")
            return
        elif len(member_name) > 100:
            messagebox.showwarning("Exceeded Characters", "Name should have a maximum of 100 characters.")
            return

        
        if not maidenname:
            messagebox.showwarning("Warning", "Please fill in the mother's maiden name.")
            return
        elif len(maidenname) < 5:
            messagebox.showwarning("Insufficient Characters", "Mother's maiden name should be at least 5 characters.")
            return
        elif len(maidenname) > 100:
            messagebox.showwarning("Exceeded Characters", "Mother's maiden name should have a maximum of 100 characters.")
            return
        
        if spouse:
            if len(spouse) < 5:
                messagebox.showwarning("Insufficient Characters", "Spouse's name should be at least 5 characters.")
                return
            elif len(spouse) > 100:
                messagebox.showwarning("Exceeded Characters", "Spouse's name should have a maximum of 100 characters.")
                return
        

        if not birthdate:
            messagebox.showwarning("Warning", "Please fill in the birthdate.")
            return
            
        if not birthplace:
            messagebox.showwarning("Warning", "Please fill in the birthplace.")
            return
        elif len(birthplace) < 5:
            messagebox.showwarning("Insufficient Characters", "Birthplace should be at least 5 characters.")
            return
        elif len(birthplace) > 100:
            messagebox.showwarning("Exceeded Characters", "Birthplace should have a maximum of 100 characters.")
            return

        if not sex:
            messagebox.showwarning("Warning", "Please select the sex.")
            return
        if not civilstatus:
            messagebox.showwarning("Warning", "Please select the civil status.")
            return
        if not citizenship:
            messagebox.showwarning("Warning", "Please fill in the citizenship.")
            return
        
        if not permanentaddress:
            messagebox.showwarning("Warning", "Please fill in the permanent address.")
            return
        elif len(permanentaddress) < 10:
            messagebox.showwarning("Insufficient Characters", "Permanent Address should be at least 10 characters.")
            return
        elif len(permanentaddress) > 300:
            messagebox.showwarning("Exceeded Characters", "Permanent Address should have a maximum of 100 characters.")
            return

        if not mailingaddres:
            messagebox.showwarning("Warning", "Please fill in the mailing address.")
            return
        elif len(mailingaddres) < 10:
            messagebox.showwarning("Insufficient Characters", "Mailing Address should be at least 10 characters.")
            return
        elif len(mailingaddres) > 300:
            messagebox.showwarning("Exceeded Characters", "Mailing Address should have a maximum of 100 characters.")
            return
        
        if not mobile:
            messagebox.showwarning("Warning", "Please fill in the mobile number.")
            return
        if not email:
            messagebox.showwarning("Warning", "Please fill in the email address.")
            return
        if not (directcontributor or indirectcontributor):
            messagebox.showwarning("Warning", "Please specify if the member is a direct or indirect contributor.")
            return
        
        try:
            monthly_income = float(monthly_income_str)
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid numeric value for monthly income. If none please type 0")
            return
        
        try:
            connection = connect_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO Personal_Details (Member_ID, Members_Name, Mothers_MaidenName, SpouseName, Birthdate, Birthplace, Sex, Civil_Status, Citizenship, Philsys_IDNum, TIN, Permanent_Address, Mailing_Address, Home_PhoneNum, Mobile_Number, Business_DL, Email_Address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (member_id, member_name, maidenname, spouse, birthdate, birthplace, sex, civilstatus, citizenship, philsys, tin, permanentaddress, mailingaddres, homephone, mobile, businessdl, email))
                cursor.execute("INSERT INTO Member_Type (Member_ID, Direct_Contributor, Indirect_Contributor, Profession, Monthly_Income, Income_Proof) VALUES (%s, %s, %s, %s, %s, %s)",
                            (member_id, directcontributor, indirectcontributor, profession, monthly_income, incomeproof))
                connection.commit()
                self.load_userdata()
                messagebox.showinfo("Success", "Member created successfully")
                self.clear_fields()  # Call clear_fields() after successful insertion
        except Error as e:
            messagebox.showerror("Error", f"Error creating member: {e}")
        finally:
            if connection and connection.is_connected():
                connection.close()

    #CLEAR FUNCTION
    def clear_fields(self):
        self.name_entry.delete(0, "end")
        self.maiden_name_entry.delete(0, "end")
        self.spouse_entry.delete(0, "end")
        self.birthdate_entry.delete(0, "end")
        self.birthplace_entry.delete(0, "end")
        self.sex_var.set("")
        self.civil_status_var.set("")
        self.citizenship_var.set("")
        self.philsys_id_entry.delete(0, "end")
        self.tin_entry.delete(0, "end")
        self.permanent_address_entry.delete(0, "end")
        self.mailing_address_entry.delete(0, "end")
        self.home_phone_entry.delete(0, "end")
        self.mobile_entry.delete(0, "end")
        self.business_directline_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        
        self.direct_contributor_var.set("")
        self.indirect_contributor_var.set("")
        self.profession_entry.delete(0, "end")
        self.monthly_income_entry.delete(0, "end")
        self.income_proof_entry.delete(0, "end")

    #MEMBER ID GENERATOR
    def generate_member_id(self):
        try:
            connection = connect_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT Member_ID FROM Personal_Details ORDER BY Member_ID DESC LIMIT 1")
                result = cursor.fetchone()
                if result:
                    last_id = int(result[0][2:])
                    new_id = f"PH{last_id + 1:03d}"
                else:
                    new_id = "PH001"
                return new_id
        except Error as e:
            messagebox.showerror("Error", f"Error generating member ID: {e}")
        finally:
            if connection and connection.is_connected():
                connection.close()

    #FOR TABLE DISPLAY, LOAD ALL TABLE
    def load_userdata(self):
        for i in self.data_tree.get_children():
            self.data_tree.delete(i)
        
        try: 
            connection = connect_db()
            if connection:
                cursor = connection.cursor()
                
                # Fetch data from Personal_Details and Member_Type tables
                query = """
                    SELECT pd.Member_ID, pd.Members_Name, pd.Mothers_MaidenName, pd.SpouseName, pd.Birthdate, 
                        pd.Birthplace, pd.Sex, pd.Civil_Status, pd.Citizenship, pd.Philsys_IDNum, 
                        pd.TIN, pd.Permanent_Address, pd.Mailing_Address, pd.Home_PhoneNum, 
                        pd.Mobile_Number, pd.Business_DL, pd.Email_Address, 
                        mt.Direct_Contributor, mt.Indirect_Contributor, mt.Profession, mt.Monthly_Income, mt.Income_Proof
                    FROM Personal_Details pd
                    LEFT JOIN Member_Type mt ON pd.Member_ID = mt.Member_ID
                """
                cursor.execute(query)
                rows = cursor.fetchall()
                
                # Insert fetched data into the tree view
                for row in rows:
                    row_list = list(row)
                    row_list[6] = self.reverse_sex_map.get(row_list[6], row_list[6])
                    row_list[7] = self.reverse_civilstatus_map.get(row_list[7], row_list[7])
                    row_list[8] = self.reverse_citizenship_map.get(row_list[8], row_list[8])  
                    row_list[17] = self.reverse_directcontributor_map.get(row_list[17], row_list[17])  
                    row_list[18] = self.reverse_indirectcontributor_map.get(row_list[18], row_list[18])  # Map abbreviation to full word or keep original
                    self.data_tree.insert('', 'end', values=tuple(row_list))

        except Error as e:
            messagebox.showerror("Error", f"Error loading data: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    #TO CENTER MAIN WINDOW
    def form_center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = 1920
        window_height = 1080

        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    #TO ADD DEPENDENTS (DIFFERENT WINDOW)
    def add_dependents(self):
        dependents_window = tk.Toplevel(self)
        dependents_window.title("Add Dependents")
        window_width = 350
        window_height = 300

        screen_width = dependents_window.winfo_screenwidth()
        screen_height = dependents_window.winfo_screenheight()

        x_position = int((screen_width / 2) - (window_width / 2))
        y_position = int((screen_height / 2) - (window_height / 2))

        dependents_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        dependents_window.configure(bg="white")

        form_frame = tk.Frame(dependents_window)
        form_frame.pack(fill=tk.BOTH, expand=True) 

    #FOR FORM - DEPENDENTS
        tk.Label(form_frame, text="Dependents Declaration", font=("Helvetica", 16)).grid(row=0, columnspan=2, sticky="w", padx=5, pady=5)

        tk.Label(form_frame, text="Member ID:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.my_member_id_entry = tk.Entry(form_frame)
        self.my_member_id_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Dependent Name:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.dep_name_entry = tk.Entry(form_frame, width=30)
        self.dep_name_entry.grid(row=3, column=1, padx=5, pady=5)
        self.dependentnamebtn = tk.Button(form_frame, text="?", font=("Helvetica", 10, "bold"), bg = "#D4E7C5", fg="#000000", command = self.show_name)
        self.dependentnamebtn.grid(row=3, column=2, padx=5, pady=5)

        tk.Label(form_frame, text="Relationship:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.relationship_var = tk.StringVar(form_frame)
        self.relationship_dropdown = ttk.Combobox(form_frame, textvariable=self.relationship_var, values=list(self.relationship_map.keys()), state ="readonly")
        self.relationship_dropdown.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Birthdate:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.dep_birthdate_entry = DateEntry(form_frame, width=12, background='darkgreen', foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.dep_birthdate_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Citizenship:").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.citizenship_entry = tk.Entry(form_frame, width=30)
        self.citizenship_entry.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Disability:").grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.disability_var = tk.BooleanVar()
        self.disability_checkbox = tk.Checkbutton(form_frame, variable=self.disability_var)
        self.disability_checkbox.grid(row=7, column=1, padx=5, pady=5)

        # Submit button
        self.submit_button = tk.Button(form_frame, text="Submit", command=lambda:self.submit_dep_form(dependents_window), bg="#1F8D16", fg="white", font=("Helvetica", 12), padx=10, pady=5, borderwidth=2)
        self.submit_button.grid(row=8, column=0, pady=10)

        # Clear button
        self.clear_button = tk.Button(form_frame, text="Clear", command=self.clear_dep_fields, bg="#D84839", fg="white", font=("Helvetica", 12), padx=10, pady=5, borderwidth=2)
        self.clear_button.grid(row=8, column=1, pady=10, sticky="e")

    def submit_dep_form(self, dependents_window):
        dependents_id = self.generate_dependent_id()
        mymemberid = self.my_member_id_entry.get()
        dependent_name = self.dep_name_entry.get()
        relationship_display= self.relationship_var.get()
        relationship = self.relationship_map.get(relationship_display, "")
        dependent_birthdate = self.dep_birthdate_entry.get_date().strftime('%Y-%m-%d')
        dependent_citizenship = self.citizenship_entry.get()
        dependent_disability = self.disability_var.get()

        # Check if any required fields are empty
        if not mymemberid:
            messagebox.showwarning("Warning","Please fill in the member ID.", parent=dependents_window)
            return
        
        #Check if Member ID Exists
        connection = connect_db()
        if connection:
                cursor = connection.cursor()
                query = "SELECT * FROM Personal_Details WHERE Member_ID = %s"
                cursor.execute(query, (mymemberid,))
                if cursor.fetchone() is None:
                    messagebox.showwarning("Warning", "Member ID does not exist.", parent=dependents_window)
                    return
                cursor.close()
                connection.close()

        #RESTRICTIONS     
        if not dependent_name:
            messagebox.showwarning("Warning","Please fill in the dependent name.", parent=dependents_window)
            return
        elif len(dependent_name) < 5:
            messagebox.showwarning("Insufficient Characters", "Dependent Name should be at least 5 characters.", parent=dependents_window)
            return
        elif len(dependent_name) > 100:
            messagebox.showwarning("Exceeded Characters", "Dependent Name should have a maximum of 100 characters.", parent=dependents_window)
            return
        
        if not relationship:
            messagebox.showwarning("Warning", "Please fill in the relationship.", parent=dependents_window)
            return
        if relationship == "CH" and self.calculate_age(dependent_birthdate) > 21:
            messagebox.showwarning("Warning", "Children should be 21 years old or younger.", parent=dependents_window)
            return
        if relationship == "MO" and self.calculate_age(dependent_birthdate) < 60:
            messagebox.showwarning("Warning", "Mother should be 60 years old or above.", parent=dependents_window)
            return
        if relationship == "FA" and self.calculate_age(dependent_birthdate) < 60:
            messagebox.showwarning("Warning", "Father should be 60 years old or above.", parent=dependents_window)
            return

        if not dependent_birthdate:
            messagebox.showwarning("Warning","Please fill in the dependent birthdate.", parent=dependents_window)
            return
        if not dependent_citizenship:
            messagebox.showwarning("Warning","Please fill in the dependent citizenship.", parent=dependents_window)
            return

        try:
            connection = connect_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO Dependents_Declaration (Dependent_ID, Member_ID, Dependent_Name, Relationship, Dependent_Birthdate, Dependent_Citizenship, Dependent_Disability) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                               (dependents_id, mymemberid, dependent_name, relationship, dependent_birthdate, dependent_citizenship, dependent_disability))
                connection.commit()
                self.load_dependents()
                messagebox.showinfo("Success", "Member's Dependent created successfully")
                self.clear_dep_fields()
                dependents_window.destroy()
        except Error as e:
            messagebox.showerror("Error", f"Error creating Member's Dependent: {e}")
        finally:
            if connection and connection.is_connected():
                connection.close()

                
    #CLEAR FIELDS
    def clear_dep_fields(self):
        self.my_member_id_entry.delete(0, tk.END)
        self.dep_name_entry.delete(0, tk.END)
        self.relationship_var.set(" ")
        self.dep_birthdate_entry.delete(0, "end")
        self.citizenship_entry.delete(0, tk.END)
        self.disability_var.set(False)

    #FOR AGE CALCULATION
    def calculate_age(self, birthdate):
        today = date.today()
        birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age
    
    #DEPENDENT ID GENERATOR
    def generate_dependent_id(self):
        try:
            connection = connect_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT Dependent_ID FROM Dependents_Declaration ORDER BY Dependent_ID DESC LIMIT 1")
                result = cursor.fetchone()
                if result:
                    last_id = int(result[0][4:])  # Assuming the ID format starts after the prefix
                    new_id = f"PHMD{last_id + 1:03d}"
                else:
                    new_id = "PHMD001"
                return new_id
        except Error as e:
            messagebox.showerror("Error", f"Error generating dependents ID: {e}")
        finally:
            if connection and connection.is_connected():
                connection.close()
    
    #LOAD TABLE FOR DEPENDENTS TO BE SHOWN IN UI
    def load_dependents(self):
        for i in self.data_tree_dependents.get_children():
            self.data_tree_dependents.delete(i)
        
        try: 
            connection = connect_db()
            if connection:
                cursor = connection.cursor()
                
                # Fetch data from Dependents_Declaration table
                query = """
                    SELECT Dependent_ID, Member_ID, Dependent_Name, Relationship, Dependent_Birthdate, 
                           Dependent_Citizenship, Dependent_Disability
                    FROM Dependents_Declaration
                """
                cursor.execute(query)
                rows = cursor.fetchall()
                
                for row in rows:
                    row_list = list(row)
                    row_list[3] = self.reverse_relationship_map.get(row_list[3], row_list[3]) 
                    self.data_tree_dependents.insert('', 'end', values=tuple(row_list))

        except Error as e:
            messagebox.showerror("Error", f"Error loading dependents data: {e}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection and connection.is_connected():
                connection.close()


if __name__ == "__main__":
    philitout_form = PhilitoutForm()
    philitout_form.mainloop()