import tkinter as tk
from tkinter import ttk
import subprocess
from tkinter import messagebox
from PIL import Image, ImageTk

class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Splash Screen")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.after(3000, self.close_splash)

        self.image_path = "D:\\2nd Sem\\Information Management\\PHILITOUT\\pictures\\Landscape logo (500 x 300 px).png"
        self.logo = tk.PhotoImage(file=self.image_path)
        self.label_logo = ttk.Label(root, image=self.logo)
        self.label_logo.pack()

        self.center_window()
        
    #TO CENTER SPLASHSCREEN
    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - 500) // 2
        y = (screen_height - 300) // 2

        self.root.geometry("500x300+{}+{}".format(x, y))

    #TO CLOSE SPLASH
    def close_splash(self):
        self.root.destroy()
        welcome_root = tk.Tk()
        welcome_page = WelcomePage(welcome_root)
        welcome_root.mainloop()

class WelcomePage:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1500x600")
        self.root.title("Welcome to PHIL it out!")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        try:
            self.background_image = tk.PhotoImage(file="D:\\2nd Sem\\Information Management\\PHILITOUT\\pictures\\Welcome Page (1500 x 600 px).png")
            print("Image loaded successfully.")
        except Exception as e:
            print("Error loading image:", e)

        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.center_window()

        # Add Access Form button
        access_button = tk.Button(root, text="Access Form", command=self.access_form, bg="#1F8D16", fg="white", font=("Helvetica", 16), highlightthickness=4)
        access_button.place(relx=0.5, rely=0.65, anchor="center", width=210, height=55)
        access_button.bind("<Enter>", self.on_access_enter)
        access_button.bind("<Leave>", self.on_access_leave)

        # Add Instructions button
        instructions_button = tk.Button(root, text="Instructions", command=self.show_instructions, bg="#4285F4", fg="white", font=("Helvetica", 16), highlightthickness=4)
        instructions_button.place(relx=0.5, rely=0.55, anchor="center", width=210, height=55)
        instructions_button.bind("<Enter>", self.on_instructions_enter)
        instructions_button.bind("<Leave>", self.on_instructions_leave)

        # Add Exit button
        exit_button = tk.Button(root, text="Exit", command=self.exit_program, bg="#D84839", fg="white", font=("Helvetica", 16), highlightthickness=4)
        exit_button.place(relx=0.5, rely=0.75, anchor="center", width=210, height=55)
        exit_button.bind("<Enter>", self.on_exit_enter)
        exit_button.bind("<Leave>", self.on_exit_leave)
    
    #WHEN USER CLICKED X BUTTON
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you really want to leave PHIL it out?"):
            self.root.destroy()

    #TO CENTER WELCOME PAGE WINDOW
    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - 1500) // 2
        y = (screen_height - 600) // 2

        self.root.geometry("1500x600+{}+{}".format(x, y))

    #FOR ACCESS FORM BUTTON
    def access_form(self):
        try:
            subprocess.Popen(["python", "D:\\2nd Sem\\Information Management\\PHILITOUT\\src\\Philitout.py"])
            print("Philitout.py opened successfully.")
            self.root.destroy()
        except Exception as e:
            print("Error opening Philitout.py:", e)

    #FOR SHOW INSTRUCTIONS BUTTON
    def show_instructions(self):
        instructions_window = tk.Toplevel(self.root)
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

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        instructions_window.geometry(f"+{x}+{y}")

    #FOR EXIT BUTTON
    def exit_program(self):
        if messagebox.askokcancel("Quit", "Do you really want to leave PHIL it out?"):
            self.root.destroy()

    #HOVER FUNCTIONS
    def on_access_enter(self, event):
        event.widget.config(bg="#34A853")
    def on_access_leave(self, event):
        event.widget.config(bg="#1F8D16")
    def on_instructions_enter(self, event):
        event.widget.config(bg="#4285F4")
    def on_instructions_leave(self, event):
        event.widget.config(bg="#3367D6")
    def on_exit_enter(self, event):
        event.widget.config(bg="#FF5C5C")
    def on_exit_leave(self, event):
        event.widget.config(bg="#D84839")

if __name__ == "__main__":
    root = tk.Tk()
    splash_screen = SplashScreen(root)
    root.mainloop()