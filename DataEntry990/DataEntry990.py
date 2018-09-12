# Data Entry 990 tool

import tkinter as tk
from tkinter import ttk
import pandas as pd
import pandas.io.sql as psql
import pyodbc
import os

LARGE_FONT = ("Verdana", 12)


class NextForm:
	def getnext(self):
		self.pyocnxn = pyodbc.connect("DRIVER={SQL Server};SERVER=SNADSSQ3;DATABASE=assessorwork;trusted_connection=yes;")
		self.nextform_sql = """ SELECT TOP 1 * from [ManualDataEntry].[990].[Next990ForEntry] """
		self.formdf = pd.DataFrame(psql.read_sql(self.nextform_sql, self.pyocnxn))
		p1id = self.formdf.loc[0,'Page1_Id']
		#print(p1id)
		cursor = self.pyocnxn.cursor()
		self.updatefiling_sql = """ UPDATE [ManualDataEntry].[990].[Filing] set ExtractionCodeId=1 where Page1_Id = ? """
		cursor.execute(self.updatefiling_sql,p1id)
		self.pyocnxn.commit()
		self.pyocnxn.close()
		print(self.formdf)

class DE990App(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		
		tk.Tk.wm_title(self,"990 Data Entry Tool")
		
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		
		self.frames = {}
		
		#Page List - use classes to create distinct pages
		for F in (StartPage, PageOne, PageTwo, PFEntry):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="nsew")
		
		self.show_frame(StartPage)

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()
	
	#NF = NextForm()
	#NF.getnext()
	

def qf(param):
	print(param)

class StartPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		label = tk.Label(self, text="Start Page", font=LARGE_FONT)
		label.pack(pady=10, padx=10)
		
		button1 = ttk.Button(self, text="Visit Page 1", 
			command=lambda: controller.show_frame(PageOne))
		button1.pack()
		button2 = ttk.Button(self, text="Visit Page 2", 
			command=lambda: controller.show_frame(PageTwo))
		button2.pack()
		buttonPF = ttk.Button(self, text="PF Entry", 
			command=lambda: controller.show_frame(PFEntry))
		buttonPF.pack()

class PageOne(tk.Frame):
	thistext='1. Mikael'
	def ttext(self, param):
		print(param)
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page One", font=LARGE_FONT)
		label.pack(pady=10, padx=10)
		buttonhome = ttk.Button(self, text="Back to Home", 
			command=lambda: controller.show_frame(StartPage))
		buttonhome.pack()
		button2 = ttk.Button(self, text="Visit Page 2", 
			command=lambda: controller.show_frame(PageTwo))
		button2.pack()
		buttonprint = ttk.Button(self, text="Print 'Mikael'", command=lambda: self.ttext(self.thistext))
		buttonprint.pack()
		buttonPF = ttk.Button(self, text="PF Entry", 
			command=lambda: controller.show_frame(PFEntry))
		buttonPF.pack()
		NF = NextForm()
		nfbtn = ttk.Button(self, text="Next Form", command=NF.getnext)
		nfbtn.pack()

#def ptext(param):
#	print(param)
#thistext="Mikael"

class PageTwo(tk.Frame):
	thistext='2. Miller'
	def ttext2(self, param):
		print(param)
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Page Two!", font=LARGE_FONT)
		label.pack(pady=10, padx=10)
		buttonhome = ttk.Button(self, text="Back to Home", 
			command=lambda: controller.show_frame(StartPage))
		buttonhome.pack()
		button1 = ttk.Button(self, text="Visit Page 1", 
			command=lambda: controller.show_frame(PageOne))
		button1.pack()
		buttonprint2 = ttk.Button(self, text="Print 'Miller'", command=lambda: self.ttext2(self.thistext))
		buttonprint2.pack()
		buttonPF = ttk.Button(self, text="PF Entry", 
			command=lambda: controller.show_frame(PFEntry))
		buttonPF.pack()
		NF = NextForm()
		nfbtn = ttk.Button(self, text="Next Form", command=NF.getnext)
		nfbtn.pack()

class PFEntry(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="PF Entry", font=LARGE_FONT)
		label.pack(pady=10, padx=10)
		buttonhome = ttk.Button(self, text="Back to Home", 
			command=lambda: controller.show_frame(StartPage))
		buttonhome.pack()
		button1 = ttk.Button(self, text="Visit Page 1", 
			command=lambda: controller.show_frame(PageOne))
		button1.pack()
		button2 = ttk.Button(self, text="Visit Page 2", 
			command=lambda: controller.show_frame(PageTwo))
		button2.pack()
		NF = NextForm()
		nfbtn = ttk.Button(self, text="Next Form", command=NF.getnext)
		nfbtn.pack()
	


app = DE990App()
print("Opening 990 App")
app.mainloop()