
from tkinter import *
from tkinter import ttk,messagebox
import csv
from datetime import datetime
import uuid


###############################DATA BASE##############################

import sqlite3

# สร้าง database
conn = sqlite3.connect('expense.sqlite3')
# สร้างตัวดำเนินการ
c = conn.cursor()

# สร้าง table ด้วยภาษา sql
# ['Transaction ID'(transactionID)--TEXT
# ,'รายการ'(title)--TEXT
# ,'ราคา'(price)--REAL
# ,'จำนวน'(quantity)--INTEGER
# ,'รวม'(total)--REAL
# ,'วัน-เวลา'(datetime)--TEXT
# ]
c.execute("""CREATE TABLE IF NOT EXISTS mypongp (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            transactionID TEXT,
            title TEXT,
            price REAL,
            quantity INTEGER,
            total REAL,
            datetime TEXT

             ) """)

def show_mypongp():
    with conn:
        c.execute("SELECT * FROM mypongp")
        expense = c.fetchall() # คำสั่งให้ดึงข้อมูลออกมา
        # #print(expense)
    return expense

def insert_mypongp(transactionID,title,price,quantity,total,datetime):
    ID = None
    with conn:
        c.execute("""INSERT INTO mypongp VALUES (?,?,?,?,?,?,?) """,
            ([ID,transactionID,title,price,quantity,total,datetime]))
    
    sqlite3.connect('expense.sqlite3').commit() # ก็คือ save ไฟล์นั่นเเหละ เเม่ย้อย !!!
    # #print('Insert success !!!')

def Edit_mypongp(transactionID,title,price,quantity,total):
    with conn:
        c.execute("""UPDATE mypongp SET title = ?,
             price = ? ,
             quantity = ?,
             total = ?
             WHERE transactionID = ?""",([title,price,quantity,total,transactionID]))
    conn.commit()
    # #print('Data Edited')

def delete_mypongp(TRANSACTIONID): 
    with conn:
        c.execute("DELETE FROM mypongp where transactionID =?",([TRANSACTIONID]))
    conn.commit()
    # #print('Delete complete !!!')





##############################DATA BASE###############################

################################# PROGRAM ####################



GUX = Tk()
GUX.title('โปรเเกรมพัฒนาโดยกุเอง V.1.0')

ws = GUX.winfo_screenwidth()
hs = GUX.winfo_screenheight()

x = (ws/2)-(300)
y = (hs/2)-(300)


GUX.geometry(f'600x600+{x:.0f}+{y:.0f}')


###################################### Menu Bar ####################################
menubar=Menu(GUX)
GUX.config(menu=menubar)

# 	File menu 
filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import CSV')


# 	Donate menu 

def About():
	# #print('About Menu')
	messagebox.showinfo('About','บริจาคมาดิไอเหี้ย !!!!')

Donatemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Donate',menu=Donatemenu)
Donatemenu.add_command(label='Just 1 Bitcoin',command=About)


# 	Help menu 

Helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=Helpmenu)
Helpmenu.add_command(label='Face Book')



Tab = ttk.Notebook(GUX)
T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill=BOTH,expand = 1)

icon_t1 = PhotoImage(file='Coin-icon.png')
icon_t2 = PhotoImage(file='Checklist-icon.png')
icon_t3 = PhotoImage(file='save-icon.png')


Tab.add(T1,text = f'{"Add Expense": ^30}',image=icon_t1,compound = 'top')
Tab.add(T2,text = f'{"Added Expense": ^30}',image=icon_t2,compound = 'top')

# T1 = Frame(T1)
# T1.pack()

days = {
	"Mon" : 'จันทร์',
	'Tue': "อังคาร",
	'Wed':'พุธ',
	'Thu':'พฤหัสบดี',
	'Fri': "ศุกร์",
	'Sat':'เสาร์',
	'Sun':'อาทิตย์',
}


def Save(event = None):
	expense = v_expense.get()
	price = v_price.get()
	quantity = v_quantity.get()

	if expense == '' and price =='' and quantity == '':
		# #print('No data')
		messagebox.showwarning('Error','กรุณากรอกข้อมูลทุกช่อง')
		return
	elif expense == '':
		messagebox.showwarning('Error','กรุณากรอกข้อมูลรายการ')
		return
	elif price == '':
		messagebox.showwarning('Error','กรุณากรอกข้อมูลราคา')
		return
	elif quantity == '':
		messagebox.showwarning('Error','กรุณากรอกข้อมูลจำนวน')
		return


	try:
		total = float(price)*float(quantity) #บรรทัดที่เราคิดว่าจะเกิด error (พวก format ตั่งต่าง)
		v_quantity.set('')
		v_price.set('')
		v_expense.set('')
		stamp = datetime.now()
		today = stamp.strftime('%a') # ไว้เอาไปใช้เเบบนี้: days["Mon"] = 'จันทร์'
		time_now = stamp.strftime('%Y-%m-%d %H:%M:%S')
		time_now = days[today] + '-' + time_now
		transactionID = stamp.strftime('%Y%m%d%H%M%f')
		text = 'รายการ: {} ราคา: {} \nจำนวน: {} ทั้งหมด: {}'.format(expense,price,quantity,total)
		v_result.set(text)
		# #print('รายการ: {} ราคา: {} จำนวน: {} ทั้งหมด: {}'.format(expense,price,quantity,total))

		#---------------- Sqlite --------------
		insert_mypongp(transactionID,expense,float(price),int(quantity),total,time_now)
		
		#----------- csv -----------------------------
		with open('ep6.csv','a',encoding = 'utf-8',newline = '') as f:

			fw = csv.writer(f) 
			data = [transactionID,expense,price,quantity,total,time_now]
			fw.writerow(data)
			
			
		
		E1.focus()
		update_table()
	except Exception as e:
		#print('ERROR: ',e)
		# messagebox.showerror('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		messagebox.showwarning('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		v_quantity.set('')
		v_price.set('')
		v_expense.set('')

#############################################

GUX.bind('<Return>',Save) # ----------- def Save(event=None) ------

FONT1 = (None,20)
#-------- image --------
money_icon = PhotoImage(file='money.png')
mainicon = Label(T1,image=money_icon)
mainicon.pack()


L = ttk.Label(T1,text='รายการ',font = FONT1).pack()
v_expense = StringVar()
E1 = ttk.Entry(T1,textvariable=v_expense,font = FONT1)
E1.pack()
#------------------------------------------------

L = ttk.Label(T1,text='ราคา',font = FONT1).pack()
v_price = StringVar()
E2 = ttk.Entry(T1,textvariable=v_price,font = FONT1).pack()
#------------------------------------------------

L = ttk.Label(T1,text='จำนวน',font = FONT1).pack()
v_quantity = StringVar()
E3 = ttk.Entry(T1,textvariable=v_quantity,font = FONT1)
E3.pack()
#------------------------------------------------
############# save ##################

B2 = ttk.Button(T1,text = 'save',command = Save,image=icon_t3,compound = 'left')
B2.pack()

v_result = StringVar()
v_result.set('-----------ผลลัพธ์-----------')
result = ttk.Label(T1,textvariable=v_result,font=FONT1,foreground='blue')
result.pack(pady=20)

#############################################################

def read_csv():
	
	with open('ep6.csv',newline='',encoding='utf-8') as f: 
		fr = csv.reader(f)
		data = list(fr)
		# #print(data[0][0])
	return data
#------------ ใช้ with เพราะกันลืมปิดไฟล์ !!!!!
#---------------------- วิธีทั่วๆไป --------------------------
	# f= open('ep6.csv',newline='',encoding='utf-8')
	# fr = csv.reader(f)
	# f.close()

L = ttk.Label(T2,text='ตารางเเสดงผลลัพธ์ทั้งหมด',font = FONT1).pack()

header = ['Transaction ID','รายการ','ราคา','จำนวน','รวม','วัน-เวลา']
resulttable = ttk.Treeview(T2,columns=header,show='headings',height=20)
resulttable.pack()

# for i in range(len(header)):
# 	resulttable.heading(header[i],text = header[i])

for h in header:
	resulttable.heading(h,text=h)


headerwidth = [150,150,80,80,90,170]

for h,w in zip(header,headerwidth):
	resulttable.column(h,width=w)
# for i in range(len(header)):
# 	resulttable.column(header[i],width=headerwidth[i])

# resulttable.insert('','end',value=['น้ำดื่ม','10','2','20','จันทร์'])




# def update_csv():
# 	with open('ep6.csv','w',newline='',encoding='utf-8') as f: 
# 		ABC = csv.writer(f)
# 		# เตรียมข้อมูลให้กลายเป็น list
# 		data = list(allTransaction.values())
# 		ABC.writerows(data)  # multiple line from nested list [[],[],[]]
# 		#print('Table was update')

def update_SQL():   #เอาค่าในตัวเเปร allTransaction ไปเก็บไว้ใน SQL
	data = list(allTransaction.values())
	# #print('DATA UPDATE: ',data)
	for d in data:
		Edit_mypongp(d[0],d[1],d[2],d[3],d[4]) #transactionID,title,price,quantity,total



allTransaction = {}  # ถูก assigne ค่าที่ ฟังก์ชัน update_table() โดยจะเก็บข้อมูลที่มีอยู่ทั้งหมดในดาต้าเบส



def delete_Record(event = None):
	select = resulttable.selection()
	if (select == ()):
		return
	check = messagebox.askyesno('Confirm','จะลบข้อมูลใช่ไหม')
	#print('delete')
	#print('Select: ',select)
	data = resulttable.item(select)
	#print('Pre_data: ',data)
	data = data['values']
	#print(data)
	transactionid = data[0]
	# #print('TransactionID: ',transactionid)
	del allTransaction[str(transactionid)]
	# #print('Post Transaction: ',allTransaction)
	# update_csv()
	delete_mypongp(str(transactionid)) # delete in database
	update_table() # อ่านข้อมูลใน SQL มาเก็บไว้ในตัวเเปร allTransaction ใหม่ เพื่อเเสดงผลบนตาราง
	





Delete_Button = ttk.Button(T2,text='delete',command=delete_Record)
Delete_Button.place(x=50,y=500)

resulttable.bind('<Delete>',delete_Record)

def update_table():
	resulttable.delete(*resulttable.get_children())
	# for i in resulttable.get_children():
	# 	resulttable.delete(i)
	try:
		data = show_mypongp()
		#print('Data test: ',data)
		for d in data:
			# create allTransaction
			allTransaction[d[1]] = d[1:]
			resulttable.insert('','end',values=d[1:])
		#print('allTransaction: ',allTransaction)
	except:
		print('No File')

update_table() #รันตอนที่โค้ดเริ่มรันครั้งเเรกเสมอ เพื่อเก็บตัวเเปร allTransaction มาก่อน

# Right Click Menu

def EditRecord():
	POPUP = Toplevel() # คล้ายๆกับ Tk()
	POPUP.title('Edit Record')
	ws = POPUP.winfo_screenwidth()
	hs = POPUP.winfo_screenheight()

	x = (ws/2)-(250)
	y = (hs/2)-(200)


	POPUP.geometry(f'500x400+{x:.0f}+{y:.0f}')
	
	L = ttk.Label(POPUP,text='รายการ',font = FONT1).pack()
	v_expense = StringVar()
	E1 = ttk.Entry(POPUP,textvariable=v_expense,font = FONT1)
	E1.pack()
	#------------------------------------------------

	L = ttk.Label(POPUP,text='ราคา',font = FONT1).pack()
	v_price = StringVar()# 
	E2 = ttk.Entry(POPUP,textvariable=v_price,font = FONT1).pack()
	#------------------------------------------------

	L = ttk.Label(POPUP,text='จำนวน',font = FONT1).pack()
	v_quantity = StringVar()# 
	E3 = ttk.Entry(POPUP,textvariable=v_quantity,font = FONT1)
	E3.pack()
	#------------------------------------------------

	def Edit():
		Old_Data = allTransaction[str(transactionid)]
		v1 = v_expense.get()
		v2 = float(v_price.get())
		v3 = float(v_quantity.get())
		total = v2*v3
		new_data = [Old_Data[0],v1,v2,v3,total,Old_Data[5]]  
		allTransaction[str(transactionid)] = new_data  #ทำการจัดการภายในตัวเเปร allTransaction ตัวนั้นๆก่อน
		# update_csv()
		update_SQL()   #เอาตัวเเปร allTransaction ทั้งหมดไปเก็บไว้ใน SQL
		update_table() #อ่านข้อมูลใน SQL มาเก็บไว้ในตัวเเปร allTransaction ใหม่ เพื่อเเสดงผลบนตาราง
		POPUP.destroy()



	B2 = ttk.Button(POPUP,text = 'save',command = Edit,image=icon_t3,compound = 'left')
	B2.pack()

	# get data in selected record
	select = resulttable.selection()
	data = resulttable.item(select)
	#print('Pre_data: ',data)
	data = data['values']
	#print(data)
	transactionid = data[0]
    # สั่งเซตค่าเก่าไว้ตรงช่องกรอก
	v_expense.set(data[1])
	v_price.set(data[2])
	v_quantity.set(data[3])




	POPUP.mainloop()




rightclick = Menu(GUX,tearoff=0)
rightclick.add_command(label='Edit',command=EditRecord)
rightclick.add_command(label='Delete',command=delete_Record)

def menupopup(event):
	select = resulttable.selection()
	if (select == ()):
		return
	#print(event.x_root, event.y_root)
	rightclick.post(event.x_root,event.y_root)

resulttable.bind('<Button-3>',menupopup)


	







GUX.mainloop()
