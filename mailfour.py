import smtplib
from email.message import EmailMessage
import tkinter as tk
from tkinter import messagebox
from datetime import datetime


def update_datetime():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    datetime_label.config(text=f"Date & Time: {now}")
    root.after(1000, update_datetime) 


def send_email():
    sender = gmail_address.get()
    pwd = password.get()
    to = recipient.get()
    sbjt = subject.get()

    msg = EmailMessage()
    msg['Subject'] = sbjt
    msg['From'] = sender
    msg['To'] = to
    msg.set_content(message.get())

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(sender, pwd)
            smtp.send_message(msg)
        messagebox.showinfo("Success", "✅ Email sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"❌ Failed to send email:\n{e}")

# Setup GUI
root = tk.Tk()
root.geometry("500x300")
root.title("Internet messager")

# Variables
gmail_address = tk.StringVar()
password = tk.StringVar()
recipient = tk.StringVar()
subject= tk.StringVar()
message= tk.StringVar()


# UI Elements
tk.Label(root, text="Your email (Gmail or Yahoo)").grid(row=0, column=0)
tk.Entry(root, textvariable=gmail_address).grid(row=1, column=0)

tk.Label(root, text="Password (app password)").grid(row=2, column=0)
tk.Entry(root, textvariable=password, show='*').grid(row=3, column=0)

tk.Label(root, text="Recipient email").grid(row=4, column=0)
tk.Entry(root, textvariable=recipient).grid(row=5, column=0)

tk.Label(root, text="subject").grid(row=6, column=0)
tk.Entry(root, textvariable = subject).grid(row=6, column=1)

tk.Label(root, text="Compose Email").grid(row=7, column=0, sticky='nw')
message_text = tk.Text(root, width=50, height=10)
message_text.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

datetime_label = tk.Label(root, font=("Arial", 10), fg="gray")
datetime_label.grid(row=12, column=0, columnspan=2, pady=(10, 0))
update_datetime()



tk.Button(root, text="Send Email", command=send_email).grid(row=10, column=0, pady=10)

root.mainloop()
