
import sqlite3
from sys import maxsize
import time
import tkinter as tk
from tkinter import ttk
import dbCom as com

dbConnection = sqlite3.connect("companyDatabase.db")
db = dbConnection.cursor()


dimensions = []
editedDimensions = []

global orderWindow
global dimensionsEntry
dimensionsEntry = None
orderWindow = None       

def dynamicEntry(fieldsToCreate,root):
    global dimensionsEntry
    dimensionsEntry = tk.Toplevel(root)
    dimensionsEntry.title("Company Managment - wymiary elementow")
    dimensionsEntry.geometry("500x400")
    dimensionsEntry.focus_set()
    
    label1 = tk.Label(dimensionsEntry, text="Dlugosc przejscia").grid(row=0,column=1, padx=10,pady=10)
    label2 = tk.Label(dimensionsEntry, text="Szerokosc").grid(row=0,column=2, padx=10,pady=10)
    label3 = tk.Label(dimensionsEntry, text="Ilosc").grid(row=0,column=3, padx=10,pady=10)
    
    for i in range (fieldsToCreate):
         label = tk.Label(dimensionsEntry, text=str(i+1)+".").grid(row = i+1,column=0,padx = 5,pady=10)
         entry1 = tk.Entry(dimensionsEntry)
         entry1.grid(row=i+1,column=1, padx=10,pady=10)
         
         
         
         entry2 = tk.Entry(dimensionsEntry)
         entry2.grid(row=i+1,column=2, padx=10,pady=10)
         
         entry3 = tk.Entry(dimensionsEntry)
         entry3.grid(row=i+1, column=3, padx=10,pady=10)
         
         dimensions.append([entry1,entry2,entry3])  
         
    tk.Button(dimensionsEntry, text = "Zatwierdz i przeslij",command=lambda:writeDimensToDb(fieldsToCreate)).grid(row = fieldsToCreate+2,column=1,padx=10,pady=10)

    dimensionsEntry.mainloop()

    
    
 


def addOrder(root):
    global orderWindow
    orderWindow = tk.Toplevel(root)
    orderWindow.title("Company Managment - wprowadz zlecenie")
    orderWindow.geometry("550x180")
    orderWindow.focus_set()

    tk.Label(orderWindow, text="Podaj nazwe klienta").grid(row = 0,column = 0, padx=10,pady=10, sticky="nsew")
    clientNameEntry = tk.Entry(orderWindow)
    clientNameEntry.grid(row = 1,column = 0, padx=10,pady=10, sticky="nsew")
    tk.Label(orderWindow, text="Podaj ilosc roznych przedmiotow w zamowieniu").grid(row = 0,column = 2, padx=10,pady=10, sticky="nsew")
    quantityEntry = tk.Entry(orderWindow)
    quantityEntry.grid(row = 1,column = 2, padx=10,pady=10, sticky="nsew")
    
    buttonNameAndQuantity = tk.Button(orderWindow, text="Zapisz informacje", command=lambda:writeCredToDb(clientNameEntry,quantityEntry,orderWindow)).grid(row = 2,column = 1, padx=10,pady=10)
    orderWindow.mainloop()




def writeCredToDb(nameEntry, quantityEntry,root): 
     clientName = nameEntry.get()
     quantity = quantityEntry.get()
     
     named_tuple = time.localtime() # get struct_time
     time_string = time.strftime("%H:%M:%S", named_tuple)
     date_string = time.strftime("%d:%m:%Y", named_tuple)
    
     db.execute("INSERT INTO ordersInProduction (clientName,amountOfElements,dateOfAcceptance, timeOfAcceptance) VALUES (?,?,?,?)",(clientName, quantity, date_string, time_string))
     dbConnection.commit() 
     
     dynamicEntry(int(quantity),root)
     
     
def writeDimensToDb(quantity):
    db.execute("SELECT ID FROM ordersInProduction ORDER BY ID DESC LIMIT 1")
    dbConnection.commit() 
    orderId = db.fetchone()
    orderId = orderId[0]
    
    for i in range (0, int(quantity)):
        db.execute("INSERT INTO ordersElements (orderID,length,width,amount) VALUES (?,?,?,?)",(orderId, dimensions[i][0].get(), dimensions[i][1].get(),dimensions[i][2].get()))
        dbConnection.commit()  
    dimensions.clear()
    
    
    global dimensionsEntry, orderWindow
    
    if dimensionsEntry is not None:
        dimensionsEntry.destroy()
        dimensionsEntry = None  # Ustawienie na None, aby unikn¹æ próby ponownego zamkniêcia

    if orderWindow is not None:
        orderWindow.destroy()
        orderWindow = None
    com.update()
    


    
def showOrders(root):
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")    
        showOrdersWindow = tk.Toplevel(root)
        screen_width = showOrdersWindow.winfo_screenwidth()
        screen_height = showOrdersWindow.winfo_screenheight()
        showOrdersWindow.title("Company Managment - Zlecenia w produkcji")
        showOrdersWindow.geometry(f"900x550+{int((screen_width-900)/2)}+{int((screen_height-550)/2)}")
        showOrdersWindow.focus_set()

        canvas = tk.Canvas(showOrdersWindow)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        scrollbar = ttk.Scrollbar(showOrdersWindow, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        


        frame = ttk.Frame(canvas)

        canvas.create_window((0, 0), window=frame, anchor='nw')

        for col in range(4):  # Dla czterech kolumn
            frame.grid_columnconfigure(col, weight=1, uniform="group1")

        db.execute("SELECT ID, clientName, amountOfElements, dateOfAcceptance FROM ordersInProduction")
        rekordy = db.fetchall()
    

        text1 = tk.Label(frame, text="Zlecenia w produkcji", font=("Segoe UI", 20)).grid(row=0, column=0,columnspan=5, sticky="nsew")
        header1 = tk.Label(frame, text="Nr.").grid(row=1, column=0, sticky="nsew", padx=0, pady=5)
        header2 = tk.Label(frame, text="Nazwa klienta").grid(row=1, column=1, sticky="nsew", padx=0, pady=5)
        header3 = tk.Label(frame, text ="Ilosc roznych elementow").grid(row=1, column=2, sticky="nsew", padx=0, pady=5)
        header4 = tk.Label(frame, text="Data zlozenia zamowienia").grid(row=1, column=3, sticky="nsew", padx=0, pady=5)
        
        for i, (id, client_name, amount, date) in enumerate(rekordy, start=1):
            tk.Label(frame, text=id, borderwidth=4, relief="groove").grid(row=i+1, column=0, sticky="nsew", padx=0, pady=5)
            tk.Label(frame, text=client_name, borderwidth=4, relief="groove").grid(row=i+1, column=1, sticky="nsew", padx=0, pady=5)
            tk.Label(frame, text=amount, borderwidth=4, relief="groove").grid(row=i+1, column=2, sticky="nsew", padx=0, pady=5)
            tk.Label(frame, text=date, borderwidth=4, relief="groove").grid(row=i+1, column=3, sticky="nsew", padx=0, pady=5)
            
            detailsButton = tk.Button(frame, text="Szczegoly", command=lambda order_Id = id: showDetails(showOrdersWindow,order_Id))
            detailsButton.grid(row=i+1,column=4, padx=0, pady=5)
                                      
            deleteButton = tk.Button(frame, text="Usun",command=lambda order_Id = id: deleteOrder(showOrdersWindow,order_Id))
            deleteButton.grid(row=i+1,column=5, padx=0, pady=5)

        showOrdersWindow.bind("<MouseWheel>", on_mousewheel)
        frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        showOrdersWindow.mainloop()

def writeAddedToDb(root, id, length, width, amount):
    length = length.get()
    width = width.get()
    amount = amount.get()
    db.execute("INSERT INTO ordersElements (orderId, length, width, amount) VALUES(?,?,?,?)",(id, length,width,amount))
    dbConnection.commit()
    root.destroy()

def addElement(root, id):
    addElementWindow = tk.Toplevel(root)
    addElementWindow.geometry("450x150+350+180")
    
    label1 = tk.Label(addElementWindow, text="Dlugosc przejscia (w mm)").grid(row=0,column=0, padx=10,pady=10, sticky="nsew")
    label2 = tk.Label(addElementWindow, text="Szerokosc (w mm)").grid(row=0,column=1, padx=10,pady=10, sticky="nsew")
    label3 = tk.Label(addElementWindow, text="Ilosc").grid(row=0,column=2, padx=10,pady=10, sticky="nsew")
    
    entry1 = tk.Entry(addElementWindow)
    entry1.grid(row = 1, column = 0, padx=10,pady=10, sticky="nsew")

    entry2 = tk.Entry(addElementWindow)
    entry2.grid(row = 1, column = 1, padx=10,pady=10, sticky="nsew")
    
    entry3 = tk.Entry(addElementWindow)
    entry3.grid(row = 1, column = 2, padx=10,pady=10, sticky="nsew")
    
    but1 = tk.Button(addElementWindow, text="Dodaj",command=lambda:writeAddedToDb(addElementWindow, id,entry1, entry2, entry3))
    but1.grid(row=2, column=0, columnspan=3,padx=10,pady=20,sticky="nsew")
    
    addElementWindow.mainloop()
    

def showDetails(root,id):
    def on_mousewheel(event):
        try:
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except tk.TclError:
            pass  # Ignorowanie b³êdu, jeœli canvas nie istnieje
      
    def on_close(parent):
        detailsWindow.unbind_all("<MouseWheel>")  # Usuniêcie globalnego powi¹zania przewijania
        detailsWindow.destroy()  # Zamkniêcie okna
        
    detailsWindow = tk.Toplevel(root)
    detailsWindow.geometry("650x500+400+150")
    detailsWindow.focus_set()
    detailsWindow.grab_set()
    detailsWindow.protocol("WM_DELETE_WINDOW",lambda: on_close(root))  # Ustawienie procedury obs³ugi zamkniêcia

    canvas = tk.Canvas(detailsWindow)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(detailsWindow, orient='vertical', command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill='y')
     
    canvas.configure(yscrollcommand=scrollbar.set)
     
    frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor='nw')



    db.execute("SELECT ID, clientName, dateOfAcceptance, timeOfAcceptance FROM ordersInProduction WHERE ID = ?",(id,))
    header = db.fetchone()
    
    tk.Label(frame, text="Zamowienie nr. "+str((header[0]))).grid(row=0,column=0,columnspan=4,sticky="nsew")
    tk.Label(frame, text="Klient").grid(row=1,column=0,sticky="nsew")
    tk.Label(frame, text="Data zlozenia zamowienia").grid(row=1,column=1,sticky="nsew")
    tk.Label(frame, text="Godzina zlozenia zamowienia").grid(row=1,column=2,sticky="nsew")
    
    
    tk.Label(frame, text=(header[1])).grid(row=2,column=0,sticky="nsew")
    tk.Label(frame, text=(header[2])).grid(row=2,column=1,sticky="nsew")
    tk.Label(frame, text=(header[3])).grid(row=2,column=2,sticky="nsew")
    
    tk.Label(frame, text = "Elementy:").grid(row=3,column=0,sticky="nsew")
    tk.Button(frame, text = "Dodaj", command=lambda:addElement(detailsWindow,id)).grid(row =3, column = 4 ,sticky="nsew")

    db.execute("SELECT orderId, length, width, amount FROM ordersElements WHERE orderId LIKE ?",(id,))
    rekordy = db.fetchall()
    
    tk.Label(frame, text="Lp.").grid(row = 4, column=0, sticky="nsew")
    tk.Label(frame, text="Dlugosc przejscia (w mm)").grid(row = 4, column=1, sticky="nsew")
    tk.Label(frame, text="Szerokosc (w mm)").grid(row = 4, column=2, sticky="nsew")
    tk.Label(frame, text="Ilosc").grid(row = 4, column=3, sticky="nsew")
    
    for i, (id, length, width,amount) in enumerate(rekordy, start=1):
            tk.Label(frame, text=i, borderwidth=4, relief="groove").grid(row=i+5, column=0, sticky="nsew", padx=0, pady=5)
            tk.Label(frame, text=length, borderwidth=4, relief="groove").grid(row=i+5, column=1, sticky="nsew", padx=0, pady=5)
            tk.Label(frame, text=width, borderwidth=4, relief="groove").grid(row=i+5, column=2, sticky="nsew", padx=0, pady=5)   
            tk.Label(frame, text=amount, borderwidth=4, relief="groove").grid(row=i+5, column=3, sticky="nsew", padx=0, pady=5)
            tk.Button(frame, text = "Edytuj",command=lambda orderId = id,len = length, wid = width, am = amount:editElement(detailsWindow,orderId,len,wid,am)).grid(row=i+5, column=4, sticky="nsew",padx=15,pady=5)
        
    detailsWindow.bind_all("<MouseWheel>", on_mousewheel)
    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    detailsWindow.mainloop()
    
def writeEditedToDb(root,id,oldLen,oldWid,oldQ, len, wid, Q):
    len = len.get()
    wid = wid.get()
    Q = Q.get()
    db.execute("UPDATE ordersElements SET length = ?, width = ?, amount = ? WHERE orderID = ? AND length = ? AND width = ? AND amount = ?",(len,wid, Q, id, oldLen, oldWid, oldQ))
    dbConnection.commit()
    root.destroy()

def editElement(root,id, len, wid,q):
    editElementWindow = tk.Toplevel(root)
    editElementWindow.geometry("500x150+300+150")
    editElementWindow.focus_set()
    editElementWindow.grab_set()
    
    tk.Label(editElementWindow, text="Nowa dlugosc przejscia (w mm):").grid(row = 0, column = 0, padx=10,pady=10, sticky="nsew")
    tk.Label(editElementWindow, text="Nowa szerokosc (w mm):").grid(row = 0, column = 1, padx=10,pady=10, sticky="nsew")
    tk.Label(editElementWindow, text="Nowa ilosc:").grid(row = 0, column = 2, padx=10,pady=10, sticky="nsew")
    
    entry1 = tk.Entry(editElementWindow)
    entry1.grid(row = 1, column = 0, padx=10,pady=10, sticky="nsew")

    entry2 = tk.Entry(editElementWindow)
    entry2.grid(row = 1, column = 1, padx=10,pady=10, sticky="nsew")
    
    entry3 = tk.Entry(editElementWindow)
    entry3.grid(row = 1, column = 2, padx=10,pady=10, sticky="nsew")


    but1 = tk.Button(editElementWindow, text="Zaktualizuj",command=lambda: writeEditedToDb(root,id,len,wid,q,entry1,entry2,entry3))
    but1.grid(row=2, column=0, columnspan=3,padx=10,pady=20,sticky="nsew")
    
    editElementWindow.mainloop()



def deleteOrderFromDb(root,grandroot,id):
    db.execute("DELETE FROM ordersInProduction WHERE ID = ?",(id,))
    db.execute("DELETE FROM ordersElements WHERE orderID = ?",(id,))
    dbConnection.commit()
    root.destroy()
    grandroot.destroy()
    

def deleteOrder(root, id):
    deleteOrderWindow = tk.Toplevel(root)
    deleteOrderWindow.geometry("250x150")
    tk.Label(deleteOrderWindow, text="Czy na pewno chcesz usunac to zlecenie?").grid(row=0,column=0,columnspan=2, sticky="nsew",padx=10,pady=10)
    tk.Label(deleteOrderWindow, text="Ta operacja jest nieodwracalna!").grid(row=2,column=0,columnspan=2, sticky="nsew",padx=10,pady=10)
    tk.Button(deleteOrderWindow, text="Anuluj",command=lambda:deleteOrderWindow.destroy()).grid(row=3,column=0,sticky="nsew",padx=10,pady=10)
    tk.Button(deleteOrderWindow, text="Tak, chce usunac",command=lambda:deleteOrderFromDb(deleteOrderWindow,root,id)).grid(row=3,column=1,sticky="nsew",padx=10,pady=10)
    deleteOrderWindow.mainloop()
    



    #konczenie poloczenia z baza danych
    dbConnection.close()


