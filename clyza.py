import tkinter as tk
from tkinter import messagebox
import sqlite3

class ClassScheduleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Class Schedule")
        self.geometry("400x300")

        self.conn = sqlite3.connect("class_schedule.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        self.logged_in = False
        self.create_widgets()

        self.class_schedule = {}  # Dictionary to store the class schedule

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                username TEXT,
                                password TEXT
                            )""")
        self.conn.commit()

    def create_widgets(self):
        self.label = tk.Label(self, text="Class Schedule", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.show_login_widgets()

    def show_login_widgets(self):
        self.clear_frames()

        self.login_frame = tk.Frame(self)
        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.login_frame, width=30)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.login_frame, width=30, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.pack(pady=5)

        self.signup_button = tk.Button(self.login_frame, text="Sign-up", command=self.show_signup_widgets)
        self.signup_button.pack(pady=5)

        self.login_frame.pack()

    def show_signup_widgets(self):
        self.clear_frames()

        self.signup_frame = tk.Frame(self)
        self.new_username_label = tk.Label(self.signup_frame, text="New Username:")
        self.new_username_label.pack()
        self.new_username_entry = tk.Entry(self.signup_frame, width=30)
        self.new_username_entry.pack(pady=5)

        self.new_password_label = tk.Label(self.signup_frame, text="New Password:")
        self.new_password_label.pack()
        self.new_password_entry = tk.Entry(self.signup_frame, width=30, show="*")
        self.new_password_entry.pack(pady=5)

        self.signup_button = tk.Button(self.signup_frame, text="Sign Up", command=self.signup)
        self.signup_button.pack(pady=5)

        self.back_button = tk.Button(self.signup_frame, text="Back to Login", command=self.show_login_widgets)
        self.back_button.pack(pady=5)

        self.signup_frame.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = self.cursor.fetchone()
        if user:
            self.logged_in = True
            self.show_schedule_widgets()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def signup(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()

        if new_username and new_password:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, new_password))
            self.conn.commit()

            messagebox.showinfo("Success", "Sign up successful. Please login.")
            self.show_login_widgets()
        else:
            messagebox.showerror("Error", "Please enter a username and password.")

    def show_schedule_widgets(self):
        self.clear_frames()

        self.schedule_frame = tk.Frame(self)
        self.day_label = tk.Label(self.schedule_frame, text="Day:")
        self.day_label.pack()

        self.selected_day = tk.StringVar(self)
        self.selected_day.set("Monday")
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.day_option_menu = tk.OptionMenu(self.schedule_frame, self.selected_day, *days)
        self.day_option_menu.pack(pady=5)

        self.time_label = tk.Label(self.schedule_frame, text="Time:")
        self.time_label.pack()

        self.time_entry = tk.Entry(self.schedule_frame, width=30)
        self.time_entry.pack(pady=5)

        self.class_label = tk.Label(self.schedule_frame, text="Class:")
        self.class_label.pack()

        self.class_entry = tk.Entry(self.schedule_frame, width=30)
        self.class_entry.pack(pady=5)

        self.add_button = tk.Button(self.schedule_frame, text="Add Class", command=self.add_class)
        self.add_button.pack(pady=5)

        self.clear_button = tk.Button(self.schedule_frame, text="Clear Schedule", command=self.clear_schedule)
        self.clear_button.pack(pady=5)

        self.schedule_label = tk.Label(self.schedule_frame, text="")
        self.schedule_label.pack(pady=10)

        self.back_button = tk.Button(self.schedule_frame, text="Logout", command=self.show_login_widgets)
        self.back_button.pack(pady=5)

        self.schedule_frame.pack()

    def add_class(self):
        day = self.selected_day.get()
        time = self.time_entry.get()
        class_name = self.class_entry.get()

        if day not in self.class_schedule:
            self.class_schedule[day] = {}

        if time not in self.class_schedule[day]:
            self.class_schedule[day][time] = class_name
            schedule_info = f"Added class: {class_name} on {day} at {time}"
            self.schedule_label.config(text=schedule_info)
        else:
            messagebox.showerror("Error", "Class already scheduled at that time.")

    def clear_schedule(self):
        self.class_schedule = {}
        self.schedule_label.config(text="Schedule cleared.")

    def clear_frames(self):
        for widget in self.winfo_children():
            widget.destroy()

    def destroy(self):
        self.conn.close()
        super().destroy()

if __name__ == "__main__":
    app = ClassScheduleApp()
    app.mainloop()