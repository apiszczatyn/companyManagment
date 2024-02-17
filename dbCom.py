import tkinter as tk



def update():
    dialog = tk.Tk()
    dialog.geometry("200x100")
    dialog.focus_set()
    label = tk.Label(dialog, text="Baza danych zostala zaktualizowana!")
    label.pack(pady=10)
    but = tk.Button(dialog, text = "Ok", command=lambda:dialog.destroy())
    but.pack()


