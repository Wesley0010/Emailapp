EMAIL SENDER APPLICATION

This is a python-based application that allows the sending of emails throw gmail using smtp.this also include graphical user interfase that is built using tkinter and the are kept as data that can be view, this is done using sqlite database so as to act as history.

Table of content

I.	stetup instructions 

A.	need for the application

B.	installation

II.	code (code structure and comments )

III.	user manual

A.	running the application

B.	sending emails

C.	view sent mails

D.	closing the application

IV.	conclusion



1 setup instructions 

   	A. need for the application

	this is a python program therefore for it to run it needs libraries and a compiler so that is runs without problems and errors and have fruitful results. The libraries needed are  smtplib, email, tkinter, sqlite3, date-time hence No external packages needed only uses Python standard libraries

apart from libraries some of the things needed will be , Python 3.x installed, Internet connection, Gmail or Yahoo account with App Passwords which you can get from your Gmail account setting for authentication and to make the connection secure



B.installation

Steps to Install:

1.	Save the code in a Python file, e.g. internet_messaging.py

2.	Run the file using Python:

a. bash

   Copy code

   python internet_messaging.py



b. open the file in vs code or pycham 

   run the code 

                  No additional installation is required.

2. code(code structure and comments )

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



#setting time and date 

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

gmail_address.set("")

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





#GUI SETUP

root = tk.Tk()

root.geometry("600x500")

root.title("Internet messager")



gmail_address = tk.StringVar()

password = tk.StringVar()

recipient = tk.StringVar()

subject = tk.StringVar()



# MENU bar 

menubar = tk.Menu(root)

menubar = tk.Menu(root, bg='lightgray', fg='gray')



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



# enter fields for data and their labels

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



#check box to change colour 

checkbox = tk.Checkbutton(root, text="Dark Mode", variable=var, command=change_background)

checkbox.grid(row=12, column=0)



#looping takes place

root.mainloop()







	here is an explanation of each parts of the codes above:

	 Libraries Used

•	`smtplib`: Handles SMTP protocol for sending emails.

•	`email.message`: Facilitates email message creation.

•	`tkinter`: Creates the GUI interface.

•	`datetime`: Timestamping sent emails and updating current date/time.

•	`sqlite3`: Stores email logs locally.

1.	Database Creation:

   The application initializes a SQLite database named `internetmessages(email).db` with a table `sent_emails` to store email logs:

•	id: Unique identifier

•	sender: Sender's email address

•	recipient: Recipient's email address

•	subject: Email subject

•	message: Email body

•	date: Timestamp when email was sent

•	

Main Window:  

   The main Tkinter window is configured with a fixed size, title, and menu options.

Input Fields

Your email (Gmail or Yahoo): Sender's email address.

Password: App password for the email account (for Gmail, generate an app password).

Recipient email: Recipient's email address.

Subject: Email subject.

Compose Email: Multi-line text box for email body.

Buttons & Menu Options:

Insert Button: Automatically fills the password field with a predefined password (`"abcd efgh ijkl mnop"`).

Send Email: Sends the email via SMTP, logs the email in the database, and provides success/error feedback.

Clear Fields: Clears all input fields.

View Sent Emails: Opens a new window displaying sent email history.

About: Shows information about the application.

Dark Mode Checkbox:Toggle background color between white and light gray.

Main Functions:

update_datetime()

Continuously updates and displays the current date and time every second.

access_pass()

Fills the password field with a predefined password.

send_email()

Creates an email message with user input.

Connects to SMTP server (`smtp.gmail.com`, port 587).

Sends the email.

Logs the email details into the database.

Provides success or error message.



clear_fields()

Resets all input fields to blank.

show_about()
Displays an informational message about the application.

view_sent_emails()

Opens a new window.

Fetches sent email logs from the database.

Displays logs in a table with scroll-bars.

change_background()

Changes GUI background color based on the checkbox state.

GUI Layout

Menu Bar: Options for File (Send Email, Exit), Tools (Clear Fields, View Sent Emails), Help (About).

Input Fields: For email addresses, password, subject, and message body.

Buttons: Send Email, Insert (password).

Date & Time Label: Shows real-time current date and time.

Dark Mode Checkbox: Switch background color.

Security Considerations

Use app-specific passwords for Gmail accounts.

Always handle credentials securely.

4. User manual

A.	running the application

run the application After launching and a window will show with the title “internet messaging” at the top and inside the window you'll find fields manuals and and buttons, all with specific functions. Make sure the files name matches with the name in your Gmail account so that it authenticates your app-password

B.	sending emails

Enter your email address (must be Gmail or Yahoo)

Insert your app-specific password by clicking the Insert button or typing it manually

Enter recipient’s email, subject, and message content

Click Send Email

If successful, a message box will confirm the email was sent and the log will be stored in the local database (internetmessages(email).db).

C.	view sent mails

To view sent emails:

Navigate to Tools → View Sent Emails

D.	closing the application

to close application:

navigate on the menu bar to home   ->  exit

E.	To clear input fields:

•	Navigate to Tools → Clear Fields

I. To learn more about the app:

•	Navigate to Help → About
