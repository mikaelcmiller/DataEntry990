# Data Entry 990 tool

import tkinter as tk
from tkinter import ttk
from tkinter import *
import pandas as pd
import pandas.io.sql as psql
import pyodbc
import os
import numpy as np

LARGE_FONT = ("Verdana", 12)

class Dataverse:
	def __init__(self):
		self.EIN = '444444444'
		self.Company = 'ERI'
		self.FormYear = '2018'
		self.FileLocation = 'location/location.pdf/location'
		self.Page1_Id = '0e0e0e0e'
		self.FileType = 'EO'
	
	def getnext(self, *event):
		print("Getnext Company")
		pyocnxn = pyodbc.connect("DRIVER={SQL Server};SERVER=SNADSSQ3;DATABASE=assessorwork;trusted_connection=yes;")
		nextform_sql = """ SELECT TOP 1 * from [ManualDataEntry].[990].[Next990ForEntry] where Page1_Id in ('0e0c6692','0e0c66d4','0e0c66f6','0e0c671e','0e0c672b','0e0c674b','0e0c678a','0e0c6797','0e0c67a7','0e0c67bc','0e0c67de','0e0c67fa','0e0c6813','0e0c6829','0e0c6856','0e0c6872','0e0c6889','0e0c68a9','0e0c68c4','0e0c68e6','0e0c6919','0e0c6929','0e0c6943','0e0c6957','0e0c697f','0e0c699f','0e0c69b8','0e0c6a2b','0e0c6a49','0e0c6a6a','0e0c6a84','0e0c6aad','0e0c6ad9','0e0c6b00','0e0c6b20','0e0c6b34','0e0c6b45','0e0c6b5f','0e0c6b7c','0e0c6b9b','0e0c6bc0','0e0c6bd3','0e0c6be6','0e0c6c06','0e0c6c21','0e0c6c3e','0e0c6c5f','0e0c6c9b','0e0c6cc1','0e0c6cec','0e0c6d01','0e0c6d12','0e0c6d2e','0e0c6d50','0e0c6d6d') """
		formdf = pd.DataFrame(psql.read_sql(nextform_sql, pyocnxn))
		p1id = formdf.loc[0,'Page1_Id']
		cursor = pyocnxn.cursor()
		updatefiling_sql = """ UPDATE [ManualDataEntry].[990].[Filing] set ExtractionCodeId=1 where Page1_Id = ? """
		cursor.execute(updatefiling_sql,p1id)
		pyocnxn.commit()
		pyocnxn.close()
		self.EIN = formdf.loc[0,'Ein']
		self.Company = formdf.loc[0,'Name']
		self.FormYear = str(formdf.loc[0,'FileDate'])[0:4]
		self.FileLocation = formdf.loc[0,'FileLocation']
		self.Page1_Id = formdf.loc[0,'Page1_Id']
		self.FileType = formdf.loc[0,'FileType']
		print("Getnext done")


class DE990App(tk.Tk):
	global Page1_Id
	global FileType
	
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		
		tk.Tk.wm_title(self,"990 Data Entry Tool")
		
		#self.data = Dataverse()
		
		#self.getnext()
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		
		self.frames = {}
		
		#Page List - use classes to create distinct pages
		for F in (StartPage, EOEntry, PFEntry):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="nsew")
		
		self.show_frame(StartPage)

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()
	
	#def getnext(*self):
	#	global Page1_Id
	#	global FileType
	#	print("GetNext active")
	#	pyocnxn = pyodbc.connect("DRIVER={SQL Server};SERVER=SNADSSQ3;DATABASE=assessorwork;trusted_connection=yes;")
	#	nextform_sql = """ SELECT TOP 1 * from [ManualDataEntry].[990].[Next990ForEntry] where Page1_Id in ('0e0c6692','0e0c66d4','0e0c66f6','0e0c671e','0e0c672b','0e0c674b','0e0c678a','0e0c6797','0e0c67a7','0e0c67bc','0e0c67de','0e0c67fa','0e0c6813','0e0c6829','0e0c6856','0e0c6872','0e0c6889','0e0c68a9','0e0c68c4','0e0c68e6','0e0c6919','0e0c6929','0e0c6943','0e0c6957','0e0c697f','0e0c699f','0e0c69b8','0e0c6a2b','0e0c6a49','0e0c6a6a','0e0c6a84','0e0c6aad','0e0c6ad9','0e0c6b00','0e0c6b20','0e0c6b34','0e0c6b45','0e0c6b5f','0e0c6b7c','0e0c6b9b','0e0c6bc0','0e0c6bd3','0e0c6be6','0e0c6c06','0e0c6c21','0e0c6c3e','0e0c6c5f','0e0c6c9b','0e0c6cc1','0e0c6cec','0e0c6d01','0e0c6d12','0e0c6d2e','0e0c6d50','0e0c6d6d') """
	#	formdf = pd.DataFrame(psql.read_sql(nextform_sql, pyocnxn))
	#	p1id = formdf.loc[0,'Page1_Id']
	#	cursor = pyocnxn.cursor()
	#	updatefiling_sql = """ UPDATE [ManualDataEntry].[990].[Filing] set ExtractionCodeId=1 where Page1_Id = ? """
	#	cursor.execute(updatefiling_sql,p1id)
	#	pyocnxn.commit()
	#	pyocnxn.close()
		
	#	Page1_Id = formdf.loc[0,'Page1_Id']
	#	FileType = formdf.loc[0,'FileType']
	#	#print('Page1_Id (getnext): '+Page1_Id)
	#	#print(formdf)
	#	print("Getnext Page1_Id: "+Page1_Id)
	#	print("Getnext FileType: "+FileType)
	#	if FileType=='EO': app.show_frame(EOEntry)
	#	else: app.show_frame(PFEntry)
	
	def submit(*self):
		print("Submitting data to SQL tables")




def qf(param):
	print(param)

class StartPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		label = tk.Label(self, text="Start Page", font=LARGE_FONT)
		label.pack(pady=10, padx=10)
		
		button2 = ttk.Button(self, text="EO Entry", 
			command=lambda: controller.show_frame(EOEntry))
		button2.pack()
		buttonPF = ttk.Button(self, text="PF Entry", 
			command=lambda: controller.show_frame(PFEntry))
		buttonPF.pack()


#def ptext(param):
#	print(param)
#thistext="Mikael"

class EOEntry(tk.Frame):
	thistext='2. Miller'
	def ttext2(self, param):
		print(param)
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		self.data = Dataverse()
		
		for x in range(21):
			colspacer = tk.Label(self, text = "."); colspacer.grid(row=0, column=x)
		for y in range(41):
			rowspacer = tk.Label(self, text = "."); rowspacer.grid(row=y, column=0)
		
		EINlabel = tk.Label(self, text="EIN"); EINlabel.grid(row=2,column=1,sticky="NW")
		Companylabel = tk.Label(self, text="Company"); Companylabel.grid(row=3,column=1,sticky="NW")
		FormYearlabel = tk.Label(self, text="Form Year"); FormYearlabel.grid(row=4,column=1,sticky="NW")
		FileLocationlabel = tk.Label(self, text="File Location"); FileLocationlabel.grid(row=5,column=1,sticky="NW")
		Page1_Idlabel = tk.Label(self, text="Page1_Id"); Page1_Idlabel.grid(row=6,column=1,sticky="NW")
		TotalEmployeeslabel = tk.Label(self, text="(P1L5) Total Employees"); TotalEmployeeslabel.grid(row=8,column=1,sticky="NW")
		TotalRevenuelabel = tk.Label(self, text="(P1L12C2) Total Revenue"); TotalRevenuelabel.grid(row=9,column=1,sticky="NW")
		TotalAssetsBoYlabel = tk.Label(self, text="(P1L20C1) Total Assets BoY"); TotalAssetsBoYlabel.grid(row=10,column=1,sticky="NW")
		TotalLiabilitiesBoYlabel = tk.Label(self, text="(P1L21C1) Total Liabilities BoY"); TotalLiabilitiesBoYlabel.grid(row=11,column=1,sticky="NW")
		TotalContributionslabel = tk.Label(self, text="(P1L8C2) Total Contributions"); TotalContributionslabel.grid(row=8,column=4,sticky="NW")
		TotalExpenseslabel = tk.Label(self, text="(P1L18C2) Total Expenses"); TotalExpenseslabel.grid(row=9,column=4,sticky="NW")
		TotalAssetsEoYlabel = tk.Label(self, text="(P1L20C2) Total Assets EoY"); TotalAssetsEoYlabel.grid(row=10,column=4,sticky="NW")
		TotalLiabilitiesEoYlabel = tk.Label(self, text="(P1L21C2) Total Liabilities EoY"); TotalLiabilitiesEoYlabel.grid(row=11,column=4,sticky="NW")
		#Namelabel = tk.Label(self, text="Name"); Namelabel.grid(row=14,column=1,sticky="NW")
		#Titlelabel = tk.Label(self, text="Title"); Titlelabel.grid(row=14,column=5,sticky="NW")
		#Hourslabel = tk.Label(self, text="Hours"); Hourslabel.grid(row=14,column=11,sticky="NW")
		#Reportablelabel = tk.Label(self, text="Reportable (Column D)"); Reportablelabel.grid(row=14,column=13,sticky="NW")
		#Relatedlabel = tk.Label(self, text="Related (Column E)"); Relatedlabel.grid(row=14,column=16,sticky="NW")
		#Otherlabel = tk.Label(self, text="Other (Column F)"); Otherlabel.grid(row=14,column=18,sticky="NW")
		ProblemCodeLabel = tk.Label(self, text="Problem Code (only if submitting no data)",fg="red"); ProblemCodeLabel.grid(row=37,column=1,sticky="NW",columnspan=3)
		UserLabel = tk.Label(self, text="User: "); UserLabel.grid(row=2,column=18,sticky="NW")
		
		
		#Dynamic/Updating Labels
		self.EIN = tk.Entry(self, width = 50, borderwidth=0,background="#f0f0f0")
		self.EIN.insert(0,self.data.EIN)
		self.EIN.grid(row=2,column=2,columnspan=13,sticky="NW")
		self.Company = tk.Entry(self, width = 100, borderwidth=0)#,background="#f0f0f0")
		self.Company.insert(0,self.data.Company)
		self.Company.grid(row=3,column=2,columnspan=13,sticky="NW")
		self.FormYear = tk.Entry(self, width = 50, borderwidth=0,background="#f0f0f0")
		self.FormYear.insert(0,self.data.FormYear)
		self.FormYear.grid(row=4,column=2,columnspan=13,sticky="NW")
		self.FileLocation = tk.Entry(self, width = 100, borderwidth=0,background="#f0f0f0")
		self.FileLocation.insert(0,self.data.FileLocation)
		self.FileLocation.grid(row=5,column=2,columnspan=13,sticky="NW")
		self.Page1_Id = tk.Entry(self, width = 50, borderwidth=0,background="#f0f0f0")
		self.Page1_Id.insert(0,self.data.Page1_Id)
		self.Page1_Id.grid(row=6,column=2,columnspan=13,sticky="NW")
		#self.FileType = tk.Label(self, text=self.data.FileType)
		#self.FileType.grid(row=7,column=2,sticky="NW")
		self.entries = [self.EIN,self.Company, self.FormYear, self.FileLocation, self.Page1_Id]
		for entry in self.entries:
			entry.config(state="readonly")
		
		## Problem code dropdown
		self.tkvar = StringVar(self)
		
		choices = ['                                        ','3  - No compensation','4  - Aggregate compensation only','5  - Not in English','6  - Compensation already in database','7  - Zero compensation in all categories','8  - Error with the pdf creation app','9  - Too old to look at','10 - Pdf was skipped in the entry tool','11 - Organization is not in a US state']
		self.tkvar.set('                                        ') # set the default option
		
		self.popupMenu = OptionMenu(self, self.tkvar, *choices)
		self.popupMenu.grid(row = 38, column =1)
		
		# on change dropdown value
		#def change_dropdown(*args):
		#	print( tkvar.get() )
		
		# link function to change dropdown
		#tkvar.trace('w', change_dropdown)
		
		## Company Financials Inputs
		self.clist = []
		for i in range(4):
			self.clist.append([])
			for x in range(2):
				e = Entry(self,width=15)
				if (x==0): e.grid(row=i+8,column=2)
				if (x==1): e.grid(row=i+8,column=5)
				self.clist[-1].append(e)
		
		## User Input Entries
		wmaster = 1150
		hmaster = 500
		self.entryframe = Frame(self,width=wmaster,height=hmaster)
		self.entryframe.grid(row=15,column=1,columnspan=19,rowspan=19)
		
		
		self.canvas = Canvas(self.entryframe,bg='#FFFFFF',width=wmaster,height=hmaster)
		self.vbar = Scrollbar(self.entryframe,orient=VERTICAL)
		self.vbar.pack(side=RIGHT,fill=Y)
		self.vbar.config(command=self.canvas.yview)
		self.canvas.config(yscrollcommand=self.vbar.set)
		self.canvas.pack(side=LEFT,expand=TRUE,fill=BOTH,anchor='nw')
		self.f2 = Frame(self.canvas,width=wmaster,height=700)
		self.canvas.create_window((0,0),window=self.f2,anchor='nw')
		
		#for x in range(7):
		#	colspacer = tk.Label(self.f2, text = "."); colspacer.grid(row=0, column=x)
		#for y in range(15):
		#	rowspacer = tk.Label(self.f2, text = "."); rowspacer.grid(row=y, column=0)
		
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))
		
		headerlabels = ['Name','Title','Hours','Reportable','Related','Other']
		for h in range(6):
			label = Label(self.f2, text=headerlabels[h])
			label.grid(row=0,column=h,sticky="NW")
		
		self.listofentries = []
		self.listofchecks = []
		self.rowrange = 15
		listofchk = ['Individual Trustee','Institutional Trustee','Officer','Key','Former']
		for i in range(self.rowrange): #rows
			self.listofentries.append([])
			self.listofchecks.append([])
			## Entries
			for x in range(6): #columns
				if (x==0 or x==1): e = Entry(self.f2, width=20)
				else: e = Entry(self.f2, width=10)
				e.grid(row=(((i+1)*2)-1),column=x)
				self.listofentries[-1].append(e)
			## Checkboxes
			self.chkframe = Frame(self.f2)
			self.chkframe.grid(row=(i+1)*2,column=1,columnspan=5)
			for x in range(5):
				c = IntVar()
				chk = Checkbutton(self.chkframe, text=listofchk[x],variable=c)
				chk.grid(row=0,column=(x+1))
				self.listofchecks[-1].append(c)
		
		
		
		getbtn = Button(self.f2, text="Get entries", command=self.getentries)
		getbtn.grid(row=7,column=7)
		
		buttonNext = ttk.Button(self, text="Next Form", 
			command=self.UpdateCompanyInfo)
		buttonNext.grid(row=4,column=18)
		buttonSubmit = ttk.Button(self, text="Submit", command=lambda: controller.submit())
		buttonSubmit.grid(row=38, column=18)
		
	def getentries(self,*event):
		companytodf = []
		for i in range(4):
			companytodf.append([])
			for j in range(2):
				companytodf[i].append(self.clist[i][j].get())
		print(companytodf)
		
		todf = []
		for i in range(self.rowrange):
			todf.append([])
			for j in range(6):
				todf[i].append(self.listofentries[i][j].get())
			for j in range(5):
				todf[i].append(self.listofchecks[i][j].get())
		#print(todf)
		
		df = pd.DataFrame(todf)
		df.replace('',np.nan,inplace=True)
		for d in range(6,11):
			df[d].replace(0,np.nan,inplace=True)
		df.dropna(how='all',inplace=True)
		print("Output Officer Data")
		df.replace(np.nan,'',inplace=True)
		print(df)
		# Send DF to Officers
		
		self.clearentries()
		
	def clearentries(self,*event):
		for i in range(4):
			for j in range(2):
				self.clist[i][j].delete(0,END)
		
		for i in range(self.rowrange):
			for j in range(6):
				self.listofentries[i][j].delete(0,END)
			for j in range(5):
				self.listofchecks[i][j].set(0)
		
		self.tkvar.set('                                        ')
		
		
	def UpdateCompanyInfo(self, *event):
		for entry in self.entries:
			entry.config(state=NORMAL)
		print("Updating Company Info")
		self.data.getnext()
		self.EIN.delete(0,END)
		self.EIN.insert(0,self.data.EIN)
		self.Company.delete(0,END)
		self.Company.insert(0,self.data.Company)
		self.FormYear.delete(0,END)
		self.FormYear.insert(0,self.data.FormYear)
		self.FileLocation.delete(0,END)
		self.FileLocation.insert(0,self.data.FileLocation)
		self.Page1_Id.delete(0,END)
		self.Page1_Id.insert(0,self.data.Page1_Id)
		#self.FileType.config(text=self.data.FileType)
		for entry in self.entries:
			entry.config(state="readonly")

class PFEntry(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		label = tk.Label(self, text="PF Entry", font=LARGE_FONT)
		label.pack(pady=10, padx=10)
		buttonhome = ttk.Button(self, text="Back to Home", 
			command=lambda: controller.show_frame(StartPage))
		buttonhome.pack()
		button2 = ttk.Button(self, text="EO Entry", 
			command=lambda: controller.show_frame(EOEntry))
		button2.pack()
		buttonNext = ttk.Button(self, text="Next", 
			command=lambda: controller.getnext())
		buttonNext.pack()
		buttonSubmit = ttk.Button(self, text="Submit", command=lambda: controller.submit())
		buttonSubmit.pack()




app = DE990App()
print("Opening 990 App")
app.mainloop()