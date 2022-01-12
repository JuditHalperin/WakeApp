from tkinter import *
from PIL import ImageTk, Image

# root
root = Tk()
root.title("WakeApp")
root.geometry("800x420+100+50")
root.resizable(False, False)  # disable resizing

# background image
background = PhotoImage(file="../Data/background.png")
Label(root, image=background).place(x=300, y=0)

# info page frame
info_page = Frame(root, bg="white")
info_page.place(x=0, y=0, height=920, width=400)

frame = Frame(info_page, width=100, height=200)
frame.pack()
frame.place(anchor='se', relx=0.75, rely=0.12)

# Create an object of tkinter ImageTk
img = ImageTk.PhotoImage(Image.open("../Data/slogo.png"))

# Create a Label Widget to display the text or Image
label = Label(frame, image=img,background="white")
label.pack()
label.grid(row=60,column=40)

Label(info_page,
      text="Note that your contact will receive an email \n in case of a repeating drowsiness detection.",
      font=("Goudy pld style", 13), fg="#619BAF", bg="white").place(x=30, y=80)
# driver name label and text box
Label(info_page, text="Driver name", font=("Goudy pld style", 12, "bold"), fg="#B80008", bg="white").place(x=30,
                                                                                                           y=140)
txt_driver_name = Entry(info_page, font=("times new roman", 15), bg="lightgray")
txt_driver_name.place(x=35, y=170, width=350, height=25)

# contact name label and text box
Label(info_page, text="Contact name", font=("Goudy pld style", 12, "bold"), fg="#B80008", bg="white").place(
    x=30, y=200)
txt_name_contact = Entry(info_page, font=("times new roman", 15), bg="lightgray")
txt_name_contact.place(x=35, y=230, width=350, height=25)

# contact email label and text box
Label(info_page, text="Contact email", font=("Goudy pld style", 12, "bold"), fg="#B80008", bg="white").place(
    x=30, y=260)
txt_email_contact = Entry(info_page, font=("times new roman", 15), bg="lightgray")
txt_email_contact.place(x=35, y=290, width=350, height=25)

# start button
Button(root, text="Start Driving", bg="#ABCAD5",
       font=("times new roman", 12)).place(x=150, y=346, width=100, height=30)
root.mainloop()  # infinite loop waiting for an event to occur and process the event as long as the window is not closed

