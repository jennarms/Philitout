import tkinter as tk
from tkinter import ttk, messagebox
from mysql.connector import Error
import mysql.connector
from PIL import Image, ImageTk
import subprocess
import os


class DoQuery(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Execute SQL Query")
        self.geometry("1500x600")
        self.create_header()
        self.initialize_ui()
        self.center_window()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    #WHEN X BUTTON IS CLICKED
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you really want to leave PHIL it out?"):
            self.destroy()

    #WIDGETS FOR UI - HEADER
    def create_header(self):
        self.header_canvas = tk.Canvas(bg="#D4E7C5", height=80)
        self.header_canvas.pack(fill=tk.X)

        logo_path = 'D:\\2nd Sem\\Information Management\\PHILITOUT\\pictures\\App Logo (70 x 70 px).png'
        logo = Image.open(logo_path)
        logo_image = ImageTk.PhotoImage(logo)
        self.header_canvas.create_image(20, 40, anchor=tk.W, image=logo_image)
        header_label = tk.Label(self.header_canvas, text="PHIL it out! > SQL Query", font=("Arial", 24, "bold"), bg="#D4E7C5")
        header_label.place(x=100, y=20)
        self.header_canvas.image = logo_image

        back_button = tk.Button(self.header_canvas, text="Back", command=self.go_back, bg="#D84839", fg="white", font=("Helvetica", 12), padx=10, pady=5, borderwidth=2)
        back_button.pack(side=tk.RIGHT, padx=20, pady=20)

        details_button = tk.Button(self.header_canvas, text="Database Details", command=self.database_details, bg="#1F8D16", fg="white", font=("Helvetica", 12), padx=10, pady= 5, borderwidth=2)
        details_button.pack(side=tk.RIGHT, padx=20, pady=20)
    
    #DATABASE DETAILS BUTTON
    def database_details(self):
        databasedetails_window = tk.Toplevel(self)
        databasedetails_window.title("Database Details")
        databasedetails_window.attributes("-topmost", True)
        databasedetails_window.overrideredirect(True)

        try:
            image_paths = [
                "D:\\2nd Sem\\Information Management\\PHILITOUT\\pictures\\Database Description (1300 x 500 px)\\1.png",
                "D:\\2nd Sem\\Information Management\\PHILITOUT\\pictures\\Database Description (1300 x 500 px)\\2.png",
                "D:\\2nd Sem\\Information Management\\PHILITOUT\\pictures\\Database Description (1300 x 500 px)\\3.png",
                "D:\\2nd Sem\\Information Management\\PHILITOUT\\pictures\\Database Description (1300 x 500 px)\\4.png"
            ]

            current_image_index = 0
            total_images = len(image_paths)

            databasedetails_label = tk.Label(databasedetails_window)
            databasedetails_label.pack()

            def show_image(index):
                nonlocal current_image_index
                current_image_index = index % total_images  # Wrap around images
                image_path = image_paths[current_image_index]
                databasedetails_image = Image.open(image_path)
                databasedetails_photo = ImageTk.PhotoImage(databasedetails_image)

                databasedetails_label.config(image=databasedetails_photo)
                databasedetails_label.image = databasedetails_photo

            show_image(current_image_index)

            #NEXT BUTTON >
            def move_next():
                nonlocal current_image_index
                current_image_index += 1
                show_image(current_image_index)
            
            #BACK BUTTON <
            def move_back():
                nonlocal current_image_index
                current_image_index -= 1
                show_image(current_image_index)

            back_button = tk.Button(databasedetails_window, text="◄", command=move_back, width=8, bg="#D4E7C5", fg="#000000", font=('Helvetica', 14))
            back_button.pack(side=tk.LEFT, padx=20, pady=20)

            proceed_button = tk.Button(databasedetails_window, text="►", command=move_next, width=8, bg="#D4E7C5", fg="#000000", font=('Helvetica', 14))
            proceed_button.pack(side=tk.RIGHT, padx=20, pady=20)

            close_button = tk.Button(databasedetails_window, text="Close", command=databasedetails_window.destroy, width=8, font=('Helvetica', 14))
            close_button.pack(pady=20)

        except Exception as e:
            messagebox.showerror("Error", f"Error displaying instructions: {e}")

        databasedetails_window.configure(borderwidth=5)  
        databasedetails_window.update_idletasks()
        window_width = databasedetails_window.winfo_width()
        window_height = databasedetails_window.winfo_height()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        databasedetails_window.geometry(f"+{x}+{y}")
    
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

    #WIDGETS FOR UI - QUERY EXECUTER
    def initialize_ui(self):
        tk.Label(self, text="Enter your SQL query below:", font=("Helvetica", 12, "italic bold")).pack(pady=10)
        
        self.query_text = tk.Text(self, height=5, width=70)
        self.query_text.pack(pady=10)
        
        execute_button = tk.Button(self, text="Execute", command=self.execute_query, bg="#1F8D16", fg="white", font=("Helvetica", 12, "bold"), padx=10, pady=5, borderwidth=2)
        execute_button.pack(pady=10)
        
        self.result_tree = ttk.Treeview(self)
        self.result_tree.pack(fill="both", expand=True, pady=20)
    
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

    #EXECUTE BUTTON
    def execute_query(self):
        query = self.query_text.get("1.0", tk.END).strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a SQL query.")
            return
        
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
    
    #TO CENTER DO QUERY WINDOW
    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 1500) // 2
        y = (screen_height - 600) // 2
        self.geometry("1500x600+{}+{}".format(x, y))

if __name__ == "__main__":
    do_query = DoQuery()
    do_query.mainloop()
