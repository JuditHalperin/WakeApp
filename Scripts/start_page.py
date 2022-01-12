# GUI first page
# Driver and emergency contact details before starting driving


# import packages
from tkinter import *
from tkinter import messagebox
import re
import tkinter as tk
from PIL import ImageTk, Image
# import tk


# import scripts
from PIL import ImageTk

import drowsiness_classification

# regular expression for validating an email
REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def is_valid_email(email):
    """This function checks if the email address is valid"""
    return re.fullmatch(REGEX, email)


class InfoPage:

    def __init__(self, root):
        """This function initializes the info-page"""

        # root
        self.root = root
        self.root.title("WakeApp")
        self.root.geometry("800x420+100+50")
        self.root.resizable(False, False)  # disable resizing

        # background image
        self.background = PhotoImage(file="../Data/background.png")
        Label(self.root, image=self.background).place(x=300, y=0)

        # info page frame
        info_page = Frame(self.root, bg="white")
        info_page.place(x=0, y=0, height=920, width=400)

        frame = Frame(info_page, width=100, height=200)
        frame.pack()
        frame.place(anchor='se', relx=0.75, rely=0.12)

        # Create an object of tkinter ImageTk
        img = ImageTk.PhotoImage(Image.open("../Data/slogo.png"))

        # Create a Label Widget to display the text or Image
        label = Label(frame, image=img, background="white")
        label.pack()
        label.grid(row=60, column=40)
        Label(info_page,
              text="Note that your contact will receive an email \n in case of a repeating drowsiness detection.",
              font=("Goudy pld style", 13), fg="#619BAF", bg="white").place(x=30, y=80)

        # driver name label and text box
        Label(info_page, text="Driver name", font=("Goudy pld style", 12, "bold"), fg="#B80008", bg="white").place(x=30,
                                                                                                                   y=140)
        self.txt_driver_name = Entry(info_page, font=("times new roman", 15), bg="lightgray")
        self.txt_driver_name.place(x=35, y=170, width=350, height=25)

        # contact name label and text box
        Label(info_page, text="Contact name", font=("Goudy pld style", 12, "bold"), fg="#B80008", bg="white").place(
            x=30, y=200)
        self.txt_name_contact = Entry(info_page, font=("times new roman", 15), bg="lightgray")
        self.txt_name_contact.place(x=35, y=230, width=350, height=25)

        # contact email label and text box
        Label(info_page, text="Contact email", font=("Goudy pld style", 12, "bold"), fg="#B80008", bg="white").place(
            x=30, y=260)
        self.txt_email_contact = Entry(info_page, font=("times new roman", 15), bg="lightgray")
        self.txt_email_contact.place(x=35, y=290, width=350, height=25)

        # start button
        Button(self.root, command=self.start_function, text="Start Driving", bg="#ABCAD5",
               font=("times new roman", 12)).place(x=150, y=346, width=100, height=30)

    def start_function(self):
        """This function checks the correctness of the input and starts the system, in case of missing or incorrect details messagebox will appear"""

        # if there is an empty field, show an error message
        if self.txt_email_contact.get() == "" or self.txt_driver_name.get() == "" or self.txt_name_contact.get() == "":
            messagebox.showerror("Error", "All fields are required.", parent=self.root)

        # if the email address is invalid, show an error message
        elif not is_valid_email(self.txt_email_contact.get()):
            messagebox.showerror("Error", "Invalid email address.", parent=self.root)

        # otherwise, show a success message, close the window and start driving
        else:
            messagebox.showinfo("Start Driving",
                                f"{self.txt_driver_name.get()}, have a pleasant journey! \nYour emergency contact is {self.txt_name_contact.get()}. \n\nPlease wait a few seconds...",
                                parent=self.root)
            username, contact_name, contact_email = self.txt_driver_name.get(), self.txt_name_contact.get(), self.txt_email_contact.get()  # these will be deleted when the root is destroyed
            self.root.destroy()
            drowsiness_classification.start_driving(username, contact_name, contact_email)


def main():
    root = Tk()
    InfoPage(root)
    root.mainloop()  # infinite loop waiting for an event to occur and process the event as long as the window is not closed


if __name__ == '__main__':
    main()
