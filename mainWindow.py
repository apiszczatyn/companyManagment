import tkinter as tk
import ordersManagment as orders
import employeesManagment as employees
from tkinter import *


global root

def createMainWindow():
    global root
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.title("Company Managment - alpha")
    root.geometry(f"{int(screen_width/2)}x{int(screen_height/2)}+400+200")
    
   
    img = tk.PhotoImage(file='images/logo100x100.png')

    label1 = tk.Label(root, image = img)
    label1.grid(row = 0, column = 0, rowspan = 2, columnspan=2,padx=10,pady=10)
    label2 = tk.Label(root, text ="Modern Company Managment" ,font=('Segoe UI', 20, 'bold'))
    label2.grid(row = 0, column = 2, rowspan = 2, columnspan=3, padx=10,pady=10)


    button1 = tk.Button(root, text="Dodaj zlecenie", command=lambda:orders.addOrder(root)).grid(row = 4, column = 1, padx=20,pady=10)
    button2 = tk.Button(root,text="Przegladaj zlecenia", command=lambda:orders.showOrders(root)).grid(row = 4, column = 2, padx=20,pady=10)
    button3 = tk.Button(root, text="Pracownicy",command = lambda: employees.showEmployees(root)).grid(row=4,column=3,padx=20,pady=10)
    root.mainloop()