from tkinter import *
from tkinter import messagebox

import re

# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


# Define a function for
# for validating an Email

def check(email):
    # pass the regular expression
    # and the string into the fullmatch() method
    if re.fullmatch(regex, email):
        return 0

    else:
        return 1


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System")
        self.root.geometry("920x600+100+50")
        self.root.resizable(False, False)
        # ====BG IMage====
        self.bg = PhotoImage(file="C:\\Users\\naamo\\Desktop\\DriverDrowsinessDetection\\imgDriver.png")
        self.bg_image = Label(self.root, image=self.bg).place(x=1, y=0, relheight=1)

        # =====Sign in Frame=====
        Frame_Sign = Frame(self.root, bg="white")
        Frame_Sign.place(x=30, y=100, height=340, width=500)

        title = Label(Frame_Sign, text="Enter details here", font=("Impact", 35, "bold"), fg="sky blue",
                      bg="white").place(x=60, y=10)
        desc = Label(Frame_Sign, text="Driver Drowsiness Detection System", font=("Goudy pld style", 13, "bold"),
                     fg="sky blue",
                     bg="white").place(x=90, y=70)
        lbl_name = Label(Frame_Sign, text="Name driver", font=("Goudy pld style", 15, "bold"),
                         fg="gray",
                         bg="white").place(x=60, y=115)
        self.txt_name = Entry(Frame_Sign, font=("times new roman", 15), bg="lightgray")
        self.txt_name.place(x=65, y=150, width=350, height=25)

        lbl_namecontact = Label(Frame_Sign, text="Name contact", font=("Goudy pld style", 15, "bold"),
                                fg="gray",
                                bg="white").place(x=60, y=180)
        self.txt_namecontact = Entry(Frame_Sign, font=("times new roman", 15), bg="lightgray")
        self.txt_namecontact.place(x=65, y=210, width=350, height=25)

        lbl_emailcontact = Label(Frame_Sign, text="Email contact", font=("Goudy pld style", 15, "bold"),
                                 fg="gray",
                                 bg="white").place(x=60, y=240)
        self.txt_emailcontact = Entry(Frame_Sign, font=("times new roman", 15), bg="lightgray")
        self.txt_emailcontact.place(x=65, y=270, width=350, height=25)

        start_button = Button(self.root,command=self.start_function, text="Start", bg="sky blue", font=("times new roman", 12)).place(x=220, y=425,
                                                                                                          width=100,height=30)



    def start_function(self):
        if self.txt_emailcontact.get() == "" or self.txt_name.get() == "" or self.txt_namecontact.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        elif check(self.txt_emailcontact.get())==1:

            messagebox.showerror("Error", "Invalid Email", parent=self.root)
        else:
            messagebox.showinfo("Enter details completed",
                                f"{self.txt_name.get()} drive carefully!\nYour contact:{self.txt_namecontact.get()}",
                                parent=self.root)



root = Tk()
obj = Login(root)
root.mainloop()
