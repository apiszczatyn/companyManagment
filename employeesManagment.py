import sqlite3
import tkinter as tk
from tkinter import ttk


dbConnection = sqlite3.connect("companyDatabase.db")
db = dbConnection.cursor()

newEmployee = []

positions = ['Pracownik Linii Produkcyjnej','Technik Utrzymania Ruchu','Specjalista ds. Logistyki',
             'Ksiegowy','Brygadzista Linii Produkcyjnej','Technolog','Magazynier','Menadzer ds. Sprzedazy',
             'Specjalista ds. BHP','Kierownik Produkcji','Kierowca']

def writeEmployeeToDb(root):
    db.execute("INSERT INTO employees (firstName, lastName, phoneNumber, age, position, hWage) VALUES (?,?,'unknown',?,?,?)",(newEmployee[0][0].get(),newEmployee[0][1].get(),newEmployee[0][2].get(),newEmployee[0][3].get(),newEmployee[0][4].get()))
    dbConnection.commit()
    root.destroy()

def addEmployee(root):
    newEmployee.clear()
    addEmployeeWindow = tk.Toplevel(root)
    addEmployeeWindow.geometry("300x350+200+250")
    addEmployeeWindow.focus_set()
    addEmployeeWindow.grab_set()
    
    tk.Label(addEmployeeWindow, text="Dodawanie nowego pracownika").grid(columnspan=2,row=0,column=0,padx=10,pady=10, sticky="nsew")

    tk.Label(addEmployeeWindow, text = "Imie").grid(row = 1, column = 0, padx=10,pady=10, sticky="nsew")
    tk.Label(addEmployeeWindow, text = "Nazwisko").grid(row = 2, column = 0, padx=10,pady=10, sticky="nsew")
    tk.Label(addEmployeeWindow, text = "Wiek").grid(row = 3, column = 0, padx=10,pady=10, sticky="nsew")
    tk.Label(addEmployeeWindow, text = "Stanowisko").grid(row = 4, column = 0, padx=10,pady=10, sticky="nsew")
    tk.Label(addEmployeeWindow, text = "Stawka").grid(row = 5, column = 0, padx=10,pady=10, sticky="nsew")
    
    firstName = tk.Entry(addEmployeeWindow, width=20)
    firstName.grid(row=1, column=1,padx=10,pady=10,sticky="nsew")
    lastName = tk.Entry(addEmployeeWindow)
    lastName.grid(row=2, column=1,padx=10,pady=10,sticky="nsew")
    age = tk.Entry(addEmployeeWindow, width=3)
    age.grid(row=3, column=1,padx=10,pady=10,sticky="nsew")
    position = ttk.Combobox(addEmployeeWindow, values=positions, state='readonly')
    position.grid(row=4, column=1,padx=10,pady=10,sticky="nsew")
    hWage = tk.Entry(addEmployeeWindow)
    hWage.grid(row=5, column=1,padx=10,pady=10,sticky="nsew")
    
    tk.Button(addEmployeeWindow, text="Zatwierdz i przeslij", command=lambda:writeEmployeeToDb(addEmployeeWindow)).grid(row=6,column=0,columnspan=2,sticky="nsew",padx=10,pady=10)

    newEmployee.append([firstName, lastName, age, position, hWage])
    addEmployeeWindow.mainloop()
    

            
def showEmployees(root):
     def on_mousewheel(event):
        try:
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except tk.TclError:
            pass  # Ignorowanie b³êdu, jeœli canvas nie istnieje
      
     def on_close(parent):
        showEmployeesWindow.unbind_all("<MouseWheel>")  # Usuniêcie globalnego powi¹zania przewijania
        showEmployeesWindow.destroy()  # Zamkniêcie okna
        
     showEmployeesWindow = tk.Toplevel(root)
     showEmployeesWindow.geometry("550x650+100+50")
     showEmployeesWindow.focus_set()

     showEmployeesWindow.protocol("WM_DELETE_WINDOW",lambda: on_close(root))  # Ustawienie procedury obs³ugi zamkniêcia
     canvas = tk.Canvas(showEmployeesWindow)
     canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
###############
     menu_bar = tk.Menu(showEmployeesWindow)
     menu1 = tk.Menu(menu_bar,tearoff=0)
     menu1.add_command(label="Dodaj pracownika", command=lambda:addEmployee(showEmployeesWindow))
     
     menu_bar.add_cascade(label="Akcje", menu=menu1)
     showEmployeesWindow.config(menu=menu_bar)
     


###############
     scrollbar = ttk.Scrollbar(showEmployeesWindow, orient='vertical', command=canvas.yview)
     scrollbar.pack(side=tk.RIGHT, fill='y')  
     canvas.configure(yscrollcommand=scrollbar.set)
     frame = ttk.Frame(canvas)
     canvas.create_window((0, 0), window=frame, anchor='nw')
###############
     db.execute("SELECT ID,firstName, lastName, position, age, hWage FROM employees")
     queryRes = db.fetchall()
###############     
     header = tk.Label(frame, text="Pracownicy", font=("Segoe UI", 20)).grid(row=0, column=0,columnspan=5, sticky="nsew")
     header1= tk.Label(frame,text ="Lp").grid(row=1, column=0, sticky="nsew", padx=0, pady=5)
     header2= tk.Label(frame,text ="Imie, Nazwisko").grid(row=1, column=1, sticky="nsew", padx=0, pady=5)
     header4= tk.Label(frame,text ="Stanowisko").grid(row=1, column=2, sticky="nsew", padx=0, pady=5)
     header5= tk.Label(frame,text ="Wiek").grid(row=1, column=3, sticky="nsew", padx=0, pady=5)
     header6= tk.Label(frame,text ="Stawka/h").grid(row=1, column=4, sticky="nsew", padx=0, pady=5)
     
     for i, (id, firstName, lastName,position, age, hWage) in enumerate(queryRes, start=1):
         tk.Label(frame, text=i, borderwidth=4, relief="groove").grid(row=i+1, column=0, sticky="nsew", padx=0, pady=5)
         tk.Label(frame, text=firstName+" "+lastName, borderwidth=4, relief="groove").grid(row=i+1, column=1, sticky="nsew", padx=0, pady=5)
         tk.Label(frame, text=position,borderwidth=4, relief="groove").grid(row=i+1, column=2, sticky="nsew", padx=0, pady=5)
         tk.Label(frame, text=age,borderwidth=4, relief="groove").grid(row=i+1, column=3, sticky="nsew", padx=0, pady=5)
         tk.Label(frame, text=round(hWage,2),borderwidth=4, relief="groove").grid(row=i+1, column=4, sticky="nsew", padx=0, pady=5)

     showEmployeesWindow.bind_all("<MouseWheel>", on_mousewheel)
     frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
     showEmployeesWindow.mainloop()
     

