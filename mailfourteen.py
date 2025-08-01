#libraries being used
import smtplib
from email.message import EmailMessage
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import sqlite3
from tkinter import ttk
from tkinter import filedialog 

#data base sqlite to store data
conn = sqlite3.connect("internetmessages(email).db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sent_emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        recipient TEXT,
        subject TEXT,
        message TEXT,
        date TEXT
    )
''')
conn.commit()

def update_datetime():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    datetime_label.config(text=f"Date & Time: {now}")
    root.after(1000, update_datetime)

#setting the password
def access_pass():
    password.set("yrok sois infx goow")

#the smtp protocal to send emails
def send_email():
    sender = gmail_address.get()
    pwd = password.get()
    to = recipient.get()
    sbjt = subject.get()
    body = message_text.get("1.0", tk.END).strip()

    msg = EmailMessage()
    msg['Subject'] = sbjt
    msg['From'] = sender
    msg['To'] = to
    msg.set_content(body)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(sender, pwd)
            smtp.send_message(msg)

        # Saving to the database
        date_sent = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO sent_emails (sender, recipient, subject, message, date) VALUES (?, ?, ?, ?, ?)",
                       (sender, to, sbjt, body, date_sent))
        conn.commit()

        messagebox.showinfo("Success", "✅ Email sent and logged in database!")
    except Exception as e:
        messagebox.showerror("Error", f"❌ Failed to send email:\n{e}")

#clearing the feilds after use
def clear_fields():
    #gmail_address.set("")
    password.set("")
    recipient.set("")
    subject.set("")
    message_text.delete("1.0", tk.END)

#gives the about infomation of our program
def show_about():
    messagebox.showinfo("About", "Email Sender App\nCreated with Python and Tkinter.")

#here we wre able to view the history to the emails sent
def view_sent_emails():
    view_window = tk.Toplevel(root)
    view_window.title("Sent Email History")
    view_window.geometry("800x400")

    # Treeview widget
    columns = ("Sender", "Recipient", "Subject", "Date")
    tree = ttk.Treeview(view_window, columns=columns, show="headings")
    tree.heading("Sender", text="Sender")
    tree.heading("Recipient", text="Recipient")
    tree.heading("Subject", text="Subject")
    tree.heading("Date", text="Date")

    # Resize columns
    tree.column("Sender", width=150)
    tree.column("Recipient", width=150)
    tree.column("Subject", width=250)
    tree.column("Date", width=150)

    # Fetch data from DB
    cursor.execute("SELECT sender, recipient, subject, date FROM sent_emails ORDER BY id DESC")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

    tree.pack(fill=tk.BOTH, expand=True)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(view_window, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

#change background color with checkbox
def change_background():
    if var.get():
        root.config(background='lightgray')
    else:
        root.config(background='white')



# GUI SETUP 
root = tk.Tk()
root.geometry("600x500")
root.title("Internet messager")

gmail_address = tk.StringVar()
password = tk.StringVar()
recipient = tk.StringVar()
subject = tk.StringVar()

# MENU 
menubar = tk.Menu(root)
menubar = tk.Menu(root, bg='darkgray', fg='gray')


file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Send Email", command=send_email)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)

tools_menu = tk.Menu(menubar, tearoff=0)
tools_menu.add_command(label="Clear Fields", command=clear_fields)
tools_menu.add_command(label="View Sent Emails", command=view_sent_emails)
menubar.add_cascade(label="Tools", menu=tools_menu)

help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menubar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menubar)

# UI ELEMENTS
tk.Label(root, text="Your email (Gmail or Yahoo)").grid(row=0, column=0, sticky='w', padx=10)
tk.Entry(root, textvariable=gmail_address, width=40).grid(row=1, column=0, columnspan=2, padx=10, sticky="nsew")

tk.Label(root, text="Password (app password)").grid(row=2, column=0, sticky='w', padx=10)
tk.Entry(root, textvariable=password, show='*', width=40).grid(row=3, column=0, columnspan=2, padx=10, sticky="nsew")
button = tk.Button(root, text="insert", command=access_pass)
button.grid(row=3, column=1)

tk.Label(root, text="Recipient email").grid(row=4, column=0, sticky='w', padx=10)
tk.Entry(root, textvariable=recipient, width=40).grid(row=5, column=0, columnspan=2, padx=10, sticky="nsew")

tk.Label(root, text="Subject").grid(row=6, column=0, sticky='w', padx=10)
tk.Entry(root, textvariable=subject, width=40).grid(row=6, column=1, padx=10, sticky="nsew")

tk.Label(root, text="Compose Email").grid(row=7, column=0, sticky='nw', padx=10)
message_text = tk.Text(root, width=60, height=10)
message_text.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

tk.Button(root, text="Send Email", command=send_email).grid(row=9, column=0, columnspan=2, pady=10, sticky="nsew")

datetime_label = tk.Label(root, font=("Arial", 10), fg="gray")
datetime_label.grid(row=10, column=0, columnspan=2, pady=(10, 0))
update_datetime()

var = tk.IntVar()

checkbox = tk.Checkbutton(root, text="Dark Mode", variable=var, command=change_background())
checkbox.grid(row=12, column=0)

root.mainloop()
