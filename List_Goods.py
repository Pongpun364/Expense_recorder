
from tkinter import *
from tkinter import ttk,messagebox
import csv
from datetime import datetime
GUX = Tk()
GUX.title('โปรเเกรมพัฒนาโดยกุเอง')
GUX.geometry('600x600+1035+50')


######################################Menu Bar####################################
menubar=Menu(GUX)
GUX.config(menu=menubar)

# 	File menu 
filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import CSV')




# 	Donate menu 

def About():
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
		print('No data')
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
		today = datetime.now().strftime('%a') # ไว้เอาไปใช้เเบบนี้: days["Mon"] = 'จันทร์'
		time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		time_now = days[today] + '-' + time_now
		text = 'รายการ: {} ราคา: {} \nจำนวน: {} ทั้งหมด: {}'.format(expense,price,quantity,total)
		v_result.set(text)
		print('รายการ: {} ราคา: {} จำนวน: {} ทั้งหมด: {}'.format(expense,price,quantity,total))
		#----------- csv -----------------------------
		with open('ep6.csv','a',encoding = 'utf-8',newline = '') as f:

			fw = csv.writer(f) 
			data = [expense,price,quantity,str(total),time_now]
			fw.writerow(data)
			
		
		E1.focus()
		update_table()
	except Exception as e:
		print('ERROR: ',e)
		# messagebox.showerror('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		messagebox.showwarning('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		v_quantity.set('')
		v_price.set('')
		v_expense.set('')

# ���������ö�� enter ��
GUX.bind('<Return>',Save) # ----------- def Save(event=None) ------

FONT1 = (None,20)
#-------- image --------
money_icon = PhotoImage(file='money.png')
mainicon = Label(T1,image=money_icon)
mainicon.pack()


L = ttk.Label(T1,text='รายการ',font = FONT1).pack()
v_expense = StringVar()# �����þ��������Ѻ�红������ GUI
E1 = ttk.Entry(T1,textvariable=v_expense,font = FONT1)
E1.pack()
#------------------------------------------------

L = ttk.Label(T1,text='ราคา',font = FONT1).pack()
v_price = StringVar()# �����þ��������Ѻ�红������ GUI
E2 = ttk.Entry(T1,textvariable=v_price,font = FONT1).pack()
#------------------------------------------------

L = ttk.Label(T1,text='จำนวน',font = FONT1).pack()
v_quantity = StringVar()# �����þ��������Ѻ�红������ GUI
E3 = ttk.Entry(T1,textvariable=v_quantity,font = FONT1)
E3.pack()
#------------------------------------------------


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
		# print(data[0][0])
	return data
#------------ ใช้ with เพราะกันลืมปิดไฟล์ !!!!!
#---------------------- วิธีทั่วๆไป --------------------------
	# f= open('ep6.csv',newline='',encoding='utf-8')
	# fr = csv.reader(f)
	# f.close()

L = ttk.Label(T2,text='ตารางเเสดงผลลัพธ์ทั้งหมด',font = FONT1).pack()

header = ['รายการ','ราคา','จำนวน','รวม','วัน-เวลา']
resulttable = ttk.Treeview(T2,columns=header,show='headings',height=20)
resulttable.pack()

# for i in range(len(header)):
# 	resulttable.heading(header[i],text = header[i])

for h in header:
	resulttable.heading(h,text=h)

headerwidth = [150,80,80,90,170]

for h,w in zip(header,headerwidth):
	resulttable.column(h,width=w)
# for i in range(len(header)):
# 	resulttable.column(header[i],width=headerwidth[i])

# resulttable.insert('','end',value=['น้ำดื่ม','10','2','20','จันทร์'])



def update_table():
	resulttable.delete(*resulttable.get_children())
	# for i in resulttable.get_children():
	# 	resulttable.delete(i)
	data = read_csv()
	for d in data:
		resulttable.insert('','end',values=d)

	














GUX.mainloop()
