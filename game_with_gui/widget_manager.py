
import tkinter as tk

class Widgets():
    def __init__(self,root):
        self.rt=root
    
    def gui_player_name(self):
        
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
    ########################## gui_player_name() end ###############################
    
    
    def gui_disp_half_hands(self,players_lst,obj_half_deal_lst):
        
        self.players_lst=players_lst
        
        fr_0=tk.Frame(self.rt,background='DeepSkyBlue4')
        fr_0.pack(side=tk.BOTTOM,pady=10)

        fr_1=tk.Frame(self.rt,background='DeepSkyBlue4')
        fr_1.pack(side=tk.RIGHT,padx=10)

        fr_2=tk.Frame(self.rt,background='DeepSkyBlue4')
        fr_2.pack(side=tk.TOP,pady=10)

        fr_3=tk.Frame(self.rt,background='DeepSkyBlue4')
        fr_3.pack(side=tk.LEFT,padx=10)

        fr_lst=[fr_0,fr_1,fr_2,fr_3]

        button_lst_4_nme=[]
        for i in range(4):
            button_lst_4_nme.append(tk.Button(fr_lst[i],text=self.players_lst[i],\
                                              font=('GNU Unifont',15)))
            button_lst_4_nme[i].pack(side=tk.BOTTOM,pady=10)


        button_lst_4_crd=[[],[],[],[]]
        for j in range(4):
            for i in range(4):
                k=obj_half_deal_lst[j][i]
                button_lst_4_crd[j].append(tk.Button(fr_lst[j],text=k.form(),fg=k.colour(),\
                                                     font=('GNU Unifont',15)))
                button_lst_4_crd[j][i].pack(side=tk.LEFT)

        some_var=tk.IntVar()
        
        def clear_fr_cen():
            fr_center.pack_forget()
            some_var.set(1)
        
        fr_center=tk.Frame(self.rt,background='black')
        fr_center.pack()
        but_cen=tk.Button(fr_center,text='Start bidding',command=clear_fr_cen)
        but_cen.pack(side=tk.TOP,pady=300)
        
        fr_center.wait_variable(some_var)
        
    ############### gui_disp_half_hands() end ######################################
    
    def gui_half_bid_mes(self,first_bidder):
        
        some_var2=tk.IntVar()
        
        def var2():
            some_var2.set(1)
        
        def set_bid_labels():
            lab_mes.pack_forget()
            but_mes.pack_forget()
            
            self.lab_self_call=tk.Label(self.fr_hlf_bd_center,text='Waiting bid turn',font=('GNU Unifont',15))
            self.lab_right_call=tk.Label(self.fr_hlf_bd_center,text='Waiting bid turn',font=('GNU Unifont',15))
            self.lab_mate_call=tk.Label(self.fr_hlf_bd_center,text='Waiting bid turn',font=('GNU Unifont',15))
            self.lab_left_call=tk.Label(self.fr_hlf_bd_center,text='Waiting bid turn',font=('GNU Unifont',15))
            self.lab_call_lst=[self.lab_self_call,self.lab_right_call,\
                               self.lab_mate_call,self.lab_left_call]

            self.but_next=tk.Button(self.fr_hlf_bd_center,text='>>',font=('GNU Unifont',15),command=var2)
            
            self.lab_self_call.grid(row=4,column=1,columnspan=2,pady=5,sticky='')
            self.lab_right_call.grid(row=2,column=3,padx=5,sticky='')
            self.lab_mate_call.grid(row=0,column=1,columnspan=2,pady=5,sticky='')
            self.lab_left_call.grid(row=2,column=0,padx=5,sticky='')
            self.but_next.grid(row=2,column=1,columnspan=2,sticky='')
            
            
        
        self.fr_hlf_bd_center=tk.Frame(self.rt,background='black')
        self.fr_hlf_bd_center.pack(side=tk.TOP,pady=250)
        lab_mes=tk.Label(self.fr_hlf_bd_center,text='Bidding starts with '+first_bidder,\
                        font=('GNU Unifont',15))
        lab_mes.pack()
        but_mes=tk.Button(self.fr_hlf_bd_center,text='>>',command=set_bid_labels)
        but_mes.pack(pady=10)
        
        self.fr_hlf_bd_center.wait_variable(some_var2)
        
    ############## gui_half_bid_mes() end ##########################################
    
    def gui_half_bid_entry(self):
                
        half_bid_var=tk.StringVar()
        some_var3=tk.IntVar()
        
        self.lab_self_call.grid_forget()
        
        def save_hlf_bd_val():
            global half_bid_val
            half_bid_val=half_bid_var.get()
            lab_hlf_bd_val.grid_forget()
            ent_hlf_bd_val.grid_forget()
            but_hlf_bd_val.grid_forget()

            some_var3.set(1)
        
        lab_hlf_bd_val=tk.Label(self.fr_hlf_bd_center,text='Enter bid value',font=('GNU Unifont',15))
        ent_hlf_bd_val=tk.Entry(self.fr_hlf_bd_center,textvariable=half_bid_var,font=('GNU Unifont',15))
        but_hlf_bd_val=tk.Button(self.fr_hlf_bd_center,text='Enter', font=('GNU Unifont',15),\
                                 command=save_hlf_bd_val)

        lab_hlf_bd_val.grid(row=4,column=1,sticky='')
        ent_hlf_bd_val.grid(row=4,column=2,sticky='')
        but_hlf_bd_val.grid(row=5,column=2,sticky='')
        
        self.fr_hlf_bd_center.wait_variable(some_var3)
        
        return(half_bid_val)
        
    ############## gui_half_bid_entry() end ########################################
    
    def gui_half_bid_values(self,bidder_indx,bid_val,calls):
        
        self.lab_self_call.grid(row=4,column=1,columnspan=2,pady=5,sticky='')
        
        some_var4=tk.IntVar()
        
        def nxt():
            some_var4.set(1)
    
        if calls:
            self.lab_call_lst[bidder_indx].configure(text=self.players_lst[bidder_indx]+' calls '+str(bid_val))

        elif bid_val==10:
            self.lab_call_lst[bidder_indx].configure(text=self.players_lst[bidder_indx]+' passes ')

        else:
            some_var4.set(1)
            
        self.but_next.configure(command=nxt)
        
        self.fr_hlf_bd_center.wait_variable(some_var4)
        
    ############## gui_half_bid_values() end #######################################
    
    def gui_half_bid_trump(self):
        pass
    ############## gui_half_bid_trump() end ########################################
    
    def gui_half_bid_declare(self):
        pass
    ############## gui_half_bid_declare() end ######################################
