from tkinter import *


def btn_clicked():
    print("Button Clicked")


window = Tk()

window.geometry("500x500")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 500,
    width = 500,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    105.0, -1136.5,
    image = entry0_img)

entry0 = Entry(
    bd = 0,
    bg = "#dedede",
    highlightthickness = 0)

entry0.place(
    x = 92.5, y = -261,
    width = 225.0,
    height = 47)

entry1_img = PhotoImage(file = f"img_textBox1.png")

'''
filename = PhotoImage(file = "sunshine.gif")
image = canvas.create_image(50, 50, anchor=NE, image=filename)
'''
entry1_bg = canvas.create_image(
    205.0, -151.5,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#dedede",
    highlightthickness = 0)

entry1.place(
    x = 92.5, y = -176,
    width = 225.0,
    height = 47)

entry2_img = PhotoImage(file = f"img_textBox2.png")
entry2_bg = canvas.create_image(
    206.0, -67.5,
    image = entry2_img)

entry2 = Entry(
    bd = 0,
    bg = "#dedede",
    highlightthickness = 0)

entry2.place(
    x = 93.5, y = -92,
    width = 225.0,
    height = 47)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    -75.5, -121.0,
    image=background_img)

window.resizable(False, False)
window.mainloop()
