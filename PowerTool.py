from tkinter import *
import pymysql
import tkinter.ttk as ttk
from tkinter import messagebox
import time
def raiseFrame(frame):
    buttonState(frame)
    frame.tkraise()
    
def buttonState(frame):
    if(frame==itemFrame):
        viewAllItems()
        btnItem.config(state=DISABLED)
        btnRent.config(state="normal")
    elif(frame==rentFrame):
        viewAllRent()
        btnItem.config(state="normal")
        btnRent.config(state=DISABLED)
        
def dbConnection():
    global db,cursor
    db= pymysql.connect("localhost","root","26010","PowerTool" )
    cursor=db.cursor()
   

root = Tk()
root.title("Power Tools")
root.geometry("1518x786+0+2")
root.configure(bg='white',bd=20)
dbConnection()

dashboard=Frame(root)
dashboard.configure(bg="gray13",width=250,height=750)
dashboard.grid(row=1,column=0)  
itemFrame = Frame(root)
itemFrame.configure(bg="white",width=1476,height=750)
rentFrame = Frame(root)
rentFrame.configure(bg="white",width=1476,height=750)

#=========================================================================BtnFrame==============================================================================

btnRent=Button(dashboard,text="Rent",width=22,height=3,bg="darkcyan",fg="white",command=lambda:raiseFrame(rentFrame))
btnRent.place(x=10,y=15)
btnRent.configure(font=('vardhana', 13,'bold'))

btnItem=Button(dashboard,text="Item",width=22,height=3,bg="darkcyan",fg="white",command=lambda:raiseFrame(itemFrame))
btnItem.place(x=10,y=105)
btnItem.configure(font=('vardhana', 13,'bold'))
#=========================================================================ItemFrame Functions=====================================================================
def clearItemTextFields():
    t1.config(state="normal")
    t1.delete(0, 'end')
    t2.delete(0, 'end')
    t3.delete(0, 'end')
    t4.delete(0, 'end')
    t5.delete(0, 'end')
 
def addItem():
    dbConnection()
    sql = "insert into item values(%s,%s,%s,%s,%s)"
    val = (e1.get(),e2.get(),e3.get(),int(e4.get()),float(e5.get()))
    cursor.execute(sql, val)
    db.commit()
    db.close()
    viewAllItems()
    addItemWin.destroy()
    
def editItem():
    dbConnection()
    sql = "update item set itemName=%s,description=%s,quantity=%s,rentPrice=%s where itemCode =%s;"
    val = (t2.get(),t3.get(),int(t4.get()),float(t5.get()),t1.get())
    result=cursor.execute(sql, val)
    db.commit()
    db.close()
    if(result):
        messagebox.showinfo("", "Update Successful")
    else:
        messagebox.showinfo("", "Update Failed")
    viewAllItems()
    clearItemTextFields()
    
def deleteItem():
    msgBoxResult = messagebox.askokcancel("Python","Would you like to delete the data?")
    if(msgBoxResult):
        dbConnection()
        sql = "delete from item where itemCode = %s"
        val = (t1.get())
        result=cursor.execute(sql, val)
        db.commit()
        db.close()
        if(result):
            messagebox.showinfo("", "Delete Successful")
        else:
            messagebox.showinfo("", "Delete Failed")
        viewAllItems()
        clearItemTextFields()
def loadItem(event):
    if not itemTree.selection():
       print("ERROR")
    else:
        curItem = itemTree.focus()
        contents =(itemTree.item(curItem))
        selecteditem = contents['values']
        clearItemTextFields()
        t1.insert(0,selecteditem[0])
        t1.config(state="disabled")
        t2.insert(0,selecteditem[1])
        t3.insert(0,selecteditem[2])
        t4.insert(0,selecteditem[3])
        t5.insert(0,selecteditem[4])
       
def viewAllItems():
    dbConnection()
    cursor.execute("select * from item")
    itemList = cursor.fetchall()
    db.commit()
    db.close()
    for i in itemTree.get_children():
        itemTree.delete(i)
    for item in itemList:
        itemTree.insert('', 'end', values=item)
        
    
def newItemWindow():
    global addItemWin,e1,e2,e3,e4,e5
    addItemWin = Toplevel()
    addItemWin.configure(bg='white',bd=30)
    Label(addItemWin, text="Item Code",bg='white',width=20,height=3).grid(row=0)
    Label(addItemWin, text="Name",bg='white',width=20,height=3).grid(row=1)
    Label(addItemWin, text="Description",bg='white',width=20,height=3).grid(row=2)
    Label(addItemWin, text="Quantity",bg='white',width=20,height=3).grid(row=3)
    Label(addItemWin, text="RentPrice",bg='white',width=20,height=3).grid(row=4)
    e1 = Entry(addItemWin,width=20,bg='white',relief="solid")
    e2 = Entry(addItemWin,width=50,bg='white',relief="solid")
    e3 = Entry(addItemWin,width=100,bg='white',relief="solid")
    e4 = Entry(addItemWin,width=20,bg='white',relief="solid")
    e5 = Entry(addItemWin,width=20,bg='white',relief="solid")
    e1.grid(row=0, column=2,sticky=W, ipadx=10, ipady=4)
    e2.grid(row=1, column=2,sticky=W, ipadx=10, ipady=4)
    e3.grid(row=2, column=2,sticky=W, ipadx=10, ipady=4)
    e4.grid(row=3, column=2,sticky=W, ipadx=10, ipady=4)
    e5.grid(row=4, column=2,sticky=W, ipadx=10, ipady=4)

    btnAdd = Button(addItemWin,text="Add Item",fg="blue",bg='gray66',width=20,height=2,bd=0,command=addItem)
    btnAdd.place(x=640,y=230)
    addItemWin.mainloop()
#=========================================================================ItemFrame==============================================================================
Label(itemFrame, text="Item Form",bg='white',font=('vardhana', 25,'bold')).place(x=500,y=0)
frame1=Frame(itemFrame)
lb_header = ['Item Code','Name', 'Description','quantity','RentPrice']
itemTree =ttk.Treeview(frame1,height = 10,columns=lb_header, show="headings")
vsb = Scrollbar(frame1,orient="vertical", command=itemTree.yview)
hsb = Scrollbar(frame1,orient="horizontal", command=itemTree.xview)
itemTree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
itemTree.grid(column=0, row=0, sticky='nsew', in_=frame1)
vsb.grid(column=1, row=0, sticky='ns', in_=frame1)
hsb.grid(column=0, row=1, sticky='ew', in_=frame1)
itemTree.bind("<<TreeviewSelect>>", loadItem)
itemTree.grid(in_=frame1)
for col in lb_header:
    itemTree.heading(col, text=col.title())
frame1.place(x = 50, y = 70)

btnAddNew = Button(itemFrame,text="Add new Item",fg="darkcyan",width=20,height=2,bd=0,command=newItemWindow)
btnAddNew.place(x = 50, y = 350)

middleItemFrame=Frame(itemFrame)
middleItemFrame.configure(bg='white')
Label(middleItemFrame, text="Item Code",bg='white',width=20,height=3).grid(row=0)
Label(middleItemFrame, text="Name",bg='white',width=20,height=3).grid(row=1)
Label(middleItemFrame, text="Description",bg='white',width=20,height=3).grid(row=2)
Label(middleItemFrame, text="Quantity",bg='white',width=20,height=3).grid(row=3)
Label(middleItemFrame, text="RentPrice",bg='white',width=20,height=3).grid(row=4)
t1 = Entry(middleItemFrame,width=20,relief=RIDGE)
t2 = Entry(middleItemFrame,width=50,relief=RIDGE)
t3 = Entry(middleItemFrame,width=100,relief=RIDGE)
t4 = Entry(middleItemFrame,width=20,relief=RIDGE)
t5 = Entry(middleItemFrame,width=20,relief=RIDGE)
t1.grid(row=0, column=2,sticky=W, ipadx=10, ipady=4)
t2.grid(row=1, column=2,sticky=W, ipadx=10, ipady=4)
t3.grid(row=2, column=2,sticky=W, ipadx=10, ipady=4)
t4.grid(row=3, column=2,sticky=W, ipadx=10, ipady=4)
t5.grid(row=4, column=2,sticky=W, ipadx=10, ipady=4)
middleItemFrame.place(x = 40, y = 400)

btnEditItem = Button(itemFrame,text="Edit Item",fg="blue",bg='gray76',width=15,height=2,bd=0,command=editItem)
btnEditItem.place(x=760,y=620)
btnDeleteItem = Button(itemFrame,text="Delete Item",fg="red",bg='gray76',width=15,height=2,bd=0,command=deleteItem)
btnDeleteItem.place(x=890,y=620)
#=========================================================================RentFrame Functions==============================================================================
def clearRentTextFields():
    rt1.config(state="normal")
    rt1.delete(0, 'end')
    rt2.delete(0, 'end')
    rt3.delete(0, 'end')
    rt4.delete(0, 'end')
    rt5.delete(0, 'end')
    rt6.delete(0, 'end')
    rt7.delete(0, 'end')
    
def loadRent(event):
    curItem = rentFormTree.focus()
    contents =(rentFormTree.item(curItem))
    selecteditem = contents['values']
    clearRentTextFields()
    rt1.insert(0,selecteditem[0])
    rt1.config(state="disabled")
    rt2.insert(0,selecteditem[1])
    rt3.insert(0,selecteditem[2])
    rt4.insert(0,selecteditem[3])
    rt5.insert(0,selecteditem[4])
    rt6.insert(0,selecteditem[5])
    rt7.insert(0,selecteditem[6]) 
def saveRent():
    dbConnection()
    sql = "insert into Rent values(%s,%s,%s,%s,%s,%s,%s)"
    val = (rtn1.get(),rtn2.get(),rtn3.get(),rtn4.get(),int(rtn5.get()),float(rtn6.get()),rtn7.get())
    cursor.execute(sql, val)
    db.commit()
    db.close()
    viewAllRent()
    addRentWin.destroy()
    
def editRent():
    dbConnection()
    sql = "update rent set customerName=%s,nic=%s,itemCode=%s,quantity=%s,rentPrice=%s,date=%s where rentId =%s;"
    val = (rt2.get(),rt3.get(),rt4.get(),int(rt5.get()),float(rt6.get()),rt7.get(),rt1.get())
    result=cursor.execute(sql, val)
    db.commit()
    db.close()
    if(result):
        messagebox.showinfo("", "Update Successful")
    else:
        messagebox.showinfo("", "Update Failed")
    viewAllRent()
    clearRentTextFields()
    
def deleteRent():
    msgBoxResult = messagebox.askokcancel("Delete Rent","Would you like to delete the data?")
    if(msgBoxResult):
        dbConnection()
        sql = "delete from rent where rentId = %s"
        val = (rt1.get())
        result=cursor.execute(sql, val)
        db.commit()
        db.close()
        if(result):
            messagebox.showinfo("", "Delete Successful")
        else:
            messagebox.showinfo("", "Delete Failed")
        viewAllRent()
        clearRentTextFields()
        
def viewAllRent():
    dbConnection()
    cursor.execute("select * from Rent")
    rentList = cursor.fetchall()
    db.commit()
    db.close()
    for i in rentFormTree.get_children():
        rentFormTree.delete(i)
    for rent in rentList:
        rentFormTree.insert('', 'end', values=rent)
        
def loadComboBox():
    dbConnection()
    cursor.execute("select * from item")
    itemlist = cursor.fetchall()
    db.commit()
    db.close()
    rtn4.delete(0, END)
    comboValues=[]
    for item in itemlist:
        comboValues.append(item[0])
    rtn4['values']=comboValues
    
def fillTxtValues(event):
    dbConnection()
    sql="select * from item where itemCode=%s"
    selectedCode=rtn4.get()
    cursor.execute(sql, selectedCode)
    itemTupple=cursor.fetchall()
    item=itemTupple[0]
    rtn5.delete(0,'end')
    rtn6.delete(0,'end')
    rtn5.insert(0,item[3])
    rtn6.insert(0,item[4])
    

        
def newRentWindow():
    global addRentWin,rtn1,rtn2,rtn3,rtn4,rtn5,rtn6,rtn7
    addRentWin = Toplevel()
    addRentWin.configure(bg='white',bd=30)
    addRentWin.geometry("900x686+300+70")
    Label(addRentWin, text="Available Items",bg='white',width=20,height=3,font=('vardhana', 11,'bold')).place(x=0,y=0)
    viewFrame=Frame(addRentWin)
    viewFrame.configure(bg='white')
    lb_header = ['Item Code','Name','quantity']
    itemtable =ttk.Treeview(viewFrame,height = 6,columns=lb_header, show="headings")
    vsb = Scrollbar(viewFrame,orient="vertical", command=itemtable.yview)
    hsb = Scrollbar(viewFrame,orient="horizontal", command=itemtable.xview)
    itemtable.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    itemtable.grid(column=0, row=0, sticky='nsew', in_=viewFrame)
    vsb.grid(column=1, row=0, sticky='ns', in_=viewFrame)
    hsb.grid(column=0, row=1, sticky='ew', in_=viewFrame)
    itemtable.bind("<<TreeviewSelect>>", loadItem)
    itemtable.grid(in_=viewFrame)
    for col in lb_header:
        itemtable.heading(col, text=col.title())
    viewFrame.place(x=30,y=50)

    dbConnection()
    cursor.execute("select * from rent")
    rentList = cursor.fetchall()
    cursor.execute("select * from item")
    itemList = cursor.fetchall()
    newItemList=[]
    for item in itemList:
        newQty=item[3]
        for rent in rentList:
            if(rent[3]==item[0]):
                newQty-=rent[4]
        if(newQty):
            newItemList.append((item[0],item[1],newQty,item[4]))
    for item in newItemList:
        itemtable.insert('', 'end', values=item)

    frame1=Frame(addRentWin)
    frame1.configure(bg='white',bd=30)
    Label(frame1, text="Rent ID",bg='white',width=20,height=3).grid(row=0)
    Label(frame1, text="Customer Name",bg='white',width=20,height=3).grid(row=1)
    Label(frame1, text="NIC",bg='white',width=20,height=3).grid(row=2)
    Label(frame1, text="Item Code",bg='white',width=20,height=3).grid(row=3)
    Label(frame1, text="Quantity",bg='white',width=20,height=3).grid(row=4)
    Label(frame1, text="RentPrice",bg='white',width=20,height=3).grid(row=5)
    Label(frame1, text="Date",bg='white',width=20,height=3).grid(row=6)
    rtn1 = Entry(frame1,width=20,relief="solid")
    rtn2 = Entry(frame1,width=50,relief="solid")
    rtn3 = Entry(frame1,width=100,relief="solid")
    rtn4 = ttk.Combobox(frame1)
    rtn4.bind("<<ComboboxSelected>>",fillTxtValues)
    rtn5 = Entry(frame1,width=20,relief="solid")
    rtn6 = Entry(frame1,width=20,relief="solid")
    rtn7 = Entry(frame1,width=20,relief="solid")
    rtn1.grid(row=0, column=2,sticky=W, ipadx=10, ipady=4)
    rtn2.grid(row=1, column=2,sticky=W, ipadx=10, ipady=4)
    rtn3.grid(row=2, column=2,sticky=W, ipadx=10, ipady=4)
    rtn4.grid(row=3, column=2,sticky=W, ipadx=10, ipady=4)
    rtn5.grid(row=4, column=2,sticky=W, ipadx=10, ipady=4)
    rtn6.grid(row=5, column=2,sticky=W, ipadx=10, ipady=4)
    rtn7.grid(row=6, column=2,sticky=W, ipadx=10, ipady=4)
    rtn7.insert(0,time.strftime("%d/%m/%Y"))
    
    btnAdd = Button(frame1,text="Save Rent",fg="blue",bg='gray66',width=20,height=2,bd=0,command=saveRent)
    btnAdd.place(x=640,y=320)
    frame1.place(x=0,y=200)
    loadComboBox()
    addRentWin.mainloop()     
#=========================================================================RentFrame ==============================================================================
Label(rentFrame, text="Rent Form",bg='white',font=('vardhana', 25,'bold')).place(x=500,y=0)
frame2=Frame(rentFrame)
rentLbHeader = ['RentID','Name','NIC', 'Item Code','quantity','Rent Price','Date']
rentFormTree =ttk.Treeview(frame2,height = 10,columns=rentLbHeader, show="headings")
rentFormTree.column('RentID',minwidth=0,width=80,anchor="center") 
rentFormTree.column('NIC',minwidth=0,width=200,anchor="center")
rentFormTree.column('Item Code',minwidth=0,width=100,anchor="center")
rentFormTree.column('quantity',minwidth=0,width=100,anchor="center")
rentFormTree.column('Rent Price',minwidth=0,width=100,anchor="center")
rentFormTree.column('Date',minwidth=0,width=150,anchor="c")

vsb = Scrollbar(frame2,orient="vertical", command=rentFormTree.yview)
hsb = Scrollbar(frame2,orient="horizontal", command=rentFormTree.xview)
rentFormTree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
rentFormTree.grid(column=0, row=0, sticky='nsew', in_=frame2)
vsb.grid(column=1, row=0, sticky='ns', in_=frame2)
hsb.grid(column=0, row=1, sticky='ew', in_=frame2)
rentFormTree.bind("<<TreeviewSelect>>", loadRent)
for col in rentLbHeader:
    rentFormTree.heading(col, text=col.title())
frame2.place(x = 50, y = 70)

btnAddNew = Button(rentFrame,text="New Rent",fg="darkcyan",width=20,height=2,bd=0,command=newRentWindow)
btnAddNew.place(x = 50, y = 350)

middleFrame=Frame(rentFrame)
middleFrame.configure(bg='white')
Label(middleFrame, text="Rent ID",bg='white',width=20,height=2).grid(row=0)
Label(middleFrame, text="Customer Name",bg='white',width=20,height=2).grid(row=1)
Label(middleFrame, text="NIC",bg='white',width=20,height=2).grid(row=2)
Label(middleFrame, text="Item Code",bg='white',width=20,height=2).grid(row=3)
Label(middleFrame, text="Quantity",bg='white',width=20,height=2).grid(row=4)
Label(middleFrame, text="RentPrice",bg='white',width=20,height=2).grid(row=5)
Label(middleFrame, text="Date",bg='white',width=20,height=2).grid(row=6)
    
rt1 = Entry(middleFrame,width=20,relief=RIDGE)
rt2 = Entry(middleFrame,width=50,relief=RIDGE)
rt3 = Entry(middleFrame,width=100,relief=RIDGE)
rt4 = Entry(middleFrame,width=20,relief=RIDGE)
rt5 = Entry(middleFrame,width=20,relief=RIDGE)
rt6 = Entry(middleFrame,width=20,relief=RIDGE)
rt7 = Entry(middleFrame,width=20,relief=RIDGE)
rt1.grid(row=0, column=2,sticky=W, ipadx=10, ipady=2)
rt2.grid(row=1, column=2,sticky=W, ipadx=10, ipady=2)
rt3.grid(row=2, column=2,sticky=W, ipadx=10, ipady=2)
rt4.grid(row=3, column=2,sticky=W, ipadx=10, ipady=2)
rt5.grid(row=4, column=2,sticky=W, ipadx=10, ipady=2)
rt6.grid(row=5, column=2,sticky=W, ipadx=10, ipady=2)
rt7.grid(row=6, column=2,sticky=W, ipadx=10, ipady=2)
middleFrame.place(x = 40, y = 400)

btnEdit = Button(rentFrame,text="Edit",fg="blue",bg='gray76',width=15,height=2,bd=0,command=editRent)
btnEdit.place(x=760,y=620)
btnDelete = Button(rentFrame,text="Delete",fg="red",bg='gray76',width=15,height=2,bd=0,command=deleteRent)
btnDelete.place(x=890,y=620)



#=======================================================================================================================================================
for frame in (itemFrame, rentFrame):
    frame.grid(row=1, column=1, sticky='news')

  
raiseFrame(rentFrame)
root.mainloop()
