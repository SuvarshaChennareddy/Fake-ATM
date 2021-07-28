import tkinter as tk
import sqlite3

LARGE_FONT=("Verdana",12, "bold")

conn = sqlite3.connect('users.db')
conn.execute("CREATE TABLE IF NOT EXISTS pins(id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, pin TEXT NOT NULL, balance INT NOT NULL)")
#conn.row_factory = lambda cursor, row: row[0]

#try:
#    conn.execute("CREATE UNIQUE INDEX idx ON pins(pin)")
#except:
#    pass

class container(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.winfo_toplevel().title("Fake ATM")
        global parent
        parent = tk.Frame(self, bg="#728bd4")

        global regPin
        global regBalance
        global loginPin
        global transactionMoney
        global changemsg
        global oldPin
        global newPin
        global regmsg
        global balanceamt
        global checkmsg
        global transmsg
        global delePin
        global delemsg
        regPin = tk.StringVar()
        regBalance = tk.DoubleVar()
        #loginName = tk.StringVar()
        loginPin = tk.StringVar()
        transactionMoney = tk.DoubleVar()
        changemsg = tk.StringVar()
        oldPin = tk.StringVar()
        newPin = tk.StringVar()
        regmsg = tk.StringVar()
        balanceamt = tk.StringVar()
        checkmsg = tk.StringVar()
        transmsg = tk.StringVar()
        delePin = tk.StringVar()
        delemsg = tk.StringVar()
        
        parent.pack(side="top", fill="both", expand=True)
        parent.grid_columnconfigure(0,weight=1)
        parent.grid_columnconfigure(2,weight=1)


        self.frames = {}

    def add(self, frameName, frame):
        self.frames[frameName] = frame
        self.frames[frameName].grid(row=0, column=1, sticky="nsew")

        
    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()
        if(cont == "Main"):
            regPin.set("")
            regBalance.set(0.0)
            #loginName = tk.StringVar()
            loginPin.set("")
            transactionMoney.set(0.0)
            changemsg.set("")
            oldPin.set("")
            newPin.set("")
            regmsg.set("")
            balanceamt.set("")
            checkmsg.set("")
            transmsg.set("")
            delePin.set("")
            delemsg.set("")
            



class page(tk.Frame):
    def __init__(self, parent, Name):
        self.i = 1
        tk.Frame.__init__(self, parent, bg="#728bd4")
        #self.place(x=0, y=0, anchor="nw", width=500, height=500)
        #self.configure(width=1000, height=1000)
        space = tk.Label(self,text="", bg="#728bd4")
        space.grid(row=0, column=1, sticky="nsew")
        label = tk.Label(self,text=Name,font=LARGE_FONT, bg="#728bd4", fg="#FFD700")
        label.grid(row=1, column=1, sticky="nsew")
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(2,weight=1)
        self.i+=1

    def addLabel(self, label):
        label["fg"] ="#FFD700"
        label["bg"] ="#728bd4"
        label.grid(row=self.i, column=1, sticky="nsew")
        self.i+=1
        

    def addButton(self, button):
        button.grid(row=self.i, column=1, sticky="nsew")
        self.i+=1
        
    def addEntry(self, entry):
        entry.grid(row=self.i, column=1, sticky="nsew")
        self.i+=1
        
def checkIfPinExists(pin, msg):
    cur = conn.cursor()
    cur.execute("SELECT pin FROM pins")
    data= cur.fetchall()
    out = [item for t in data for item in t]
    if(pin in out):
        msg.set("Error")
        return False
    else:
        msg.set("Successful")
        return True
        
        

def addUser():
    try:    
        if ((checkIfPinExists(regPin.get(), regmsg)) and (len(regPin.get()) == 4)):
            conn.execute("INSERT INTO pins(pin, balance) VALUES(" + regPin.get() + ", " + str(regBalance.get()) + ")")
        else:
            regmsg.set("Error")
    except:
        regmsg.set("Error")
    regPin.set(0)
    regBalance.set(0.0)
            
def check():
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM pins WHERE pin=" + loginPin.get())
        data= cur.fetchall()
        global out
        out = [item for t in data for item in t]
        if (len(out) == 0):
            checkmsg.set("Error")
        else:
            FakeATM.show_frame("Transaction")
            balanceamt.set("Current Balance: " + str(out[2]))
    except:
        checkmsg.set("Error")
        

def withdraw():
    try:
        bal = int(out[2])
        if(transactionMoney.get() > bal):
            transmsg.set("Error")
        else:
            bal = bal - transactionMoney.get()
            conn.execute("UPDATE pins SET balance=" + str(bal) + " WHERE pin=" + out[1])
            balanceamt.set("Current Balance: " + str(bal))
            out[2] = bal
            transmsg.set("Successful")
    except:
        transmsg.set("Error")


def deposit():
    try: 
        bal = int(out[2])
        bal = bal + transactionMoney.get()
        balanceamt.set("Current Balance: " + str(bal))
        conn.execute("UPDATE pins SET balance=" + str(bal) + " WHERE pin=" + out[1])
        out[2] = bal
        transmsg.set("Successful")
    except:
        transmsg.set("Error")

def change():
    try:
        if((not checkIfPinExists(oldPin.get(), changemsg)) is True):
            if ((checkIfPinExists(newPin.get(), changemsg)) and (len(newPin.get()) == 4)):
                conn.execute("UPDATE pins SET pin=" + newPin.get() + " WHERE pin=" + oldPin.get())
            else:
                changemsg.set("Error")
        else:
            changemsg.set("Error")
    except:
        changemsg.set("Error")
    oldPin.set("")
    newPin.set("")

def delete():
    try:
        if((not checkIfPinExists(delePin.get(), delemsg)) is True):
            conn.execute("DELETE FROM pins WHERE pin=" + delePin.get())
            delemsg.set("Successful")
        else:
            delemsg.set("Error")
            
    except:
        delemsg.set("Error")

    delePin.set("")
           
def popupOpen(event):
    global pop
    pop = tk.Menu(accSett2, tearoff=0)
    pop.add_command(label="Please make sure to contact your imaginary bank before proceeding and also take the necessary precautions. You have been warned! Click anywhere to close this..")
    try:
        pop.post(event.x_root, event.y_root)
    finally:
        pop.grab_release()

def popupClose(event):
    pop.unpost()
    
FakeATM = container()
#regName = tk.StringVar()

main = page(parent, "Fake ATM")
reg = page(parent, "Register")
login = page(parent, "Enter PIN")
transaction = page(parent, "Transaction")
accSett = page(parent, "Change PIN")
accSett2 = page(parent, "Delete Pin")


FakeATM.add("Main", main)
FakeATM.add("Regsiter", reg)
FakeATM.add("Login", login)
FakeATM.add("Transaction", transaction)
FakeATM.add("AccSett", accSett)
FakeATM.add("AccSett2", accSett2)

FakeATM.minsize(250, 300)

main.addLabel(tk.Label(main, text=""))
main.addButton(tk.Button(main, text="Register",
                         command=lambda: FakeATM.show_frame("Regsiter")))
main.addLabel(tk.Label(main, text=""))
main.addButton(tk.Button(main, text="Transaction",
                         command=lambda: FakeATM.show_frame("Login")))
main.addLabel(tk.Label(main, text=""))
main.addButton(tk.Button(main, text="Change PIN",
                         command=lambda: FakeATM.show_frame("AccSett")))
main.addLabel(tk.Label(main, text=""))
main.addButton(tk.Button(main, text="Delete PIN",
                         command=lambda: FakeATM.show_frame("AccSett2")))

#reg.addLabel(tk.Label(reg, text="User Name"))
#reg.addEntry(tk.Entry(reg, textvariable=))
#reg.addLabel(tk.Label(reg, text=""))
reg.addLabel(tk.Label(reg, text="PIN"))
reg.addEntry(tk.Entry(reg, textvariable=regPin))
reg.addLabel(tk.Label(reg, text=""))
reg.addLabel(tk.Label(reg, text="Balance"))
reg.addEntry(tk.Entry(reg, textvariable=regBalance))
reg.addLabel(tk.Label(reg, textvariable=regmsg))
reg.addButton(tk.Button(reg, text="Regsiter", command=addUser))
reg.addLabel(tk.Label(reg, text=""))
reg.addButton(tk.Button(reg, text="Go back to Main Page",
                         command=lambda: FakeATM.show_frame("Main")))

#login.addLabel(tk.Label(login, text="User Name"))
#login.addEntry(tk.Entry(login))
#login.addLabel(tk.Label(login, text=""))
login.addLabel(tk.Label(login, text="Insert Imaginary Card"))
login.addLabel(tk.Label(login, text=""))
login.addLabel(tk.Label(login, text="PIN"))
login.addEntry(tk.Entry(login, textvariable=loginPin))
login.addLabel(tk.Label(login, textvariable=checkmsg))
login.addButton(tk.Button(login, text="Submit",
                          command=check))
login.addLabel(tk.Label(login, text=""))
login.addButton(tk.Button(login, text="Go back to Main Page",
                         command=lambda: FakeATM.show_frame("Main")))

transaction.addLabel(tk.Label(transaction, textvariable=balanceamt))
transaction.addLabel(tk.Label(transaction, text="Amount:"))
transaction.addEntry(tk.Entry(transaction, textvariable=transactionMoney))
transaction.addLabel(tk.Label(transaction, textvariable=transmsg))
transaction.addButton(tk.Button(transaction, text="Withdraw", command=withdraw))
transaction.addButton(tk.Button(transaction, text="Deposit", command=deposit))
transaction.addLabel(tk.Label(transaction, text=""))
transaction.addButton(tk.Button(transaction, text="Go back to Main Page",
                         command=lambda: FakeATM.show_frame("Main")))

#accSett.addLabel(tk.Label(accSett, text="User Name"))
#accSett.addEntry(tk.Entry(accSett))
#accSett.addLabel(tk.Label(accSett, text=""))
accSett.addLabel(tk.Label(accSett, text="Old PIN"))
accSett.addEntry(tk.Entry(accSett, textvariable=oldPin))
accSett.addLabel(tk.Label(accSett, text=""))
accSett.addLabel(tk.Label(accSett, text="New PIN"))
accSett.addEntry(tk.Entry(accSett, textvariable=newPin))
accSett.addLabel(tk.Label(accSett, textvariable=changemsg))
accSett.addButton(tk.Button(accSett, text="Confirm",
                          command=change))
accSett.addLabel(tk.Label(accSett, text=""))
accSett.addButton(tk.Button(accSett, text="Go back to Main Page",
                         command=lambda: FakeATM.show_frame("Main")))

popupmsg = tk.Label(accSett2, text="More information...")
popupmsg.bind("<Enter>", popupOpen)
popupmsg.bind("<Leave>", popupClose)
accSett2.addLabel(popupmsg)
accSett2.addLabel(tk.Label(accSett2, text="PIN"))
accSett2.addEntry(tk.Entry(accSett2, textvariable=delePin))
accSett2.addLabel(tk.Label(accSett2, textvariable=delemsg))
accSett2.addButton(tk.Button(accSett2, text="Confirm",
                          command=delete))
accSett2.addLabel(tk.Label(accSett2, text=""))
accSett2.addButton(tk.Button(accSett2, text="Go back to Main Page",
                         command=lambda: FakeATM.show_frame("Main")))

FakeATM.show_frame("Main")
FakeATM.mainloop()
conn.commit()
conn.close()
    
"""
CREATE TABLE IF NOT EXISTS scripts (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, name TEXT NOT NULL, notes TEXT NOT NULL
CREATE UNIQUE INDEX idx_name ON scripts (name)
"""
