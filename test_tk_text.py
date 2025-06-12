import tkinter as tk
from tkinter import scrolledtext

root = tk.Tk()
root.title("Test Tkinter Text Area")

text = scrolledtext.ScrolledText(root, width=80, height=20)
text.pack(padx=10, pady=10)

root.mainloop()