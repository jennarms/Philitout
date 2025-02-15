from tkinter import ttk, messagebox
import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import os
from tkcalendar import DateEntry
import mysql.connector
from mysql.connector import Error

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

#WIDGETS FOR UI
class UserEdit(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Edit User")
        self.geometry("1500x600")
        self.attributes("-topmost", True)
        self.configure(bg="white")
        self.center_window()
        self.selected_row = None
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.sex_map = {"Male": "M", "Female": "F"}
        self.reverse_sex_map = {v: k for k, v in self.sex_map.items()}
        self.civilstatus_map = {"Single": "S", "Married": "M", "Legally Seperated": "LS", "Annuled": "A", "Widow/er": "W"}
        self.reverse_civilstatus_map = {v: k for k, v in self.civilstatus_map.items()}
        self.citizenship_map = {"Filipino" : "F", "Dual Citizen": "DC", "Foreign National": "FN"}
        self.reverse_citizenship_map = {v: k for k, v in self.citizenship_map.items()}
        self.direct_contributor_map = {"Employed Private" : "EP", "Employed Government" : " EG", "Professional Practitioner": "PP", "Self-Earning Individual": "SEII", "Self-Earning Individual Sole Proprietor": "SEISP", "Self-Earning Individual Group Enrollment Scheme": "SEIGES", 
                                                        "Kasambahay": "K", "Family Driver": "FD", "Migrant Worker Land Based": "MWLB", "Migrant Worker Sea Based": "MWSB", "Lifetime Member": "LM", "Filipinos with Dual Citizenship": "FWDC", "Foreign National": "FN"}
        self.reverse_direct_contributor_map = {v: k for k, v in self.direct_contributor_map.items()}
        self.indirect_contributor_map = {"Listahan": "L", "4Ps/MCCT": "PM", "Senior Citizen": "SC", "PAMANA": "P", "KIA/KIPO": "KK", "Bangsamoro Normalization": "BN", "LGU-Sponsored": "LGUS", "NGA-Sponsored": "NGAS", "Private-Sponsored": "PS", "Person with Disability": "PWD" }
        self.reverse_indirectcontributor_map = {v: k for k, v in self.indirect_contributor_map.items()}

    #HEADER
        self.header_canvas = tk.Canvas(bg="#D4E7C5", height=80)
        self.header_canvas.pack(fill=tk.X)
        logo_path = 'D:\\2nd Sem\\Information Management\\PHILITOUT\\pictures\\App Logo (70 x 70 px).png'
        logo = Image.open(logo_path)
        logo_image = ImageTk.PhotoImage(logo)
        self.header_canvas.create_image(20, 40, anchor=tk.W, image=logo_image)
        header_label = tk.Label(self.header_canvas, text="PHIL it out! > Edit User", font=("Arial", 24, "bold"), bg="#D4E7C5")
        header_label.place(x=100, y=20)
        self.header_canvas.image = logo_image
    
    #HEADER BUTTONS
        back_button = tk.Button(self.header_canvas, text="Back", command=self.go_back, bg="#D84839", fg="white", font=("Helvetica", 12), padx=10, pady= 5, borderwidth=2)
        back_button.pack(side=tk.RIGHT, padx=20, pady=20)
        instructions_button = tk.Button(self.header_canvas, text="Instructions", command=self.show_instructions, bg="#4285F4", fg="white", font=("Helvetica", 12), padx=10, pady= 5, borderwidth=2)
        instructions_button.pack(side=tk.RIGHT, padx=20, pady=20)

    # FORM
        input_scroll_frame = tk.Frame(self)
        input_scroll_frame.pack(side="left", padx=20, pady=20)
        self.input_canvas = tk.Canvas(input_scroll_frame, borderwidth=0, width=400, height=500, highlightthickness=2, highlightbackground="#1F8D16")
        self.input_frame = tk.Frame(self.input_canvas)
        self.vsb = tk.Scrollbar(input_scroll_frame, orient="vertical", command=self.input_canvas.yview)
        self.input_canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.input_canvas.pack(side="left", fill="both", expand=True)
        self.input_canvas.create_window((0,0), window=self.input_frame, anchor="nw")
        self.input_frame.bind("<Configure>", self.on_frame_configure)
        self.left_frame = tk.Frame(self.input_frame)
        self.create_personal_details()
        self.create_member_type()

    # SEARCH BAR FRAME
        self.search_frame = tk.Frame(self, bg="#FFFFFF")
        self.search_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(self.search_frame, text="Search Member:", bg="white", font=("Helvetica", 12)).pack(side="left", pady=(5, 0), padx=(5, 0))
        self.usersearch_text = tk.Text(self.search_frame, width=25, height=1)
        self.usersearch_text.pack(side="left", pady=(5, 0), padx=(0, 0))
        self.usersearch_button = tk.Button(self.search_frame, text="Search in Table", command=self.usersearch_record, bg="#D4E7C5", fg="#000000", font=("Helvetica", 12), padx=5, pady=5, borderwidth=2)
        self.usersearch_button.pack(side="left", pady=(5, 0), padx=(5, 5))
        self.userviewall_btn = tk.Button(self.search_frame, text="View All", command=self.userview_all_records, bg="#4285F4", fg="white", font=("Helvetica", 12), padx=5, pady=5, borderwidth=2)
        self.userviewall_btn.pack(side="left", pady=(5, 0), padx=(5, 0))
 
        # TABLE UI
        self.middle_frame = tk.Frame(self, bg="#D4E7C5", highlightthickness=2, highlightbackground="#1F8D16")
        self.middle_frame.pack(side="top", padx=20, pady=20, fill="both", expand=False)
        treeview_frame = tk.Frame(self.middle_frame)
        treeview_frame.pack(fill="both", padx=5, pady=5)
        self.data_tree = ttk.Treeview(treeview_frame, columns=(
            "Member ID", "Name", "Mother's Maiden Name", "Spouse", "Birthdate", "Birthplace", "Sex", "Civil Status",
            "Citizenship", "PhilSys ID Number", "TIN", "Permanent Address", "Mailing Address", "Home Phone Number",
            "Mobile Number", "Business Directline", "Email Address", "Direct Contributor", "Indirect Contributor", "Profession", "Monthly Income", "Income Proof"), show="headings", height=15)

        for col in self.data_tree["columns"]:
            self.data_tree.heading(col, text=col)

        vsb_tree = ttk.Scrollbar(treeview_frame, orient="vertical", command=self.data_tree.yview)
        self.data_tree.configure(yscrollcommand=vsb_tree.set)
        vsb_tree.pack(side="right", fill="y")
        hsb_tree = ttk.Scrollbar(treeview_frame, orient="horizontal", command=self.data_tree.xview)
        self.data_tree.configure(xscrollcommand=hsb_tree.set)
        hsb_tree.pack(side="bottom", fill="x")
        
        self.data_tree.pack(expand=True, fill="both")
        self.load_userdata()

        self.data_tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    #BUTTONS 
        self.right_frame = tk.Frame(self, bg = "#FFFFFF")
        self.right_frame.pack(side="left", fill="both", expand=False)
        self.update_button = tk.Button(self.right_frame, text="Update Record", command=self.populate_form_for_update, bg="#1F8D16", fg="white", font=("Helvetica", 12), padx=10, pady= 5, borderwidth=2)
        self.update_button.grid(row=0, column=0, pady=5, padx= 20)
        self.delete_button = tk.Button(self.right_frame, text="Delete Record", command=self.delete_data, bg="#D84839", fg="white", font=("Helvetica", 12), padx=10, pady= 5, borderwidth=2)
        self.delete_button.grid(row=0, column=1, pady=5, padx= 20)
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.summary_button = tk.Button(self.right_frame, text="Summarize Member Record", command=self.summarizeuser, bg="#FDF7C3", fg="#000000", font=("Helvetica", 12), padx=5, pady=5, borderwidth=2)
        self.summary_button.grid(row=0, column=2, pady=5, padx=20)
    
    # SEARCH IN TABLE
    def usersearch_record(self):
            search_term = self.usersearch_text.get("1.0", tk.END).strip()
            if not search_term:
                messagebox.showwarning("Warning", "You did not search any name.")
                return

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
                                row_list[17] = self.reverse_direct_contributor_map.get(row_list[17], row_list[17])
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

    
    #DELETE THE PREVIOUS SEARCH
    def userview_all_records(self):
        self.usersearch_text.delete(1.0, 'end')  # Clear the search entry

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
                        row_list[17] = self.reverse_direct_contributor_map.get(row_list[17], row_list[17])
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
    
    # SUMMARIZE MEMBER FUNCTION
    def summarizeuser(self):
        search_window = tk.Toplevel(self)
        search_window.title("Search Record")
        search_window.attributes("-topmost", True)
        search_window.overrideredirect(True)

        tk.Label(search_window, text="Enter Member ID:").pack(pady=10)
        self.search_entry = tk.Entry(search_window)
        self.search_entry.pack(pady=10)

        search_button = tk.Button(search_window, text="Search", command=self.summarizememberrecord, bg="#4285F4", fg="white", font=("Helvetica", 12), padx=10, pady=5, borderwidth=2)
        search_button.pack(pady=10)

        style = ttk.Style()
        style.configure('Close.TButton', font=('Helvetica', 14), padding=10)
        close_button = ttk.Button(search_window, text="Close", style='Close.TButton', command=search_window.destroy)
        close_button.pack(pady=10, padx=20)

        search_window.configure(borderwidth=5)  
        search_window.update_idletasks()
        window_width = search_window.winfo_width()
        window_height = search_window.winfo_height()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        search_window.geometry(f"+{x}+{y}")

    def summarizememberrecord(self):
        member_id = self.search_entry.get()
        if not member_id:
            messagebox.showwarning("Warning", "Please enter a member ID.")
            return

        try:
            connection = connect_db()
            if connection:
                cursor = connection.cursor()
                query = "SELECT * FROM Personal_Details WHERE Member_ID = %s"
                cursor.execute(query, (member_id,))
                row = cursor.fetchone()
                if row:
                    query = "SELECT * FROM Member_Type WHERE Member_ID = %s"
                    cursor.execute(query, (member_id,))
                    row2 = cursor.fetchone()
                    if row2:
                        dependent_query = "SELECT * FROM Dependents_Declaration WHERE Member_ID = %s"
                        cursor.execute(dependent_query, (member_id,))
                        dependents = cursor.fetchall()
                        dependent_list = []
                        for dependent in dependents:
                            dependent_list.append(f"Dependent Name: {dependent[2]}\nRelationship: {dependent[3]}\nBirthdate: {dependent[4]}\nCitizenship: {dependent[5]}\nDisability: {dependent[6]}\n\n")
                        dependent_str = ''.join(dependent_list)
                        messagebox.showinfo("Search Result", f"Member ID: {row[0]}\nMember Name: {row[1]}\nMother's Maiden Name: {row[2]}\nSpouse Name: {row[3]}\nBirthdate: {row[4]}\nBirthplace: {row[5]}\nSex: {row[6]}\nCivil Status: {row[7]}\nCitizenship: {row[8]}\nPhilsys ID Number: {row[9]}\nTIN: {row[10]}\nPermanent Address: {row[11]}\nMailing Address: {row[12]}\nHome Phone Number: {row[13]}\nMobile Number: {row[14]}\nBusiness DL: {row[15]}\nEmail Address: {row[16]}\n\nDirect Contributor: {row2[1]}\nIndirect Contributor: {row2[2]}\nProfession: {row2[3]}\nMonthly Income: {row2[4]}\nIncome Proof: {row2[5]}\n\nDependents:\n{dependent_str}")
                    else:
                        messagebox.showinfo("Search Result", f"Member ID: {row[0]}\nMember Name: {row[1]}\nMother's Maiden Name: {row[2]}\nSpouse Name: {row[3]}\nBirthdate: {row[4]}\nBirthplace: {row[5]}\nSex: {row[6]}\nCivil Status: {row[7]}\nCitizenship: {row[8]}\nPhilsys ID Number: {row[9]}\nTIN: {row[10]}\nPermanent Address: {row[11]}\nMailing Address: {row[12]}\nHome Phone Number: {row[13]}\nMobile Number: {row[14]}\nBusiness DL: {row[15]}\nEmail Address: {row[16]}\n\nNo record found in Member Type table.\nNo dependents found.")
                else:
                    messagebox.showinfo("Search Result", "No record found.")
        except Error as e:
            messagebox.showerror("Error", f"Error searching record: {e}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection and connection.is_connected():
                connection.close()

    #WHEN X BUTTON IS CLICKED
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you really want to leave PHIL it out?"):
            self.destroy()
    
    #TO LOAD DATA IN TABLE
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
                    row_list[17] = self.reverse_direct_contributor_map.get(row_list[17], row_list[17])  
                    row_list[18] = self.reverse_indirectcontributor_map.get(row_list[18], row_list[18])   # Map abbreviation to full word or keep original
                    self.data_tree.insert('', 'end', values=tuple(row_list)) 

        except Error as e:
            messagebox.showerror("Error", f"Error loading data: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    #WHEN A RECORD IS SELECTED
    def on_tree_select(self, event):
        selected_item = self.data_tree.selection()
        if selected_item:
            self.selected_row = self.data_tree.item(selected_item)['values']
    
    #WHEN UPDATE BUTTON IS CLICKED
    def populate_form_for_update(self):
        if not self.selected_row:
            messagebox.showwarning("No Selection", "You did not select any member to update.")
            return
        
        if self.selected_row:
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, self.selected_row[1])
            
            self.maiden_name_entry.delete(0, tk.END)
            self.maiden_name_entry.insert(0, self.selected_row[2])
            
            self.spouse_entry.delete(0, tk.END)
            self.spouse_entry.insert(0, self.selected_row[3])
            
            self.birthdate_entry.set_date(self.selected_row[4])
            
            self.birthplace_entry.delete(0, tk.END)
            self.birthplace_entry.insert(0, self.selected_row[5])
            
            self.sex_var.set(self.selected_row[6])
            
            self.civil_status_var.set(self.selected_row[7])
            
            self.citizenship_var.set(self.selected_row[8])
            
            self.philsys_id_entry.delete(0, tk.END)
            self.philsys_id_entry.insert(0, self.selected_row[9])
            
            self.tin_entry.delete(0, tk.END)
            self.tin_entry.insert(0, self.selected_row[10])
            
            self.permanent_address_entry.delete(0, tk.END)
            self.permanent_address_entry.insert(0, self.selected_row[11])
            
            self.mailing_address_entry.delete(0, tk.END)
            self.mailing_address_entry.insert(0, self.selected_row[12])
            
            self.home_phone_entry.delete(0, tk.END)
            self.home_phone_entry.insert(0, self.selected_row[13])
            
            self.mobile_entry.delete(0, tk.END)
            self.mobile_entry.insert(0, self.selected_row[14])
            
            self.business_directline_entry.delete(0, tk.END)
            self.business_directline_entry.insert(0, self.selected_row[15])

            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, self.selected_row[16])
            
            self.direct_contributor_var.set(self.selected_row[17])
            self.indirect_contributor_var.set(self.selected_row[18])

            self.profession_entry.delete(0, tk.END)
            self.profession_entry.insert(0, self.selected_row[19])

            self.monthly_income_entry.delete(0, tk.END)
            self.monthly_income_entry.insert(0, self.selected_row[20])

            self.income_proof_entry.delete(0, tk.END)
            self.income_proof_entry.insert(0, self.selected_row[21])
    
    #FOR SAVE CHANGES BUTTON
    def save_changes(self):
        if not self.selected_row:
            messagebox.showwarning("No Selection", "You did not select any member to update.")
            return
        
        if self.selected_row:
            name = self.name_entry.get()
            maiden_name = self.maiden_name_entry.get()
            spouse = self.spouse_entry.get()
            birthdate = self.birthdate_entry.get_date().strftime('%Y-%m-%d')
            birthplace = self.birthplace_entry.get()
            sex_display = self.sex_var.get()  
            sex = self.sex_map.get(sex_display, "")
            civilstatus_display = self.civil_status_var.get()
            civil_status = self.civilstatus_map.get(civilstatus_display, "")
            citizenship_display = self.citizenship_var.get()
            citizenship = self.citizenship_map.get(citizenship_display, "")
            philsys_id = self.philsys_id_entry.get()
            tin = self.tin_entry.get()
            permanent_address = self.permanent_address_entry.get()
            mailing_address = self.mailing_address_entry.get()
            home_phone = self.home_phone_entry.get()
            mobile_number = self.mobile_entry.get()
            business_directline = self.business_directline_entry.get()
            email = self.email_entry.get()
            directcontributor_display = self.direct_contributor_var.get()
            direct_contributor = self.direct_contributor_map.get(directcontributor_display, "")
            indirectcontributor_display = self.indirect_contributor_var.get()
            indirect_contributor = self.indirect_contributor_map.get(indirectcontributor_display, "") 
            profession = self.profession_entry.get()
            monthly_income_str = self.monthly_income_entry.get()
            income_proof = self.income_proof_entry.get()

            #ENTRY RESTRICTIONS
            if not name:
                messagebox.showwarning("Warning", "Please fill in the member name.")
                return
            elif len(name) < 5:
                messagebox.showwarning("Insufficient Characters", "Name should be at least 5 characters.")
                return
            elif len(name) > 100:
                messagebox.showwarning("Exceeded Characters", "Name should have a maximum of 100 characters.")
                return

            
            if not maiden_name:
                messagebox.showwarning("Warning", "Please fill in the mother's maiden name.")
                return
            elif len(maiden_name) < 5:
                messagebox.showwarning("Insufficient Characters", "Mother's maiden name should be at least 5 characters.")
                return
            elif len(maiden_name) > 100:
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
            if not civil_status:
                messagebox.showwarning("Warning", "Please select the civil status.")
                return
            if not citizenship:
                messagebox.showwarning("Warning", "Please fill in the citizenship.")
                return            
            
            if not permanent_address:
                messagebox.showwarning("Warning", "Please fill in the permanent address.")
                return
            elif len(permanent_address) < 10:
                messagebox.showwarning("Insufficient Characters", "Permanent Address should be at least 10 characters.")
                return
            elif len(permanent_address) > 300:
                messagebox.showwarning("Exceeded Characters", "Permanent Address should have a maximum of 100 characters.")
                return

            if not mailing_address:
                messagebox.showwarning("Warning", "Please fill in the mailing address.")
                return
            elif len(mailing_address) < 10:
                messagebox.showwarning("Insufficient Characters", "Mailing Address should be at least 10 characters.")
                return
            elif len(mailing_address) > 300:
                messagebox.showwarning("Exceeded Characters", "Mailing Address should have a maximum of 100 characters.")
                return
            
            if not mobile_number:
                messagebox.showwarning("Warning", "Please fill in the mobile number.")
                return
            if not email:
                messagebox.showwarning("Warning", "Please fill in the email address.")
                return
            if not (direct_contributor or indirect_contributor):
                messagebox.showwarning("Warning", "Please specify if the member is a direct or indirect contributor.")
                return

            # Validate monthly income
            try:
                monthly_income = float(monthly_income_str)  # Try to convert to float
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid numeric value for monthly income. If none, please type \"0\".")
                return

            try:
                # Ask for confirmation
                confirmed = messagebox.askyesno("Confirm Update", "Are you sure you want to save changes?")
                if not confirmed:
                    return
                
                connection = connect_db()
                if connection:
                    cursor = connection.cursor()
                    update_personal_details_query = """
                        UPDATE Personal_Details
                        SET Members_Name = %s, Mothers_MaidenName = %s, SpouseName = %s, Birthdate = %s, Birthplace = %s, 
                            Sex = %s, Civil_Status = %s, Citizenship = %s, Philsys_IDNum = %s, TIN = %s, 
                            Permanent_Address = %s, Mailing_Address = %s, Home_PhoneNum = %s, Mobile_Number = %s, 
                            Business_DL = %s, Email_Address = %s
                        WHERE Member_ID = %s
                    """
                    cursor.execute(update_personal_details_query, (name, maiden_name, spouse, birthdate, birthplace, sex, civil_status, citizenship, philsys_id, tin, permanent_address, mailing_address, home_phone, mobile_number, business_directline, email, self.selected_row[0]))
                    
                    update_member_type_query = """
                        UPDATE Member_Type
                        SET Direct_Contributor = %s, Indirect_Contributor = %s, Profession = %s, Monthly_Income = %s, Income_Proof = %s
                        WHERE Member_ID = %s
                    """
                    cursor.execute(update_member_type_query, (direct_contributor, indirect_contributor, profession, monthly_income, income_proof, self.selected_row[0]))
                    
                    connection.commit()
                    messagebox.showinfo("Success", "Record updated successfully.")
                    self.load_userdata()
                    self.clear_fields()
            except Error as e:
                messagebox.showerror("Error", f"Error updating data: {e}")
            finally:
                if 'cursor' in locals() and cursor:
                    cursor.close()
                if 'connection' in locals() and connection and connection.is_connected():
                    connection.close()
    
    #CLEAR FIELDS
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
    
    #DELETE BUTTON
    def delete_data(self):
        if not self.selected_row:
            messagebox.showwarning("No Selection", "You did not select any member to delete.")
            return
        
        try:
            confirmed = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this record?")
            if not confirmed:
                return
            
            connection = connect_db()
            if connection:
                cursor = connection.cursor()
                delete_personal_details_query = "DELETE FROM Personal_Details WHERE Member_ID = %s"
                cursor.execute(delete_personal_details_query, (self.selected_row[0],))
                
                delete_member_type_query = "DELETE FROM Member_Type WHERE Member_ID = %s"
                cursor.execute(delete_member_type_query, (self.selected_row[0],))
                
                connection.commit()
                messagebox.showinfo("Success", "Record deleted successfully.")
                self.load_userdata()
        except Error as e:
            messagebox.showerror("Error", f"Error deleting data: {e}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection and connection.is_connected():
                connection.close()

    #SHOW INSTRUCTIONS BUTTON
    def show_instructions(self):
        instructions_window = tk.Toplevel(self)
        instructions_window.title("Instructions")
        instructions_window.attributes("-topmost", True)
        instructions_window.overrideredirect(True)
        try:
            instructions_image_path = "D:\\2nd Sem\\Information Management\\PHILITOUT\\pictures\\Instructions (1300 x 500 px).png"
            instructions_image = Image.open(instructions_image_path)
            instructions_photo = ImageTk.PhotoImage(instructions_image)
            instructions_label = tk.Label(instructions_window, image=instructions_photo)
            instructions_label.image = instructions_photo
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
    
    #WIDGETS FOR FORM
    def create_personal_details(self):
        tk.Label(self.left_frame, text="Personal Details", font=("Helvetica", 16)).grid(row=0, columnspan=2, sticky="w", padx=5, pady=5)

        tk.Label(self.left_frame, text="Name:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.name_entry = tk.Entry(self.left_frame)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)
        self.namebtn = tk.Button(self.left_frame, text="?", font=("Helvetica", 10, "bold"), bg = "#D4E7C5", fg="#000000", command = self.show_name)
        self.namebtn.grid(row=1, column=2, padx=5, pady=5)

        tk.Label(self.left_frame, text="Mother's Maiden Name:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.maiden_name_entry = tk.Entry(self.left_frame)
        self.maiden_name_entry.grid(row=2, column=1, padx=5, pady=5)
        self.mothermaidennamebtn = tk.Button(self.left_frame, text="?", font=("Helvetica", 10, "bold"), bg = "#D4E7C5", fg="#000000", command = self.show_name)
        self.mothermaidennamebtn.grid(row=2, column=2, padx=5, pady=5)

        tk.Label(self.left_frame, text="Spouse:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.spouse_entry = tk.Entry(self.left_frame)
        self.spouse_entry.grid(row=3, column=1, padx=5, pady=5)
        self.spousenamebtn = tk.Button(self.left_frame, text="?", font=("Helvetica", 10, "bold"), bg = "#D4E7C5", fg="#000000", command = self.show_name)
        self.spousenamebtn.grid(row=3, column=2, padx=5, pady=5)
        tk.Label(self.left_frame, text="~", font=("Helvetica", 15, "italic bold"), fg="#1F8D16").grid(row=3, column=3, sticky="w", padx=5, pady=5)

        tk.Label(self.left_frame, text="Birthdate:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.birthdate_entry = DateEntry(self.left_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.birthdate_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.left_frame, text="Birthplace:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.birthplace_entry = tk.Entry(self.left_frame)
        self.birthplace_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self.left_frame, text="Sex:").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.sex_var = tk.StringVar(self.left_frame)
        self.sex_dropdown = ttk.Combobox(self.left_frame, textvariable=self.sex_var, values=list(self.sex_map.keys()), state ="readonly")
        self.sex_dropdown.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(self.left_frame, text="Civil Status:").grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.civil_status_var = tk.StringVar(self.left_frame)
        self.civil_status_dropdown = ttk.Combobox(self.left_frame, textvariable=self.civil_status_var, values=list(self.civilstatus_map.keys()), state ="readonly")
        self.civil_status_dropdown.grid(row=7, column=1, padx=5, pady=5)

        tk.Label(self.left_frame, text="Citizenship:").grid(row=8, column=0, sticky="w", padx=5, pady=5)
        self.citizenship_var = tk.StringVar(self.left_frame)
        self.citizenship_dropdown = ttk.Combobox(self.left_frame, textvariable=self.citizenship_var, values=list(self.citizenship_map.keys()), state ="readonly")
        self.citizenship_dropdown.grid(row=8, column=1, padx=5, pady=5)

        tk.Label(self.left_frame, text="PhilSys ID Number:").grid(row=9, column=0, sticky="w", padx=5, pady=5)
        self.philsys_id_entry = tk.Entry(self.left_frame)
        self.philsys_id_entry.grid(row=9, column=1, padx=5, pady=5)
        tk.Label(self.left_frame, text="~", font=("Helvetica", 15, "italic bold"), fg="#1F8D16").grid(row=9, column=2, sticky="w", padx=5, pady=5)

        tk.Label(self.left_frame, text="TIN:").grid(row=10, column=0, sticky="w", padx=5, pady=5)
        self.tin_entry = tk.Entry(self.left_frame)
        self.tin_entry.grid(row=10, column=1, padx=5, pady=5)
        tk.Label(self.left_frame, text="~", font=("Helvetica", 15, "italic bold"), fg="#1F8D16").grid(row=10, column=2, sticky="w", padx=5, pady=5)

        tk.Label(self.left_frame, text="Permanent Address:").grid(row=11, column=0, sticky="w", padx=5, pady=5)
        self.permanent_address_entry = tk.Entry(self.left_frame)
        self.permanent_address_entry.grid(row=11, column=1, padx=5, pady=5)
        self.permaddbtn = tk.Button(self.left_frame, text="?", font=("Helvetica", 10, "bold"), bg = "#D4E7C5", fg="#000000", command = self.show_address)
        self.permaddbtn.grid(row=11, column=2, padx=5, pady=5)

        tk.Label(self.left_frame, text="Mailing Address:").grid(row=12, column=0, sticky="w", padx=5, pady=5)
        self.mailing_address_entry = tk.Entry(self.left_frame)
        self.mailing_address_entry.grid(row=12, column=1, padx=5, pady=5)
        self.mailaddbtn = tk.Button(self.left_frame, text="?", font=("Helvetica", 10, "bold"), bg = "#D4E7C5", fg="#000000", command = self.show_address)
        self.mailaddbtn.grid(row=12, column=2, padx=5, pady=5)

        tk.Label(self.left_frame, text="Home Phone Number:").grid(row=13, column=0, sticky="w", padx=5, pady=5)
        self.home_phone_entry = tk.Entry(self.left_frame)
        self.home_phone_entry.grid(row=13, column=1, padx=5, pady=5)
        tk.Label(self.left_frame, text="~", font=("Helvetica", 15, "italic bold"), fg="#1F8D16").grid(row=13, column=2, sticky="w", padx=5, pady=5)

        tk.Label(self.left_frame, text="Mobile Number:").grid(row=14, column=0, sticky="w", padx=5, pady=5)
        self.mobile_entry = tk.Entry(self.left_frame)
        self.mobile_entry.grid(row=14, column=1, padx=5, pady=5)

        tk.Label(self.left_frame, text="Business Directline:").grid(row=15, column=0, sticky="w", padx=5, pady=5)
        self.business_directline_entry = tk.Entry(self.left_frame)
        self.business_directline_entry.grid(row=15, column=1, padx=5, pady=5)
        tk.Label(self.left_frame, text="~", font=("Helvetica", 15, "italic bold"), fg="#1F8D16").grid(row=15, column=2, sticky="w", padx=5, pady=5)

        tk.Label(self.left_frame, text="Email Address:").grid(row=16, column=0, sticky="w", padx=5, pady=5)
        self.email_entry = tk.Entry(self.left_frame)
        self.email_entry.grid(row=16, column=1, padx=5, pady=5)

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

        tk.Label(self.left_frame, text="Member Type", font=("Helvetica", 16)).grid(row=17, columnspan=2, sticky="w", padx=5, pady=5)

        self.contributor_type_var = tk.StringVar(value=0)

        tk.Radiobutton(self.left_frame, text="Direct Contributor", variable=self.contributor_type_var, value="Direct", command=self.update_contributor_type).grid(row=18, column=0, sticky="w", padx=5, pady=5)
        tk.Radiobutton(self.left_frame, text="Indirect Contributor", variable=self.contributor_type_var, value="Indirect", command=self.update_contributor_type).grid(row=18, column=1, sticky="w", padx=5, pady=5)

        self.direct_contributor_var = tk.StringVar(self.left_frame)
        self.direct_contributor_dropdown = ttk.Combobox(self.left_frame, textvariable=self.direct_contributor_var, values=list(self.direct_contributor_map.keys()))
        self.direct_contributor_dropdown.grid(row=19, column=0, padx=5, pady=5)

        self.indirect_contributor_var = tk.StringVar(self.left_frame)
        self.indirect_contributor_dropdown = ttk.Combobox(self.left_frame, textvariable=self.indirect_contributor_var, values=list(self.indirect_contributor_map.keys()))
        self.indirect_contributor_dropdown.grid(row=19, column=1, padx=5, pady=5)

        self.update_contributor_type()

        tk.Label(self.left_frame, text="Profession:").grid(row=20, column=0, sticky="w", padx=5, pady=5)
        self.profession_entry = tk.Entry(self.left_frame)
        self.profession_entry.grid(row=20, column=1, padx=5, pady=5)

        tk.Label(self.left_frame, text="Monthly Income:").grid(row=21, column=0, sticky="w", padx=5, pady=5)
        self.monthly_income_entry = tk.Entry(self.left_frame)
        self.monthly_income_entry.grid(row=21, column=1, padx=5, pady=5)

        tk.Label(self.left_frame, text="Income Proof:").grid(row=22, column=0, sticky="w", padx=5, pady=5)
        self.income_proof_entry = tk.Entry(self.left_frame)
        self.income_proof_entry.grid(row=22, column=1, padx=5, pady=5)
        self.incomeproofbtn = tk.Button(self.left_frame, text="?", font=("Helvetica", 10, "bold"), bg = "#D4E7C5", fg="#000000", command = self.show_incomeproof)
        self.incomeproofbtn.grid(row=22, column=2, padx=5, pady=5)

        self.savechanges_button = tk.Button(self.left_frame, text="Save Changes", command=self.save_changes, bg="#1F8D16", fg="white", font=("Helvetica", 12), padx=10, pady= 5, borderwidth=2)
        self.savechanges_button.grid(row=30, columnspan=2, pady=10)
        self.left_frame.pack(padx=20, pady=20)
    
    #FOR ? BUTTON - ADDRESS FORMAT
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

    #FOR ? BUTTON - NAME FORMAT
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

    #FOR ? BUTTON - ACCEPTED INCOME PROOF
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

    #TO CENTER EDIT USERS WINDOW
    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 1500) // 2
        y = (screen_height - 600) // 2
        self.geometry("1500x600+{}+{}".format(x, y))

    def on_frame_configure(self, event):
        self.input_canvas.configure(scrollregion=self.input_canvas.bbox("all"))

if __name__ == "__main__":
    user_edit = UserEdit()
    user_edit.mainloop()