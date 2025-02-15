from tkinter import ttk, messagebox
import tkinter as tk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import subprocess
import os
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

#WIDGETS FOR UI
class DepsEdit(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Edit Dependents")
        self.geometry("1500x600")
        self.attributes("-topmost", True)
        self.configure(bg="white")
        self.center_window()
        self.selected_row = None
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.relationship_map = {"Living Spouse" : "LVSP", "Mother": "MO", "Father": "FA", "Child": "CH"}
        self.reverse_relationship_map = {v: k for k, v in self.relationship_map.items()}

    #HEADER
        self.header_canvas = tk.Canvas(bg="#D4E7C5", height=80)
        self.header_canvas.pack(fill=tk.X)
        logo_path = 'D:\\2nd Sem\\Information Management\\PHILITOUT\\pictures\\App Logo (70 x 70 px).png'
        logo = Image.open(logo_path)
        logo_image = ImageTk.PhotoImage(logo)
        self.header_canvas.create_image(20, 40, anchor=tk.W, image=logo_image)
        header_label = tk.Label(self.header_canvas, text="PHIL it out! > Edit Dependents", font=("Arial", 24, "bold"), bg="#D4E7C5")
        header_label.place(x=100, y=20)
        self.header_canvas.image = logo_image
    
    #HEADER BUTTONS    
        back_button = tk.Button(self.header_canvas, text="Back", command=self.go_back, bg="#D84839", fg="white", font=("Helvetica", 12), padx=10, pady=5, borderwidth=2)
        back_button.pack(side=tk.RIGHT, padx=20, pady=20)
        instructions_button = tk.Button(self.header_canvas, text="Instructions", command=self.show_instructions, bg="#4285F4", fg="white", font=("Helvetica", 12), padx=10, pady=5, borderwidth=2)
        instructions_button.pack(side=tk.RIGHT, padx=20, pady=20)

    #FORM
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
        self.create_dependent_declaration()

    # SEARCH BAR FRAME
        self.search_frame = tk.Frame(self, bg="#FFFFFF")
        self.search_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(self.search_frame, text="Search Dependent:", bg="white", font=("Helvetica", 12)).pack(side="left", pady=(5, 0), padx=(5, 0))
        self.search_text = tk.Text(self.search_frame, width=25, height=1)
        self.search_text.pack(side="left", pady=(5, 0), padx=(0, 0))
        self.search_button = tk.Button(self.search_frame, text="Search in Table", command=self.dep_search_record, bg="#D4E7C5", fg="#000000", font=("Helvetica", 12), padx=5, pady=5, borderwidth=2)
        self.search_button.pack(side="left", pady=(5, 0), padx=(5, 5))
        self.viewall_btn = tk.Button(self.search_frame, text="View All", command=self.view_all_records, bg="#4285F4", fg="white", font=("Helvetica", 12), padx=5, pady=5, borderwidth=2)
        self.viewall_btn.pack(side="left", pady=(5, 0), padx=(5, 5))
    
    #TABLE UI
        self.middle_frame = tk.Frame(self, bg = "#D4E7C5", highlightthickness=2, highlightbackground="#1F8D16")
        self.middle_frame.pack(side="top", padx=20, pady=20, fill="both", expand=False)
        dep_treeview_frame = tk.Frame(self.middle_frame)
        dep_treeview_frame.pack(fill="both", padx=5, pady=5)
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

        self.data_tree_dependents.pack(expand=True, fill="both")
        self.load_dependents()
        self.data_tree_dependents.bind("<<TreeviewSelect>>", self.on_tree_select)

        #BUTTONS 
        self.right_frame = tk.Frame(self, bg = "#FFFFFF")
        self.right_frame.pack(side="left", fill="both", expand=False)
        self.update_button = tk.Button(self.right_frame, text="Update Record", command=self.populate_form_for_update, bg="#1F8D16", fg="white", font=("Helvetica", 12), padx=10, pady=5, borderwidth=2)
        self.update_button.grid(row=0, column=0, pady=5, padx=20)
        self.delete_button = tk.Button(self.right_frame, text="Delete Record", command=self.delete_data, bg="#D84839", fg="white", font=("Helvetica", 12), padx=10, pady=5, borderwidth=2)
        self.delete_button.grid(row=0, column=1, pady=5, padx=20)
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.summary_button = tk.Button(self.right_frame, text="Summarize Dependent Record", command=self.summarizedependent, bg="#FDF7C3", fg="#000000", font=("Helvetica", 12), padx=5, pady=5, borderwidth=2)
        self.summary_button.grid(row=0, column=2, pady=5, padx=20)

    #SEARCH IN TABLE
    def dep_search_record(self):
        search_term = self.search_text.get("1.0", tk.END).strip()
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
    def view_all_records(self):
        self.search_text.delete(1.0, 'end')  # Clear the search entry

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
    
    #SUMMARIZE DEPENDENT FUNCTION
    def summarizedependent(self):
        search_window = tk.Toplevel(self)
        search_window.title("Search Record")
        search_window.attributes("-topmost", True)
        search_window.overrideredirect(True)

        tk.Label(search_window, text="Enter Dependent ID:").pack(pady=10)
        self.search_entry = tk.Entry(search_window)
        self.search_entry.pack(pady=10)

        search_button = tk.Button(search_window, text="Search", command=self.summarizedependentrecord, bg="#4285F4", fg="white", font=("Helvetica", 12), padx=10, pady=5, borderwidth=2)
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

    def summarizedependentrecord(self):
        dependent_id = self.search_entry.get()
        if not dependent_id:
            messagebox.showwarning("Warning", "Please enter a dependent ID.")
            return

        try:
            connection = connect_db()
            if connection:
                cursor = connection.cursor()
                query = "SELECT * FROM Dependents_Declaration WHERE Dependent_ID = %s"
                cursor.execute(query, (dependent_id,))
                row = cursor.fetchone()
                if row:
                    query = "SELECT Members_Name FROM Personal_Details WHERE Member_ID = %s"
                    cursor.execute(query, (row[1],))
                    member_name = cursor.fetchone()[0]
                    messagebox.showinfo("Search Result", f"Dependent of Member: {member_name}\nDependent ID: {row[0]}\nMember ID: {row[1]}\nDependent Name: {row[2]}\nRelationship: {row[3]}\nDependent Birthdate: {row[4]}\nDependent Citizenship: {row[5]}\nDependent Disability: {row[6]}")
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

    #LOAD DEPENDENTS ON TABLE
    def load_dependents(self):
        for i in self.data_tree_dependents.get_children():
            self.data_tree_dependents.delete(i)
        
        try: 
            connection = connect_db()
            if connection:
                cursor = connection.cursor()
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

    #WHEN A RECORD IS SELECTED ON TABLE
    def on_tree_select(self, event):
        selected_item = self.data_tree_dependents.selection()
        if selected_item:
            self.selected_row = self.data_tree_dependents.item(selected_item)['values']

    #UPDATE BUTTON
    def populate_form_for_update(self):
        if not self.selected_row:
            messagebox.showwarning("No Selection", "You did not select any dependent to update.")
            return

        if self.selected_row:
            self.my_member_id_entry.delete(0, tk.END)
            self.my_member_id_entry.insert(0, self.selected_row[1])

            self.dep_name_entry.delete(0, tk.END)
            self.dep_name_entry.insert(0, self.selected_row[2])

            self.relationship_var.set(self.selected_row[3])

            self.dep_birthdate_entry.set_date(self.selected_row[4])

            self.citizenship_entry.delete(0, tk.END)
            self.citizenship_entry.insert(0, self.selected_row[5])
            
            self.disability_var.set(bool(self.selected_row[6]))

    #SAVE CHANGES BUTTON
    def save_changes(self):
        if not self.selected_row:
            messagebox.showwarning("No Selection", "You did not select any dependent to update.")
            return
        
        if self.selected_row:
            updated_my_member_id = self.my_member_id_entry.get()
            updated_name = self.dep_name_entry.get()
            update_relationship_display= self.relationship_var.get()
            updated_relationship = self.relationship_map.get(update_relationship_display, "")
            updated_birthdate = self.dep_birthdate_entry.get_date().strftime('%Y-%m-%d')
            updated_citizenship = self.citizenship_entry.get()
            updated_disability = self.disability_var.get()

            if not updated_my_member_id:
                messagebox.showwarning("Warning", "Please fill in the member ID.")
                return
            
            #Check if Member ID Exists
            connection = connect_db()
            if connection:
                cursor = connection.cursor()
                query = "SELECT * FROM Personal_Details WHERE Member_ID = %s"
                cursor.execute(query, (updated_my_member_id,))
                if cursor.fetchone() is None:
                    messagebox.showwarning("Warning", "Member ID does not exist.")
                    return
                cursor.close()
                connection.close()
            
            if not updated_name:
                messagebox.showwarning("Warning", "Please fill in the dependent name.")
                return
            elif len(updated_name) < 5:
                messagebox.showwarning("Insufficient Characters", "Dependent Name should be at least 5 characters.")
                return
            elif len(updated_name) > 100:
                messagebox.showwarning("Exceeded Characters", "Dependent Name should have a maximum of 100 characters.")
                return
        
            if not updated_relationship:
                messagebox.showwarning("Warning", "Please fill in the relationship.")
                return
            # Additional conditions based on age and relationship
            if updated_relationship == "Children" and self.calculate_age(updated_birthdate) <= 21:
                messagebox.showwarning("Warning", "Children should be 21 years old or younger.")
                return
            if updated_relationship == "Mother" and self.calculate_age(updated_birthdate) >= 60:
                messagebox.showwarning("Warning", "Mother should be 60 years old or above.")
                return
            if updated_relationship == "Father" and self.calculate_age(updated_birthdate) >= 60:
                messagebox.showwarning("Warning", "Father should be 60 years old or above.")
                return
        
        
            if not updated_birthdate:
                messagebox.showwarning("Warning", "Please fill in the dependent birthdate.")
                return
            if not updated_citizenship:
                messagebox.showwarning("Warning", "Please fill in the dependent citizenship.")
                return

            try:
                # Ask for confirmation
                confirmed = messagebox.askyesno("Confirm Update", "Are you sure you want to save changes?")
                if not confirmed:
                    return
                
                connection = connect_db()
                if connection:
                    cursor = connection.cursor()
                    query = """
                        UPDATE Dependents_Declaration
                        SET Member_ID = %s, Dependent_Name = %s, Relationship = %s, Dependent_Birthdate = %s,
                            Dependent_Citizenship = %s, Dependent_Disability = %s
                        WHERE Dependent_ID = %s
                    """
                    cursor.execute(query, (updated_my_member_id, updated_name, updated_relationship, updated_birthdate, updated_citizenship, updated_disability, self.selected_row[0]))
                    connection.commit()
                    messagebox.showinfo("Success", "Record updated successfully.")
                    self.load_dependents()
                    self.clear_dep_fields()
            except Error as e:
                messagebox.showerror("Error", f"Error updating record: {e}")
            finally:
                if 'cursor' in locals() and cursor:
                    cursor.close()
                if 'connection' in locals() and connection and connection.is_connected():
                    connection.close()
    
    #AGE CALCULATOR
    def calculate_age(self, birthdate):
        today = date.today()
        birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age

    #CLEAR FIELDS
    def clear_dep_fields(self):
        self.my_member_id_entry.delete(0, tk.END)
        self.dep_name_entry.delete(0, tk.END)
        self.relationship_var.set(" ")
        self.dep_birthdate_entry.delete(0, "end")
        self.citizenship_entry.delete(0, tk.END)
        self.disability_var.set(False)

    #DELETE BUTTON
    def delete_data(self):
        if not self.selected_row:
            messagebox.showwarning("No Selection", "You did not select any dependent to delete.")
            return

        try:
            confirmed = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this record?")
            if not confirmed:
                return

            connection = connect_db()
            if connection:
                cursor = connection.cursor()
                query = "DELETE FROM Dependents_Declaration WHERE Dependent_ID = %s"
                cursor.execute(query, (self.selected_row[0],))
                connection.commit()
                messagebox.showinfo("Success", "Record deleted successfully.")
                self.load_dependents()
        except Error as e:
            messagebox.showerror("Error", f"Error deleting record: {e}")
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

    def create_dependent_declaration(self):
    
    #WIDGETS FOR FORM
        tk.Label(self.left_frame, text="Dependents Declaration", font=("Helvetica", 16)).grid(row=1, columnspan=2, sticky="w", padx=5, pady=5)
        
        tk.Label(self.left_frame, text="Member ID:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.my_member_id_entry = tk.Entry(self.left_frame)
        self.my_member_id_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(self.left_frame, text="Dependent Name").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.dep_name_entry = tk.Entry(self.left_frame)
        self.dep_name_entry.grid(row=3, column=1, padx=5, pady=5)
        self.namebtn = tk.Button(self.left_frame, text="?", font=("Helvetica", 10, "bold"), bg = "#D4E7C5", fg="#000000", command = self.show_name)
        self.namebtn.grid(row=3, column=2, padx=5, pady=5)
        
        tk.Label(self.left_frame, text="Relationship").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.relationship_var = tk.StringVar(self.left_frame)
        self.relationship_dropdown = ttk.Combobox(self.left_frame, textvariable=self.relationship_var, values=list(self.relationship_map.keys()), state ="readonly")
        self.relationship_dropdown.grid(row=4, column=1, padx=5, pady=5)
         
        tk.Label(self.left_frame, text="Birthdate").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.dep_birthdate_entry = DateEntry(self.left_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.dep_birthdate_entry.grid(row=5, column=1, padx=5, pady=5)
        
        tk.Label(self.left_frame, text="Citizenship").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.citizenship_entry = tk.Entry(self.left_frame)
        self.citizenship_entry.grid(row=6, column=1, padx=5, pady=5)
        
        tk.Label(self.left_frame, text="Disability").grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.disability_var = tk.BooleanVar()
        self.disability_checkbox = tk.Checkbutton(self.left_frame, variable=self.disability_var)
        self.disability_checkbox.grid(row=7, column=1, padx=5, pady=5)
        
        self.savechanges_button = tk.Button(self.left_frame, text="Save Changes", command=self.save_changes, bg="#1F8D16", fg="white", font=("Helvetica", 12), padx=10, pady=5, borderwidth=2)
        self.savechanges_button.grid(row=8, columnspan=2, pady=10)
        self.left_frame.pack(padx=20, pady=20)
    
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

    #TO CENTER EDIT DEPS WINDOW
    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 1500) // 2
        y = (screen_height - 600) // 2
        self.geometry("1500x600+{}+{}".format(x, y))

    def on_frame_configure(self, event):
        self.input_canvas.configure(scrollregion=self.input_canvas.bbox("all"))

if __name__ == "__main__":
    user_edit = DepsEdit()
    user_edit.mainloop()