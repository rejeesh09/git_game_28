
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
        
        fr1.columnconfigure((0,1),weight=1)
        fr1.rowconfigure((0,1),weight=1)
        
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
            
            but2.focus()
        
        lab1=tk.Label(fr1,text='Name:',font=('GNU Unifont',20))
        ent1=tk.Entry(fr1,textvariable=name_var,font=('GNU Unifont',20))
        but1=tk.Button(fr1,text='Enter', font=('GNU Unifont',20),command=save_name)
        
        ent1.focus()

        lab1.grid(row=0,column=0,sticky='')
        ent1.grid(row=0,column=1,sticky='')
        but1.grid(row=1,column=1,sticky='')
        
        fr1.wait_variable(wait_var)
        
        return(name)
    ########################## gui_player_name() end ################################
    
    
    def gui_disp_half_hands(self,players_lst,obj_half_deal_lst):
    # called from obj_display_half_hands() in Deck()-through __init__ of Round_1() via __init__ of
    # Prepare_game()
        
        self.rt.columnconfigure((0,1,2),weight=1)
        self.rt.rowconfigure((0,1,2),weight=1)
        
        self.players_lst=players_lst
        
        self.fr_0=tk.Frame(self.rt,background='DeepSkyBlue4')
        self.fr_0.grid(column=1,row=2,sticky=tk.S,pady=40)

        self.fr_1=tk.Frame(self.rt,background='DeepSkyBlue4')
        self.fr_1.grid(column=2,row=1,sticky=tk.E,padx=40)

        self.fr_2=tk.Frame(self.rt,background='DeepSkyBlue4')
        self.fr_2.grid(column=1,row=0,sticky=tk.N,pady=40)

        self.fr_3=tk.Frame(self.rt,background='DeepSkyBlue4')
        self.fr_3.grid(column=0,row=1,sticky=tk.W,padx=40)

        self.fr_lst=[self.fr_0,self.fr_1,self.fr_2,self.fr_3]

        button_lst_4_nme=[]
        for i in range(4):
            button_lst_4_nme.append(tk.Button(self.fr_lst[i],text=self.players_lst[i],\
                                              font=('GNU Unifont',15)))
            button_lst_4_nme[i].pack(side=tk.BOTTOM,pady=10)


        self.button_lst_4_crd=[[],[],[],[]]
        for j in range(4):
            for i in range(4):
                k=obj_half_deal_lst[j][i]
                self.button_lst_4_crd[j].append(tk.Button(self.fr_lst[j],text=k.form(),fg=k.colour(),\
                                                     font=('GNU Unifont',15)))
                self.button_lst_4_crd[j][i].pack(side=tk.LEFT)

        some_var=tk.IntVar()
        
        def clear_fr_cen():
            fr_center.grid_forget()
            some_var.set(1)
        
        fr_center=tk.Frame(self.rt,background='black')
        fr_center.grid(column=1,row=1)
    
        but_cen=tk.Button(fr_center,text='Start bidding',font=('GNU Unifont',15),command=clear_fr_cen)
        but_cen.pack(side=tk.TOP,pady=10)
        but_cen.focus()
        
        fr_center.wait_variable(some_var)
        
    ############### gui_disp_half_hands() end #######################################
    
    def gui_half_bid_mes(self,first_bidder):
        
        some_var2=tk.IntVar()
        
#         def var2():
#             some_var2.set(1)
        
        def set_bid_labels():
            lab_mes.grid_forget()
            but_mes.grid_forget()
            
            # the below labels and button are only getting created and not packed here
            self.lab_self_call=tk.Label(self.fr_hlf_bd_center,text='Waiting bid turn',font=('GNU Unifont',15))
            self.lab_right_call=tk.Label(self.fr_hlf_bd_center,text='Waiting bid turn',font=('GNU Unifont',15))
            self.lab_mate_call=tk.Label(self.fr_hlf_bd_center,text='Waiting bid turn',font=('GNU Unifont',15))
            self.lab_left_call=tk.Label(self.fr_hlf_bd_center,text='Waiting bid turn',font=('GNU Unifont',15))
            self.lab_call_lst=[self.lab_self_call,self.lab_right_call,\
                               self.lab_mate_call,self.lab_left_call]

            self.but_next=tk.Button(self.fr_hlf_bd_center,text='>>',font=('GNU Unifont',15))
            self.but_next.focus()
            some_var2.set(1)
            
                   
        self.fr_hlf_bd_center=tk.Frame(self.rt,background='black')
        # this frame is positioned at the center cell of the self.rt window
        self.fr_hlf_bd_center.grid(column=1,row=1,sticky='NSEW')
        
        # this frame is further configured into 3 rows and 3 columns
        self.fr_hlf_bd_center.columnconfigure((0,1,2),weight=1)
        self.fr_hlf_bd_center.rowconfigure((0,1,2),weight=1)
        
        lab_mes=tk.Label(self.fr_hlf_bd_center,text='Bidding starts with '+first_bidder,\
                        font=('GNU Unifont',15))
#         lab_mes.pack()
        lab_mes.grid(column=1,row=0,sticky='')
        but_mes=tk.Button(self.fr_hlf_bd_center,text='>>',font=('GNU Unifont',15),command=set_bid_labels)
#         but_mes.pack(pady=10)
        but_mes.grid(column=1,row=1,sticky='')
        but_mes.focus()
        
        self.fr_hlf_bd_center.wait_variable(some_var2)
        
    ############## gui_half_bid_mes() end ###########################################
    
    def gui_half_bid_entry(self):
                
        half_bid_var=tk.StringVar()
        some_var3=tk.IntVar()
        
#         self.lab_self_call.grid(row=4,column=1,columnspan=2,pady=5,sticky='')
#         self.lab_right_call.grid(row=2,column=3,padx=5,sticky='')
#         self.lab_mate_call.grid(row=0,column=1,columnspan=2,pady=5,sticky='')
#         self.lab_left_call.grid(row=2,column=0,padx=5,sticky='')

        # these are now getting packed('grided') in the 'self.fr_hlf_bd_center' frame
        self.lab_self_call.grid(row=2,column=1,sticky='')
        self.lab_right_call.grid(row=1,column=2,sticky='')
        self.lab_mate_call.grid(row=0,column=1,sticky='')
        self.lab_left_call.grid(row=1,column=0,sticky='')
            
        
        def save_hlf_bd_val():
            global half_bid_val
            half_bid_val=half_bid_var.get()
            self.fr_hlf_bd_center_bot.grid_forget()
#             lab_hlf_bd_val.grid_forget()
#             ent_hlf_bd_val.grid_forget()
#             but_hlf_bd_val.grid_forget()
#             self.lab_self_call.grid(row=4,column=1,columnspan=2,pady=5,sticky='')
            self.lab_self_call.grid(row=2,column=1,sticky='')

            some_var3.set(1)
        
        self.lab_self_call.grid_forget()
        
        # creating a separate frame for player bid value entry
        self.fr_hlf_bd_center_bot=tk.Frame(self.fr_hlf_bd_center,bg='black')
        self.fr_hlf_bd_center_bot.columnconfigure((0,1),weight=1)
        self.fr_hlf_bd_center_bot.rowconfigure((0,1),weight=1)
        self.fr_hlf_bd_center_bot.grid(column=1,row=2,sticky='NSEW')
        
        lab_hlf_bd_val=tk.Label(self.fr_hlf_bd_center_bot,text='Enter bid value',font=('GNU Unifont',15))
        ent_hlf_bd_val=tk.Entry(self.fr_hlf_bd_center_bot,textvariable=half_bid_var,font=('GNU Unifont',15))
        but_hlf_bd_val=tk.Button(self.fr_hlf_bd_center_bot,text='Enter', font=('GNU Unifont',15),\
                                 command=save_hlf_bd_val)

#         lab_hlf_bd_val.grid(row=5,column=1,sticky='')
#         ent_hlf_bd_val.grid(row=5,column=2,sticky='')
#         but_hlf_bd_val.grid(row=6,column=2,sticky='')
        
        lab_hlf_bd_val.grid(row=0,column=0,sticky='')
        ent_hlf_bd_val.grid(row=0,column=1,sticky='')
        but_hlf_bd_val.grid(row=1,column=1,sticky='')
        
        ent_hlf_bd_val.focus()
        
        self.fr_hlf_bd_center.wait_variable(some_var3)
        
        return(half_bid_val)
        
    ############## gui_half_bid_entry() end #########################################
    
    def gui_half_bid_values(self,bidder_indx,bid_val,calls):

        
        some_var4=tk.IntVar()
        
        def nxt():
            some_var4.set(1)
    
        if calls:
            self.lab_call_lst[bidder_indx].configure(text=self.players_lst[bidder_indx]+' calls '+str(bid_val))

        else:
            self.lab_call_lst[bidder_indx].configure(text=self.players_lst[bidder_indx]+' passes ')

            
        self.but_next.configure(command=nxt)
#         self.but_next.grid(row=2,column=1,columnspan=2,sticky='')
        self.but_next.grid(row=1,column=1,sticky='')
        self.but_next.focus()
        
#         self.lab_self_call.grid(row=4,column=1,columnspan=2,pady=5,sticky='')
#         self.lab_right_call.grid(row=2,column=3,padx=5,sticky='')
#         self.lab_mate_call.grid(row=0,column=1,columnspan=2,pady=5,sticky='')
#         self.lab_left_call.grid(row=2,column=0,padx=5,sticky='')
        
        self.lab_self_call.grid(row=2,column=1,sticky='')
        self.lab_right_call.grid(row=1,column=2,sticky='')
        self.lab_mate_call.grid(row=0,column=1,sticky='')
        self.lab_left_call.grid(row=1,column=0,sticky='')
        
        self.fr_hlf_bd_center.wait_variable(some_var4)
        
    ############## gui_half_bid_values() end ########################################
    
    def gui_half_bid_trump(self,bid_val):
    # this method is called when player is the highest bidder in half bid and has to set trump
        
        self.lab_self_call.grid_forget()
        self.lab_right_call.grid_forget()
        self.lab_mate_call.grid_forget()
        self.lab_left_call.grid_forget()
        
        some_var6=tk.IntVar()
        trump_var=tk.StringVar()
        
        def declare():
            
            self.lab_hlf_bd_mes_fnl.configure(text='Trump card set by '+self.players_lst[0])
            self.but_next.configure(text='Deal full hand')
            self.but_next.configure(command= lambda: some_var6.set(1))
            self.but_next.focus()
        
        def save_trump():
            global hlf_bd_trump
            hlf_bd_trump=trump_var.get()
            
            self.fr_hlf_bd_center_bot.grid_forget()
            
#             self.lab_hlf_bd_trmp.grid_forget()
#             self.ent_hlf_bd_trmp.grid_forget()
#             self.but_hlf_bd_trmp.grid_forget()
            
            self.but_next.configure(command=declare)
            self.but_next.focus()
            
        
        def take_trump():
            self.lab_hlf_bd_trmp=tk.Label(self.fr_hlf_bd_center_bot,text='Enter trump card',font=('GNU Unifont',15))
            self.ent_hlf_bd_trmp=tk.Entry(self.fr_hlf_bd_center_bot,textvariable=trump_var,font=('GNU Unifont',15))
            self.but_hlf_bd_trmp=tk.Button(self.fr_hlf_bd_center_bot,text='Enter', font=('GNU Unifont',15),\
                                     command=save_trump)

#             self.lab_hlf_bd_trmp.grid(row=2,column=1,sticky='')
#             self.ent_hlf_bd_trmp.grid(row=2,column=2,sticky='')
#             self.but_hlf_bd_trmp.grid(row=3,column=2,sticky='')

            self.fr_hlf_bd_center_bot.grid(column=1,row=2,sticky='NSEW')
            
            self.lab_hlf_bd_trmp.grid(row=0,column=0,sticky='')
            self.ent_hlf_bd_trmp.grid(row=0,column=1,sticky='')
            self.but_hlf_bd_trmp.grid(row=1,column=1,sticky='')
            
            self.ent_hlf_bd_trmp.focus()
        
        self.lab_hlf_bd_mes_fnl=tk.Label(self.fr_hlf_bd_center,\
                    text=self.players_lst[0]+' made the highest bid '+str(bid_val),font=('GNU Unifont',15))
#         lab_hlf_bd_mes_fnl.grid(row=0,column=1,columnspan=2,pady=5,sticky='')
        self.lab_hlf_bd_mes_fnl.grid(row=0,column=1,sticky='')
        self.but_next.configure(command=take_trump)
        self.but_next.focus()
        
        
        self.fr_hlf_bd_center.wait_variable(some_var6)        
        return(hlf_bd_trump)
        
    ############## gui_half_bid_trump() end #########################################
    
    def gui_half_bid_declare(self,bidder_indx,bid_val):
    # this method is called when player is not the highest bidder
        
        self.lab_self_call.grid_forget()
        self.lab_right_call.grid_forget()
        self.lab_mate_call.grid_forget()
        self.lab_left_call.grid_forget()
        
        some_var5=tk.IntVar()
        
        def disp_val():
            self.lab_hlf_bd_mes_fnl.configure(text='Trump card set by '+self.players_lst[bidder_indx])
            self.but_next.configure(text='Deal full hand')
            self.but_next.configure(command= lambda: some_var5.set(1))
            self.but_next.focus()
        
        self.lab_hlf_bd_mes_fnl=tk.Label(self.fr_hlf_bd_center,\
                            text=self.players_lst[bidder_indx]+' made the highest bid '+str(bid_val),\
                                   font=('GNU Unifont',15))
#         lab_hlf_bd_mes_fnl.grid(row=0,column=1,columnspan=2,pady=5,sticky='')
        self.lab_hlf_bd_mes_fnl.grid(row=0,column=1,sticky='')
        
        self.but_next.configure(command=disp_val)
        self.but_next.focus()
        
        self.fr_hlf_bd_center.wait_variable(some_var5)
        
    ############## gui_half_bid_declare() end #######################################
    
    def gui_disp_full_hands(self,highest_bidder_indx,trump_revealed,trump_card,obj_deal_lst_copy,situation):
    # called through obj_display_hands() in Deck(), which is called at the end of bid_half_hand()-
    # (situation==0) and also at the end of bid_full_hand()-(situation==1) in Prepare_game(s) 
    
        
        some_var13=tk.IntVar()
        
        if situation==0:
        # situation==0 corresponds to display before full bid, ==1 for aft full bid, 
        # maybe 2 for aft 1st round etc.
            
            # forgetting the center frame and all card buttons in the other 4 frames in root-window
            self.fr_hlf_bd_center.grid_forget()
            for j in range(4):
                for i in range(4):
                    self.button_lst_4_crd[j][i].pack_forget()
                self.button_lst_4_crd[j].clear()

            # creating new card buttons
            for j in range(4):
                for k in obj_deal_lst_copy[j]:
                # trump_card will not be available in obj_deal_lst_copy(except in player hand if player 
                # himself was highest bidder)
                    l=tk.Button(self.fr_lst[j],text=k.form(),fg=k.colour(),font=('GNU Unifont',15))
                    self.button_lst_4_crd[j].append(l)
                    l.pack(side=tk.LEFT)

            # the trump card set in first bid will not be available in obj_deal_copy(for the comp hands), 
            # and the button for that wouldn't be created. But if player was the highest bidder, the 
            # button corresponding to trump card is being removed here.
            if (not highest_bidder_indx):
                for i in self.button_lst_4_crd[0]:
                    if i['text']==trump_card.form():
                        # removing the card from list, in addition to pack_forget
                        i.pack_forget()
                        self.button_lst_4_crd[0].remove(i)
            
            # adding an extra button to represent trump card
            self.but_trump_card=tk.Button(self.fr_lst[highest_bidder_indx],\
                                              bg='red',text='T',font=('GNU Unifont',15))

            # there is no need to actually check this condition, since this method itself is being 
            # called for now in only two situations, both of which occur before round1 starts
            if (not trump_revealed):           
                self.but_trump_card.pack(side=tk.RIGHT,padx=10)
            else:
                self.but_trump_card.pack_forget()


            some_var7=tk.IntVar()

#             def fll_bd_nxt1():
#                 some_var7.set(1)

            self.fr_fll_bd_center=tk.Frame(self.rt,background='black')
            self.fr_fll_bd_center.grid(column=1,row=1,sticky='NSEW')
            
            self.fr_fll_bd_center.columnconfigure((0,1,2),weight=1)
            self.fr_fll_bd_center.rowconfigure((0,1,2),weight=1)
            
            self.but_fll_nxt=tk.Button(self.fr_fll_bd_center,text='Start 2nd bidding',font=('GNU Unifont',15),\
                                       command=lambda:some_var7.set(1))
            self.but_fll_nxt.grid(row=1,column=1,sticky='')
            self.but_fll_nxt.focus()

            self.fr_fll_bd_center.wait_variable(some_var7)
            
        elif situation==1:
        # i.e. the full hand display method is being called after bidding is over and round1 to start
            
            for j in range(4):
                for i in self.button_lst_4_crd[j]:
                    i.pack_forget()
                self.button_lst_4_crd[j].clear()

            for j in range(4):
                for k in obj_deal_lst_copy[j]:
                    l=tk.Button(self.fr_lst[j],text=k.form(),fg=k.colour(),font=('GNU Unifont',15))
                    self.button_lst_4_crd[j].append(l)
                    l.pack(side=tk.LEFT)
                    
            # the trump card set in 2nd bid also will not be available in obj_deal_copy(for the comp hands), 
            # and the button for that wouldn't be created. But if player was the highest bidder, the 
            # button corresponding to trump card is being removed here.
            if (not highest_bidder_indx):
                for i in self.button_lst_4_crd[0]:
                    if i['text']==trump_card.form():
                        i.pack_forget()
                        self.button_lst_4_crd[0].remove(i)
            
            # since the disply hand is now being called after 2nd bidding, the trump_card button may 
            # have to change frame if the highest bidder is different, so creating a new button for it.
            self.but_trump_card.pack_forget()
            self.but_trump_card2=tk.Button(self.fr_lst[highest_bidder_indx],\
                                              bg='red',text='T',font=('GNU Unifont',15))
            
            # there is no need to actually check this condition, since this method itself is being 
            # called for now in only two situations, both of which occur before round1 starts
            if (not trump_revealed):           
                self.but_trump_card2.pack(side=tk.RIGHT,padx=10)
            else:
                self.but_trump_card2.pack_forget()
                
            
            def clear_fll_bd_fr2():
                self.fr_fll_bd_center.grid_forget()
                
                self.fr_game_center=tk.Frame(self.rt, background='black')
#                 self.fr_game_center.pack(side=tk.TOP,pady=250)
                self.fr_game_center.grid(column=1,row=1,sticky='NSEW')
    
                self.fr_game_center.columnconfigure((0,1,2),weight=1)
                self.fr_game_center.rowconfigure((0,1,2),weight=1)

                self.but_game_nxt=tk.Button(self.fr_game_center,text='Round1',font=('GNU Unifont',15))
                self.but_game_nxt.grid(row=1,column=1,sticky='')
                
                some_var13.set(1)
            
            self.but_fll_nxt.configure(text='Start game')
            self.but_fll_nxt.configure(command= clear_fll_bd_fr2)
            self.but_fll_nxt.focus()
            
            self.fr_fll_bd_center.wait_variable(some_var13)
        
    ############### gui_disp_full_hands() end #######################################
    
    def gui_full_bid_mes(self,first_bidder):
    # called from bid_full_hand in Prepare_game()
        
        some_var8=tk.IntVar()
        
        def fll_bd_labels():
            lab_fll_bd_mes.grid_forget()
            
            self.lab_self_fcall=tk.Label(self.fr_fll_bd_center,text='Waiting bid turn',font=('GNU Unifont',15))
            self.lab_right_fcall=tk.Label(self.fr_fll_bd_center,text='Waiting bid turn',font=('GNU Unifont',15))
            self.lab_mate_fcall=tk.Label(self.fr_fll_bd_center,text='Waiting bid turn',font=('GNU Unifont',15))
            self.lab_left_fcall=tk.Label(self.fr_fll_bd_center,text='Waiting bid turn',font=('GNU Unifont',15))
            self.lab_fcall_lst=[self.lab_self_fcall,self.lab_right_fcall,\
                               self.lab_mate_fcall,self.lab_left_fcall]
            
            some_var8.set(1)
                   

        lab_fll_bd_mes=tk.Label(self.fr_fll_bd_center,text='2nd round bidding starts with '+first_bidder,\
                        font=('GNU Unifont',15))
        lab_fll_bd_mes.grid(row=0,column=1,sticky='')
        self.but_fll_nxt.configure(text='>>',command=fll_bd_labels)
        self.but_fll_nxt.focus()
        
        self.fr_fll_bd_center.wait_variable(some_var8)
        
    ############### gui_full_bid_mes() end ##########################################  
    
    def gui_full_bid_entry(self):
    # called from bid_full_hand() in Prepare_game()
                
        full_bid_var=tk.StringVar()
        some_var9=tk.IntVar()
        
        self.but_fll_nxt.grid_forget()
        
        self.lab_self_fcall.grid(row=2,column=1,sticky='')
        self.lab_right_fcall.grid(row=1,column=2,sticky='')
        self.lab_mate_fcall.grid(row=0,column=1,sticky='')
        self.lab_left_fcall.grid(row=1,column=0,sticky='')
            
        
        def save_full_bd_val():
            global full_bid_val
            full_bid_val=full_bid_var.get()
            
            self.fr_fll_bd_center_bot.grid_forget()
#             lab_full_bd_val.grid_forget()
#             ent_full_bd_val.grid_forget()
#             but_full_bd_val.grid_forget()
            
            some_var9.set(1)
            
        
        self.lab_self_fcall.grid_forget()
        
        # creating a frame in the bottom cell (col=1,rw=2) of the fll_bd_center frame
        # to take full bid entry from player
        self.fr_fll_bd_center_bot=tk.Frame(self.fr_fll_bd_center,bg='black')
        self.fr_fll_bd_center_bot.grid(column=1,row=2,sticky='NSEW')
        
        self.fr_fll_bd_center_bot.columnconfigure((0,1),weight=1)
        self.fr_fll_bd_center_bot.rowconfigure((0,1),weight=1)
        
        lab_full_bd_val=tk.Label(self.fr_fll_bd_center_bot,text='Enter bid value',font=('GNU Unifont',15))
        ent_full_bd_val=tk.Entry(self.fr_fll_bd_center_bot,textvariable=full_bid_var,font=('GNU Unifont',15))
        but_full_bd_val=tk.Button(self.fr_fll_bd_center_bot,text='Enter', font=('GNU Unifont',15),\
                                 command=save_full_bd_val)

        lab_full_bd_val.grid(row=0,column=0,sticky='')
        ent_full_bd_val.grid(row=0,column=1,sticky='')
        but_full_bd_val.grid(row=1,column=1,sticky='')
        
        ent_full_bd_val.focus()
        
        self.fr_fll_bd_center.wait_variable(some_var9)
        
        return(full_bid_val)
    
    ############### gui_full_bid_entry() end ########################################
    
    def gui_full_bid_values(self,bidder_indx,bid_val,calls):
    # called from bid_full_hand() in Prepare_game()

        
        some_var10=tk.IntVar()
        
        def fll_nxt2():
            some_var10.set(1)
    
        if calls:
            self.lab_fcall_lst[bidder_indx].configure(text=self.players_lst[bidder_indx]+' calls '+str(bid_val))

        else:
            self.lab_fcall_lst[bidder_indx].configure(text=self.players_lst[bidder_indx]+' passes ')

            
        self.but_fll_nxt.configure(command=fll_nxt2)
        self.but_fll_nxt.grid(row=1,column=1,sticky='')
        self.but_fll_nxt.focus()
        
        self.lab_self_fcall.grid(row=2,column=1,sticky='')
        self.lab_right_fcall.grid(row=1,column=2,sticky='')
#         self.lab_mate_fcall.grid(row=0,column=1,columnspan=2,pady=5,sticky='')
        self.lab_mate_fcall.grid(row=0,column=1,sticky='')
        self.lab_left_fcall.grid(row=1,column=0,sticky='')
        
        self.lab_full_bd_mes_fnl=tk.Label(self.fr_fll_bd_center,text='',font=('GNU Unifont',15))
        
        self.fr_fll_bd_center.wait_variable(some_var10)
        
    ############## gui_full_bid_values() end ########################################
    
    def gui_full_bid_trump(self,bid_val):
    # called from bid_full_hand() in Prepare_game()
        
        self.lab_self_fcall.grid_forget()
        self.lab_right_fcall.grid_forget()
        self.lab_mate_fcall.grid_forget()
        self.lab_left_fcall.grid_forget()
        
        some_var11=tk.IntVar()
        trump_var=tk.StringVar()
        
        def declare_f():
            
            self.lab_full_bd_mes_fnl.configure(text='Trump card set by '+self.players_lst[0])
            self.but_fll_nxt.configure(text='>>')
            self.but_fll_nxt.configure(command= lambda: some_var11.set(1))
            self.but_fll_nxt.focus()
        
        def save_trump_f():
            global full_bd_trump
            full_bd_trump=trump_var.get()
            
            self.lab_full_bd_trmp.grid_forget()
            self.ent_full_bd_trmp.grid_forget()
            self.but_full_bd_trmp.grid_forget()
            self.fr_fll_bd_center_bot.grid_forget()
            
            self.but_fll_nxt.configure(command=declare_f)
            
        
        def take_trump_f():
            self.lab_full_bd_trmp=tk.Label(self.fr_fll_bd_center_bot,text='Enter trump card',font=('GNU Unifont',15))
            self.ent_full_bd_trmp=tk.Entry(self.fr_fll_bd_center_bot,textvariable=trump_var,font=('GNU Unifont',15))
            self.but_full_bd_trmp=tk.Button(self.fr_fll_bd_center_bot,text='Enter', font=('GNU Unifont',15),\
                                     command=save_trump_f)

            self.fr_fll_bd_center_bot.grid(column=1,row=2,sticky='NSEW')
            
            self.lab_full_bd_trmp.grid(row=0,column=0,sticky='')
            self.ent_full_bd_trmp.grid(row=0,column=1,sticky='')
            self.but_full_bd_trmp.grid(row=1,column=1,sticky='')            
            self.ent_full_bd_trmp.focus()
        
        self.lab_full_bd_mes_fnl.configure(text=self.players_lst[0]+' made the highest bid '+str(bid_val))
        self.lab_full_bd_mes_fnl.grid(row=0,column=1,sticky='')        
        self.but_fll_nxt.configure(command=take_trump_f)
        self.but_fll_nxt.focus()
        
        
        self.fr_fll_bd_center.wait_variable(some_var11)        
        return(full_bd_trump)
        
    ############## gui_full_bid_trump() end #########################################
    
    def gui_full_bid_declare(self,bidder_indx,bid_val,no_call):
    # called from bid_full_hand() in Prepare_game()
        
        self.lab_self_fcall.grid_forget()
        self.lab_right_fcall.grid_forget()
        self.lab_mate_fcall.grid_forget()
        self.lab_left_fcall.grid_forget()
        
        some_var12=tk.IntVar()
        
        self.fr_game_center=tk.Frame(self.rt, background='black')
        self.fr_game_center.columnconfigure((0,1,2),weight=1)
        self.fr_game_center.rowconfigure((0,1,2),weight=1)
        
        # an additional frame in the bottom middle cell of fr_game_center for player input
        self.fr_game_center_bot=tk.Frame(self.fr_game_center,background='black')
        self.fr_game_center_bot.columnconfigure((0,1),weight=1)
        self.fr_game_center_bot.rowconfigure((0,1),weight=1)
        
        def clear_fll_bd_fr():
            
            self.fr_fll_bd_center.grid_forget()
            
            self.fr_game_center.grid(column=1,row=1,sticky='NSEW')

        
            self.but_game_nxt=tk.Button(self.fr_game_center,text='Round1',font=('GNU Unifont',15))
            self.but_game_nxt.grid(column=1,row=1,sticky='')
            self.but_game_nxt.focus()
        
            self.but_game_nxt.configure(command= lambda: some_var12.set(1))
            
#             some_var12.set(1)
        
        def disp_val_f():
            self.lab_full_bd_mes_fnl.configure(text='Trump card set by '+self.players_lst[bidder_indx])
            self.but_fll_nxt.configure(text='>>')
#             self.but_fll_nxt.configure(command= lambda: some_var12.set(1))
            self.but_fll_nxt.configure(command= clear_fll_bd_fr)
            self.but_fll_nxt.focus()
        
        if not no_call:
            self.lab_full_bd_mes_fnl.configure(text=self.players_lst[bidder_indx]+\
                                            ' made the highest bid '+str(bid_val),font=('GNU Unifont',15))
            self.lab_full_bd_mes_fnl.grid(row=0,column=1,sticky='')

            self.but_fll_nxt.configure(command=disp_val_f)
            self.but_fll_nxt.focus()
        else:
            self.lab_full_bd_mes_fnl.configure(text='No one called 21, so trump set by '+\
                                               self.players_lst[bidder_indx]+' stays')
            self.lab_full_bd_mes_fnl.grid(row=0,column=1,sticky='')
            
            self.but_fll_nxt.configure(text='Start game')
            self.but_fll_nxt.configure(command= clear_fll_bd_fr)
            self.but_fll_nxt.focus()
            
        
        self.fr_game_center.wait_variable(some_var12)
        
    ############## gui_full_bid_declare() end #######################################
    
    def gui_card_played(self,turn_index,card_played):
    # called from round1_lead_logic() in Round_1()
    # trump_revealed status is to be checked and the trump_card button is to be dealt with
        
        some_var14=tk.IntVar() 
        
        def nxt_hnd():
            some_var14.set(1)
        
        for i in self.button_lst_4_crd[turn_index]:
            if i['text']==card_played.form():
                # this is where the played card is removed from the shown hand(button_lst_4_crd)
                i.pack_forget()
                
                # an new button for the played card is formed and packed('grided') according to the 
                # turn_index
                but_played_card=tk.Button(self.fr_game_center,text=card_played.form(),\
                                          fg=card_played.colour(),font=('GNU Unifont',15))                                         
                if turn_index==0:
                    but_played_card.grid(column=1,row=2,pady=20)
                elif turn_index==1:
                    but_played_card.grid(column=2,row=1,padx=20)
                elif turn_index==2:
                    but_played_card.grid(column=1,row=0,pady=20)
                elif turn_index==3:
                    but_played_card.grid(column=0,row=1,padx=20)
                else:
                    print('\nSomething wrong abt turn_index')
                    
        self.but_game_nxt.configure(text='>>',command=nxt_hnd)
        self.but_game_nxt.grid(column=1,row=1)
        self.but_game_nxt.focus()
        
        self.fr_game_center.wait_variable(some_var14)
        
    ############## gui_card_played() end ############################################
    
    def gui_round1_card_entry(self):
    # called from round1_lead_logic() in Round_1()
    # should be named card_select since it is now button based and not entry
        
        some_var15=tk.IntVar()
        round1_card=tk.StringVar()
        
#         def nxtt():
#             some_var15.set(1)
        
        def save_round1_card():
            global round1_entry
            round1_entry=round1_card.get()

            self.fr_game_center_bot.grid_forget()

            some_var15.set(1)
                    

        self.but_game_nxt.grid_forget()
        
        # this frame is created in full_bid_declare()
        self.fr_game_center_bot.grid(column=1,row=2,sticky='NSEW')

        
        # this is nw in a frame inside the cell at (2,1) of the fr_game_center
        self.lab_round1_card=tk.Label(self.fr_game_center_bot,text='Enter card',font=('GNU Unifont',15))
        self.ent_round1_card=tk.Entry(self.fr_game_center_bot,textvariable=round1_card,font=('GNU Unifont',15))
        self.lab_round1_card.grid(row=0,column=0,sticky='')
        self.ent_round1_card.grid(row=0,column=1,sticky='')
        self.ent_round1_card.focus()

        self.but_round1_card=tk.Button(self.fr_game_center_bot,text='Enter', font=('GNU Unifont',15),\
                                 command=save_round1_card)        
        self.but_round1_card.grid(row=1,column=1,sticky='')
                        
        
        self.fr_game_center.wait_variable(some_var15)
        
        return(round1_entry)
        
    ############## gui_round1_card_entry() end ######################################
    
    def gui_round1_trump_call_instance(self,turn_index):
    # called from round1_follow_logic() in Round_1()
    # this is to deal with the situation of trump call by player in round1
    # actually no need to pass the turn_index, since this method is called only for the turn_index==0 case
        
#         ret_val=0
        ret_var=tk.IntVar()
        
        def ret1():
            global ret_val
            ret_val=1
            ret_var.set(1)
            bt_plyr_trmp_choice1.grid_forget()
            bt_plyr_trmp_choice2.grid_forget()
            self.fr_game_center_bot.grid_forget()
            self.but_game_nxt.configure(text='Revealing trump')
            self.but_game_nxt.grid(column=1,row=1)
            
        def ret2():
            global ret_val
            ret_val=0
            ret_var.set(1)
            bt_plyr_trmp_choice1.grid_forget()
            bt_plyr_trmp_choice2.grid_forget()
            self.fr_game_center_bot.grid_forget()
            self.but_game_nxt.grid(column=1,row=1)
        
        if not turn_index:
        # no need for checking the turn_index, since the method is called only for turn_index==0
            self.but_game_nxt.grid_forget()
            # fr_game_center_bot is created in full_bid_declare() but not packed there. it is getting 
            # 'packed' in round1_card_entry() but getting packed again here as this method may get 
            # called before card_entry() is called
            self.fr_game_center_bot.grid(column=1,row=2,sticky='NSEW')
            
            bt_plyr_trmp_choice1=tk.Button(self.fr_game_center_bot,text='Calling trump'\
                                          ,font=('GNU Unifont',15),command=ret1)
            # fr_center_bot is defined in gui_round1_card_entry and it will always be called before this
            # method, since it is called in lead_logic()
            bt_plyr_trmp_choice2=tk.Button(self.fr_game_center_bot,text='Not calling trump'\
                                          ,font=('GNU Unifont',15),command=ret2)
            bt_plyr_trmp_choice1.grid(column=0,row=0)
            bt_plyr_trmp_choice2.grid(column=1,row=0)
            bt_plyr_trmp_choice1.focus()
            
            
        self.fr_game_center.wait_variable(ret_var)
        
        return(ret_val)
        
    ############## gui_round1_trump_call_instance() end #############################
    
    def gui_round1_trump_reveal(self,turn_index,trump_card):
    # called from round1_follow_logic() in Round_1()
    # this is to deal with the situ when trump is called (by comp hand) and revealed and the 
    # trump_card/trump_card2 button is to be revealed i.e. replaced with the form() of trump_card
        
        some_var16 = tk.IntVar()
        
        def trump_reveal():
            self.but_trump_card.configure(text=trump_card.form(),bg='white',fg=trump_card.colour())
            # adding the new card created to list for card buttons, so that when that card is 
            # played, it can be removed from the button list as well like other cards
            self.button_lst_4_crd[turn_index].append(self.but_trump_card)
            if turn_index:
                # checking since lb_trump_call is not packed for turn_index==0
                lb_trump_call.grid_forget()
            self.but_game_nxt.configure(text='Trump revealed',command=lambda:some_var16.set(1))
#             self.but_game_nxt.configure(command=lambda:some_var16.set(1))
            self.but_game_nxt.focus()
        
        lb_trump_call=tk.Label(self.fr_game_center,text='Calling trump',font=('GNU Unifont',15))
        
        if turn_index==0:
            # the choice of revealing or not already obtained from trump_call_instance() method for 
            # turn_index==0
            pass
        elif turn_index==1:
            lb_trump_call.grid(column=2,row=1,padx=20)
        elif turn_index==2:
            lb_trump_call.grid(column=1,row=0,pady=20)
        elif turn_index==3:
            lb_trump_call.grid(column=0,row=1,padx=20)
        else:
            print('\nSomething wrong abt turn_index')
            
        self.but_game_nxt.grid(column=1,row=1)
        self.but_game_nxt.focus()
        self.but_game_nxt.configure(command=trump_reveal)
        
        self.fr_game_center.wait_variable(some_var16)
    
    ############## gui_round1_trump_reveal() end ####################################
