
# import packages
from tkinter import *
from tkinter import messagebox
import re

# import scripts
import drowsiness_classification

# Make a regular expression, for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def check(email):
    """A function for validating an Email"""
    if re.fullmatch(regex, email):
        return 0  # in case the email is valid
    else:
        return 1  # in case the email is invalid


class Infopage:

    def __init__(self, root):

        self.root = root
        self.root.title("Info page")
        self.root.geometry("920x600+100+50")
        self.root.resizable(False, False)

        # ====BG IMage====
        self.bg = PhotoImage(file="../Data/Driver_Monitoring_Driver_Asleep.png")
        self.bg_image = Label(self.root, image=self.bg).place(x=1, y=0, relheight=1)

        # =====info page Frame=====
        info_page = Frame(self.root, bg="white")
        info_page.place(x=0, y=0, height=920, width=400)

        title = Label(info_page, text="Enter details here", font=("Arial", 25, "bold"), fg="sky blue", bg="white").place(x=60, y=20)
        desc = Label(info_page, text="Driver Drowsiness Detection System", font=("Goudy pld style", 13, "bold"), fg="sky blue", bg="white").place(x=55, y=70)

        # ======labels and txt box=====
        lbl_driver_name = Label(info_page, text="Name driver", font=("Goudy pld style", 15, "bold"), fg="gray", bg="white").place(x=30, y=115)
        self.txt_driver_name = Entry(info_page, font=("times new roman", 15), bg="lightgray")
        self.txt_driver_name.place(x=35, y=150, width=350, height=25)

        lbl_name_contact = Label(info_page, text="Name contact", font=("Goudy pld style", 15, "bold"), fg="gray", bg="white").place(x=30, y=180)
        self.txt_name_contact = Entry(info_page, font=("times new roman", 15), bg="lightgray")
        self.txt_name_contact.place(x=35, y=210, width=350, height=25)

        lbl_email_contact = Label(info_page, text="Email contact", font=("Goudy pld style", 15, "bold"), fg="gray", bg="white").place(x=30, y=240)
        self.txt_email_contact = Entry(info_page, font=("times new roman", 15), bg="lightgray")
        self.txt_email_contact.place(x=35, y=270, width=350, height=25)

        start_button = Button(self.root, command=self.start_function, text="Start Driving", bg="sky blue", font=("times new roman", 12)).place(x=150, y=500, width=100, height=30)

    def start_function(self):
        """A function that starts the system and checks the correctness of input, in case of missing or incorrect details messagebox will appear"""
        if self.txt_email_contact.get() == "" or self.txt_driver_name.get() == "" or self.txt_name_contact.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)

        elif check(self.txt_email_contact.get()) == 1:
            messagebox.showerror("Error", "Invalid Email", parent=self.root)

        else:
            messagebox.showinfo("Enter details completed",
                                f"{self.txt_driver_name.get()} drive carefully!\nYour contact:{self.txt_name_contact.get()}",
                                parent=self.root)
            username, contact_name, contact_email = self.txt_driver_name.get(), self.txt_name_contact.get(), self.txt_email_contact.get()
            self.root.destroy()
            drowsiness_classification.start_driving(username, contact_name, contact_email)


def main():
    root = Tk()
    obj = Infopage(root)
    root.mainloop()


if __name__ == '__main__':
    main()
