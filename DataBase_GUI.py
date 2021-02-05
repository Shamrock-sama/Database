# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 09:30:35 2021

@author: Jin Zhu
"""


import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfilename
from tkinter import messagebox
import json
import itertools
import time
import threading
import uuid
import re
import math
import load
import os
from time import strftime 
  
    
class BackendProcess:
    def __init__(self):
        self.finished = False

    def task(self):
        time.sleep(2)
        print('finished')
        self.finished = True

    def run(self):
        thread = threading.Thread(target=self.task, daemon=True)
        thread.start() 


def updatelist(option, menu, key):
    menu['menu'].delete(0, 'end')
    for choice in key:
        menu['menu'].add_command(label=choice, command=tk._setit(option, choice))
    menu['menu'].add_command(label='None', command=tk._setit(option, 'None'))   


def getfloat(text):
    if text is not None:
        if isinstance(text, str):
            if text == '/' or text == '-':
                return 0
            elif re.findall(r'\d+', text):
                return float(re.search(r'\d+', text).group())
            else:
                return text
        elif math.isnan(text):
            return 0
        else:
            return float(text)
    else:
        return 0


def find_key(val, dic):
    for k,v in dic.items():
        if isinstance(v, dict):
            p = find_key(val, v)
            if p:
                return [k] 
        elif getfloat(v) == val:
            return [k]


def superfilter(data, key):
    if key == '金风':
        return [i for i in data.keys() if re.findall(r'\AGW', i)]
    elif key == '远景':
        return [i for i in data.keys() if re.findall(r'\AEN', i)]
    elif key == '中车':
        return [i for i in data.keys() if re.findall(r'\AWT', i)]
    elif key == '明阳':
        return [i for i in data.keys() if re.findall(r'\AM', i)]
    elif key == '三一':
        return [i for i in data.keys() if re.findall(r'\ASE', i)]    

def getKey(data):
    length_1 = 0
    for i in range(len(data)):
        if length_1 < len(list(data.values())[i].keys()):
            length_1 = len(list(data.values())[i].keys())
            KeyList = list(list(data.values())[0].keys())                   
    length_i = 0
    Parameter_i = []
    for i in range(len(data)):
        Parameter_2 = []
        length_2 = 0
        for item in list(list(data.values())[i].values()):
            if list(item.keys()):
                length_2 += len(list(item.keys()))
                Parameter_2.append(list(item.keys()))
        if length_i < length_2:
            length_i = length_2
            Parameter_i = Parameter_2
    Parameter = Parameter_i  
    return KeyList, Parameter


def Dictfilter(Dict, key1=None, key2=None):
    info = []
    if key2:
        for project in Dict.values():
            info.append(project.get(key1, {}).get(key2))    
    elif key1:
        for project in Dict.values():
            info.append(project.get(key1, {}))
    else:
        for project in Dict.values():
            info.append(project)
    return info


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):       
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, "D:\\spyder_run\\database\\ramble.ico")
        tk.Tk.wm_title(self, "DataRamble")                
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Front Page", font=LARGE_FONT)
        label.pack()
        button = ttk.Button(self, text="Manage",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()
        button2 = ttk.Button(self, text="Look-up",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()
        button3 = ttk.Button(self, text="Graph",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()  
        preface = 'When you look at a single digit, it means nothing. \
        \nBut when you look at a bunch of numbers, it can be everything.\
        \nData are rambling. Some of them strolled away and regathered in this hub.'
        label2 = tk.Label(self, text=preface, font = ('calibri', 12, 'bold'), 
                          borderwidth=4, relief="solid", background="white", foreground="black")
        label2.pack()
        label3 = tk.Label(self, font = ('calibri', 40, 'bold'), 
            background = 'white', 
            foreground = 'black') 
        label3.pack()
        self.Time(label3)

    def Time(self, label): 
        string = strftime('%H:%M:%S %p') 
        label.config(text = string) 
        label.after(1000, time) 

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Database management!", font=LARGE_FONT)
        label.grid()      
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(row=10, column=4, sticky=tk.EW)
        self.process = BackendProcess()
        self.widget()
        
    def widget(self):
        button2 = tk.Button(self, text='Update', command=self.Update)
        button2.grid(row=2, column=4, sticky=tk.EW)        
        button3 = ttk.Button(self, text='Data path', command=self.folderpath)
        button3.grid(row=1, column=1, sticky=tk.EW)
        button4 = ttk.Button(self, text='Output path', command=self.savepath)
        button4.grid(row=2, column=1, sticky=tk.EW)
        self.path1 = tk.StringVar(self)
        self.path1.set('')
        Entry1 = tk.Entry(self, text=self.path1)
        Entry1.grid(row=1, column=2, columnspan=2, sticky=tk.EW)
        self.path2 = tk.StringVar(self)
        self.path2.set('')
        Entry2 = tk.Entry(self, text=self.path2)
        Entry2.grid(row=2, column=2, columnspan=2, sticky=tk.EW)
        self.var1 = tk.IntVar(self)
        tk.Checkbutton(self, text="Load/Update Load", variable=self.var1).grid(row=1, column=0, sticky=tk.EW)
        self.var2 = tk.IntVar(self)
        tk.Checkbutton(self, text="Load/Update Power", variable=self.var2).grid(row=2, column=0, sticky=tk.EW)
        Label2 = tk.Label(self, text="Database statistics")
        Label2.grid(row=4, column=0)
        button5 = ttk.Button(self, text='Database path', command=self.databasepath)
        button5.grid(row=4, column=1, sticky=tk.EW)        
        self.path3 = tk.StringVar(self)
        self.path3.set('')
        Entry3 = tk.Entry(self, text=self.path3)
        Entry3.grid(row=4, column=2, columnspan=2, sticky=tk.EW)
        button2 = tk.Button(self, text='Check out', command=self.checkout)
        button2.grid(row=4, column=4, sticky=tk.EW)
        Label3 = tk.Label(self, text="Number of porjects")
        Label3.grid(row=5, column=0)    
        self.num = tk.StringVar(self)
        self.num.set('')
        Entry4 = tk.Entry(self, text=self.num)
        Entry4.grid(row=5, column=1, columnspan=3, sticky=tk.EW)
        button6 = tk.Button(self, text='Export', command=self.export)
        button6.grid(row=5, column=4, sticky=tk.EW)        

    def check_process(self):
        """ Check every 1000 ms whether the process is finished """
        if self.process.finished:
            messagebox.showinfo('Info', 'Completed')
        else:
            self.after(1, self.check_process)  
            
    def Update(self):
        if self.var1.get() == 1:
            try:
                datafolder = self.path1.get()
                outputpath = self.path2.get()
                files = []
                for file in os.listdir(datafolder):
                    if file.endswith(".xlsx"):
                        files.append(file)       
                load.savedata(outputpath, load.import_data(datafolder, files))
                self.process.run()
                self.check_process()
            except:
                messagebox.showerror('Error', 'Unexpected error!')
        elif self.var2.get() == 1:
            pass
        else:
            messagebox.showerror('Error', 'Please select database type!')
    
    def folderpath(self):
        datafolder = askdirectory()
        self.path1.set(datafolder)
        
    def savepath(self):
        outputpath = asksaveasfilename(defaultextension='.json', 
                                       filetypes=[("json files", '*.json')],
                                       title="Choose file")
        self.path2.set(outputpath)

    def databasepath(self):
        datapath = askopenfilename(title = "Select database", filetypes = [('All Files', '*.json')])
        self.path3.set(datapath)
        
    def checkout(self):
        try:
            filepath = self.path3.get()
            with open(filepath, 'r') as f:
                self.data = json.load(f)
                self.num.set(len(self.data))
        except:
            messagebox.showerror('Error', 'Please select database type!')
    
    def export(self):
        pass


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid()
        self.data = {}
        self.Parameter = []
        label = tk.Label(self, text="Library!", font=LARGE_FONT)
        label.grid()
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(row=21, column=0, sticky=tk.EW)
        button3 = ttk.Button(self, text="Import database", command=self.load_database)
        button3.grid(row=1, column=0, sticky=tk.EW)
        self.widget()
        self.Tree_config()
    
    def widget(self):
        self.option_variable1 = tk.StringVar(self)
        self.option_variable1.set('Select WindTurbine')
        self.Menu1 = tk.OptionMenu(self, self.option_variable1, 'None')
        self.Menu1.grid(ipady=10, row=3, column=0, sticky=tk.EW)
        self.option_variable2 = tk.StringVar(self)
        self.option_variable2.set('Select Catagory')
        self.Menu2 = tk.OptionMenu(self, self.option_variable2, 'None')
        self.Menu2.grid(ipady=10, row=4, column=0, sticky=tk.EW)
        self.option_variable3 = tk.StringVar(self)
        self.option_variable3.set('Select Parameter')
        self.Menu3 = tk.OptionMenu(self, self.option_variable3, 'None')
        self.Menu3.grid(ipady=10, row=5, column=0, sticky=tk.EW)
        self.pathvariable = tk.StringVar(self)
        self.pathvariable.set('')
        self.Entry1 = tk.Entry(self, text=self.pathvariable)
        self.Entry1.grid(row=1, column=1, sticky=tk.EW)
        Search = tk.Button(self, text="Search", command=self.search)
        Search.grid(row=6, column=0, sticky=tk.EW)
        self.Company_name = ['金风', '远景', '明阳', '中车', '三一', 'All']
        self.option_variable4 = tk.StringVar(self)
        self.option_variable4.set('Superfilter')
        self.Menu4 = tk.OptionMenu(self, self.option_variable4, *self.Company_name)
        self.Menu4.grid(row=2, sticky=tk.EW)        

    def Tree_config(self):
        self.TreeFrame = ttk.Frame(self, padding="3")
        self.TreeFrame.grid(row=2, column=1, rowspan=20, sticky=tk.NSEW)
        self.tree = ttk.Treeview(self.TreeFrame, columns=('Values'))
        self.tree.column('Values', width=100, anchor='center')
        self.tree.heading('Values', text='Values')
        self.tree.pack(fill=tk.BOTH, expand=1)
        
    def JSONTree(self, Tree, Parent, Dictionary):
        if isinstance(Dictionary, dict):
            for key in Dictionary:
                uid = uuid.uuid4()
                if isinstance(Dictionary[key], dict):
                    Tree.insert(Parent, 'end', uid, text=key)
                    self.JSONTree(Tree, uid, Dictionary[key])
                elif isinstance(Dictionary[key], list):
                    Tree.insert(Parent, 'end', uid, text=key + '[]')
                    self.JSONTree(Tree,
                              uid,
                              dict([(i, x) for i, x in enumerate(Dictionary[key])]))
                else:
                    value = Dictionary[key]
                    if isinstance(value, str):
                        value = value.replace(' ', '_')
                    Tree.insert(Parent, 'end', uid, text=key, value=value)
        else:
            uid = uuid.uuid4()
            Tree.insert(Parent, 'end', uid, value=Dictionary)
            
    def search(self):
        try:
            compname = self.option_variable4.get()
            proname = self.option_variable1.get()
            key1 = self.option_variable2.get()
            key2 = self.option_variable3.get()
            for row in self.tree.get_children():
                self.tree.delete(row)
            if key2 in list(itertools.chain.from_iterable(self.Parameter)):
                self.JSONTree(self.tree, '', self.data[proname][key1][key2])
            elif key1 in self.KeyList:
                self.JSONTree(self.tree, '', self.data[proname][key1])
            elif proname in self.Project:
                self.JSONTree(self.tree, '', self.data[proname])
            elif compname in self.Company_name and compname != 'All':
                newdata = {}
                for i in superfilter(self.data, compname):
                    newdata[i] = self.data[i]
                self.JSONTree(self.tree, '', newdata)
            else:
                self.JSONTree(self.tree, '', self.data)
        except:
            messagebox.showerror('Error', 'No data!!')
    
    def autoupdate_option1(self, *args):
        self.Menu3["menu"].delete(0, "end")
        for i in range(len(self.KeyList)):
            if self.option_variable2.get() == self.KeyList[i]:
                for item in self.Parameter[i]:
                    self.Menu3['menu'].add_command(label=item, 
                                                   command=tk._setit(self.option_variable3, item))            
        self.Menu3['menu'].add_command(label='None', 
                                       command=tk._setit(self.option_variable3, 'None'))

    def autoupdate_option2(self, *args):
        if self.option_variable4.get() != 'All':
            self.Menu1['menu'].delete(0, 'end')
            newlist = superfilter(self.data, self.option_variable4.get())
            for item in newlist:
                self.Menu1['menu'].add_command(label=item, 
                                               command=tk._setit(self.option_variable1, item))            
            self.Menu1['menu'].add_command(label='None', 
                                   command=tk._setit(self.option_variable1, 'None'))
        else:
            updatelist(self.option_variable1, self.Menu1, self.Project)    
        
    def load_database(self):
        filepath = askopenfilename(initialdir = "/", 
                                   title = "Select database", filetypes = [('All Files', '*.json')])
        try:
            self.pathvariable.set(filepath)
            with open(filepath, 'r') as f:
                self.data = json.load(f)
            self.Project = list(self.data.keys())
            self.KeyList = getKey(self.data)[0]
            self.Parameter = getKey(self.data)[1]          
            updatelist(self.option_variable1, self.Menu1, self.Project)
            updatelist(self.option_variable2, self.Menu2, self.KeyList)
            self.option_variable2.trace('w', self.autoupdate_option1)
            self.option_variable4.trace('w', self.autoupdate_option2)
        except:
            messagebox.showwarning(title='Warning', message='Please load database!')


class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid()
        self.data = {}
        self.Parameter = []
        self.widget()
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.grid(row=0) 
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(row=5, column=2)
        button2 = ttk.Button(self, text='Load database', command=self.load_database)
        button2.grid(row=1, column=0, sticky=tk.EW)
        f = Figure(figsize=(4,4), dpi=100)
        self.a = f.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.get_tk_widget().grid() 
        navigation_frame = tk.Frame(self)
        navigation_frame.grid(row=5, columnspan=2) 
        toolbar = NavigationToolbar2Tk(self.canvas, navigation_frame)
        toolbar.update()
        self.canvas._tkcanvas.grid(row=4, columnspan=2) 

    def widget(self):
        self.option_variable1 = tk.StringVar(self)
        self.option_variable1.set('Filter data to X axis')
        self.Menu1 = tk.OptionMenu(self, self.option_variable1, 'None')
        self.Menu1.grid(row=3, column=0, sticky=tk.EW) 
        self.option_variable2 = tk.StringVar(self)
        self.option_variable2.set('Filter data to Y axis')
        self.Menu2 = tk.OptionMenu(self, self.option_variable2, 'None')
        self.Menu2.grid(row=3, column=1, sticky=tk.EW)
        self.option_variable3 = tk.StringVar(self)
        self.option_variable3.set('Select catagory to X axis')
        self.Menu3 = tk.OptionMenu(self, self.option_variable3, 'None')
        self.Menu3.grid(row=2, column=0, sticky=tk.EW) 
        self.option_variable4 = tk.StringVar(self)
        self.option_variable4.set('Select catagory to Y axis')
        self.Menu4 = tk.OptionMenu(self, self.option_variable4, 'None')
        self.Menu4.grid(row=2, column=1, sticky=tk.EW)               
        self.pathvariable = tk.StringVar(self)
        self.pathvariable.set('')
        self.Entry1 = tk.Entry(self, text=self.pathvariable)
        self.Entry1.grid(row=1, column=1, sticky=tk.EW)
        self.button3 = tk.Button(self, text='Plot', command=self.plot)
        self.button3.grid(row=2, column=2, sticky=tk.EW)
        self.button4 = tk.Button(self, text='Clear', command=self.clearplot)
        self.button4.grid(row=3, column=2, sticky=tk.EW)
        self.lookup_name = tk.StringVar(self)
        self.lookup_name.set('')
        self.Entry2 = tk.Entry(self, text=self.lookup_name)
        self.Entry2.grid(row=1, column=2)

    def autoupdate_option1(self, *args):
        self.Menu1["menu"].delete(0, "end")
        for i in range(len(self.KeyList)):
            if self.option_variable3.get() == self.KeyList[i]:
                for item in self.Parameter[i]:
                    self.Menu1['menu'].add_command(label=item, 
                                                   command=tk._setit(self.option_variable1, item))            

    def autoupdate_option2(self, *args):
        self.Menu2["menu"].delete(0, "end")
        for i in range(len(self.KeyList)):
            if self.option_variable4.get() == self.KeyList[i]:
                for item in self.Parameter[i]:
                    self.Menu2['menu'].add_command(label=item, 
                                                   command=tk._setit(self.option_variable2, item))        
    
    def clearplot(self):
        self.a.clear()
        self.canvas.draw()
    
    def load_database(self):
        filepath = askopenfilename(initialdir = "/", 
                                   title = "Select database", filetypes = [('All Files', '*.json')])
        try:
            self.pathvariable.set(filepath)
            with open(filepath, 'r') as f:
                self.data = json.load(f)
            self.KeyList = getKey(self.data)[0]
            self.Parameter = getKey(self.data)[1]
            updatelist(self.option_variable3, self.Menu3, self.KeyList)
            updatelist(self.option_variable4, self.Menu4, self.KeyList)
            self.option_variable3.trace('w', self.autoupdate_option1)
            self.option_variable4.trace('w', self.autoupdate_option2)            
        except:
            messagebox.showwarning(title='Warning', message='Please load database!')

    def onpick(self,event):
        thisline = event.artist
        xdata = thisline.get_xdata()
        ydata = thisline.get_ydata()
        ind = event.ind
        self.data1 = float(xdata[ind][0])
        self.data2 = float(ydata[ind][0])      
        self.lookup_name.set(find_key(self.data2, self.data))
        print('onpick points:', self.data2)
    
    def plot(self):
        try:
            key1 = self.option_variable3.get()
            key2 = self.option_variable4.get()
            key3 = self.option_variable1.get()
            key4 = self.option_variable2.get()
            xdata = [getfloat(i) for i in Dictfilter(self.data, key1, key3)] 
            ydata = [getfloat(i) for i in Dictfilter(self.data, key2, key4)]
            print(xdata)
            print(ydata)
            self.a.plot(xdata, ydata, 'o', picker=3, label=re.split('[(（]', key4)[0])
            self.canvas.mpl_connect('pick_event', self.onpick)
            self.a.ticklabel_format(axis="both", style="sci", scilimits=(0,0))
            self.a.legend(loc='upper left', borderaxespad=0.)
            self.canvas.draw()            
        except:
            messagebox.showerror(title='Error', message='Error!')    


LARGE_FONT= ('calibri', 15)


# def graph():
#     xList = [1, 2]
#     yList = [1, 2]
#     a.clear()
#     a.plot(xList, yList)


app = Application()
# ani = graph()
app.mainloop()
        