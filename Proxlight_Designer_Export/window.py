from tkinter import *


def btn_clicked():
    print("Button Clicked")


window = Tk()

window.geometry("500x500")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 200,
    width = 200,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 20, y = 100, anchor= CENTER)

entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    50, 50, anchor=CENTER,
    image = entry0_img)

entry0 = Entry(
    bd = 0,
    bg = "#dedede",
    highlightthickness = 0)

entry0.place(
    x = -89.5, y = -516,
    width = 225.0,
    height = 47)

entry1_img = PhotoImage(file = f"img_textBox1.png")
entry1_bg = canvas.create_image(
    24.0, -413.5,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#dedede",
    highlightthickness = 0)

entry1.place(
    x = -88.5, y = -438,
    width = 225.0,
    height = 47)

entry2_img = PhotoImage(file = f"img_textBox2.png")
entry2_bg = canvas.create_image(
    38.0, -338.5,
    image = entry2_img)

entry2 = Entry(
    bd = 0,
    bg = "#dedede",
    highlightthickness = 0)

entry2.place(
    x = -74.5, y = -363,
    width = 225.0,
    height = 47)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(50,10,image=background_img, anchor= NE)

window.resizable(False, False)
window.mainloop()
