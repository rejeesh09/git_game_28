
import tkinter as tk

class Widgets():
    def __init__(self,root):
        self.rt=root
    
    def name_entered(self):
        
        fr1=tk.Frame(self.rt)
        fr1.pack(side=tk.TOP, pady=300)

        name_var=tk.StringVar()
        self.name=name_var.get()
        wait_var=tk.IntVar()
        
        def clear_fr1():
            fr1.pack_forget()
            wait_var.set(1)

        def save_name():
            global name, lab2, but2
            name=name_var.get()
            
            lab1.grid_forget()
            ent1.grid_forget()
            but1.grid_forget()
            
            lab2=tk.Label(fr1,text='Name entered is: '+name,font=('GNU Unifont',30))
            but2=tk.Button(fr1, text='Deal',font=('GNU Unifont',30),command=clear_fr1)
            lab2.pack()
            but2.pack()
        
        lab1=tk.Label(fr1,text='Name:',font=('GNU Unifont',20))
        ent1=tk.Entry(fr1,textvariable=name_var,font=('GNU Unifont',20))
        but1=tk.Button(fr1,text='Enter', font=('GNU Unifont',20),command=save_name)

        lab1.grid(row=0,column=0,sticky='')
        ent1.grid(row=0,column=1,sticky='')
        but1.grid(row=1,column=1,sticky='')
        
        fr1.wait_variable(wait_var)
        
        return(name)
