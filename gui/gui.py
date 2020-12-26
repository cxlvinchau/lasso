import tkinter as tk


window = tk.Tk()

window.title("lasso - Probabilistic Model Checker")


window.rowconfigure(0, minsize=800, weight=1)

window.columnconfigure(2, minsize=800, weight=1)


txt_edit = tk.Text(window)

fr_buttons = tk.Frame(window)

btn_open = tk.Button(fr_buttons, text="Open")

btn_save = tk.Button(fr_buttons, text="Save As...")

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")



window.mainloop()