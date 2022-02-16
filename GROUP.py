import sys
import os
from tkinter import *

window=Tk()

window.title("Running Python Script")
window.geometry('550x200')

def run():
    os.system('v2.py')

btn = Button(window, text="Nuts", bg="gray", fg="white",command=run)
btn.grid(column=0, row=0)


def run():
    os.system('crackdetection.py')

btn = Button(window, text="Defection", bg="black", fg="white",command=run)
btn.grid(column=8, row=0)


def run():
    os.system('tan.py')

btn = Button(window, text="Bolts", bg="black", fg="white",command=run)
btn.grid(column=0, row=8)


def run():
    os.system('v2.py')

btn = Button(window, text="Measurements", bg="black", fg="white",command=run)
btn.grid(column=8, row=8)


window.mainloop()
