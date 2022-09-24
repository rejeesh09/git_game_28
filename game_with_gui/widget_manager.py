# search for the term unfolder using the find and replace option under the edit tab and 
# replace it with the same to get all the folded blocks of code unblocked. or else 
# searching using ctl-f will not yield results from the folded blocks
import tkinter as tk

class Widgets():
    '''All the gui/tkinter methods used in the code are defined here'''
    
    def __init__(self,root):
        '''Takes as argument, a tkinter window (root = tkinter.Tk()).
        
        All frames used in subsequent methods are getting defined here. They were initially 
        defined in the respective methods where they were required, but later collected here for 
        better book-keeping. 
        
        In addition, some other widgets which were defined initially in methods where they were 
        not actually used but defined only in anticipation of use in other methods are also 
        now collected here'''
        
        
        # the root window which was passed from the final(main) code
        self.rt=root
        self.rt.columnconfigure((0,1,2),weight=1)
        self.rt.rowconfigure((0,1,2),weight=1)
        
        
        # the below frame, fr1 is used for initial messages and obtaining player name before 
        # displaying half hands. used in gui_player_name()
        self.fr1=tk.Frame(self.rt)
        self.fr1.columnconfigure((0,1),weight=1)
        self.fr1.rowconfigure((0,1),weight=1)
        
        
        # below are the frames used to display the hands and the names of the 4 'players'
        # used in gui_disp_half_hands() and gui_disp_full_hands()
        self.fr_0=tk.Frame(self.rt,background='DeepSkyBlue4')
        self.fr_1=tk.Frame(self.rt,background='DeepSkyBlue4')
        self.fr_2=tk.Frame(self.rt,background='DeepSkyBlue4')
        self.fr_3=tk.Frame(self.rt,background='DeepSkyBlue4')
        # making a list of the 4 frames
        self.fr_lst=[self.fr_0,self.fr_1,self.fr_2,self.fr_3]
        # another frame for the center of the root window, only used till bidding starts (i.e. half bid)
        self.fr_center=tk.Frame(self.rt,background='white')
        
        
        # the below frame hosts all widgets for the first round bidding (half bid)
        # it should be getting attached at the center of root windows, used only till end of half bid
        self.fr_hlf_bd_center=tk.Frame(self.rt,background='white')
        self.fr_hlf_bd_center.columnconfigure((0,1,2),weight=1)
        self.fr_hlf_bd_center.rowconfigure((0,1,2),weight=1)
        # the below widgets display the bid values in half bid
        self.lab_self_call=tk.Label(self.fr_hlf_bd_center,text='Waiting bid turn',font=('GNU Unifont',15))
        self.lab_right_call=tk.Label(self.fr_hlf_bd_center,text='Waiting bid turn',font=('GNU Unifont',15))
        self.lab_mate_call=tk.Label(self.fr_hlf_bd_center,text='Waiting bid turn',font=('GNU Unifont',15))
        self.lab_left_call=tk.Label(self.fr_hlf_bd_center,text='Waiting bid turn',font=('GNU Unifont',15))
        # the above 4 widgets are collected in a list
        self.lab_call_lst=[self.lab_self_call,self.lab_right_call,\
                           self.lab_mate_call,self.lab_left_call]
        # a center clickable-button in the frame fr_hlf_bd_center
        self.but_next=tk.Button(self.fr_hlf_bd_center,text='>>',font=('GNU Unifont',15))
        
        
        # the below frame is used for taking input from the player in half bid round, 
        # it could be used for both bid value and trump entry if any (frame: fr_hlf_bd_center)
        # it should be getting attached in the cell(column=1,row=2) of the root window and is used only
        # in half bid round
        self.fr_hlf_bd_center_bot=tk.Frame(self.fr_hlf_bd_center,bg='white')
        self.fr_hlf_bd_center_bot.columnconfigure((0,1),weight=1)
        self.fr_hlf_bd_center_bot.rowconfigure((0,1),weight=1)
        
        
        # the below frame hosts all the widgets in full bid round. It should be getting attached at the 
        # center of the root window. Used only till end of full bid.
        self.fr_fll_bd_center=tk.Frame(self.rt,background='white')
        self.fr_fll_bd_center.columnconfigure((0,1,2),weight=1)
        self.fr_fll_bd_center.rowconfigure((0,1,2),weight=1)        
        # a center clickable-button in frame fr_fll_bd_center
        self.but_fll_nxt=tk.Button(self.fr_fll_bd_center,text='Start 2nd bidding',font=('GNU Unifont',15))
        
        
        # the below fram hosts all widgets for play in round 1.
        self.fr_game_center=tk.Frame(self.rt, background='white')
        self.fr_game_center.columnconfigure((0,1,2),weight=1)
        self.fr_game_center.rowconfigure((0,1,2),weight=1)       
        
    ########################## __init__() end #######################################   
    
    def gui_player_name(self):
        """Displays gui window for taking player name as input
        
        Widgets(lab1,ent1,but1,lab2 and but2) are attached to the frame fr1 in this method.
        
        The method is called from __init__ of Deck() class"""
                
        # attaching the frame 
        self.fr1.pack(side=tk.TOP, pady=300)

        name_var=tk.StringVar()
        self.name=name_var.get()
        wait_var=tk.IntVar()        
        
        # to clear the current frame for other frames to come (button command)
        def clear_fr1():
            self.fr1.pack_forget()
            wait_var.set(1)
        
        # to save the name entered by player (button command)
        def save_name():
            global name
            name=name_var.get()
            
            lab1.grid_forget()
            ent1.grid_forget()
            but1.grid_forget()
            
            lab2=tk.Label(self.fr1,text='Name entered is: '+name,font=('GNU Unifont',20))
            but2=tk.Button(self.fr1, text='Deal',font=('GNU Unifont',20),command=clear_fr1)
            lab2.pack()
            but2.pack()
            
            but2.focus()
        
        # widgets for taking name input (frame: fr1)
        lab1=tk.Label(self.fr1,text='Name:',font=('GNU Unifont',20))
        ent1=tk.Entry(self.fr1,textvariable=name_var,font=('GNU Unifont',20))
        but1=tk.Button(self.fr1,text='Enter', font=('GNU Unifont',20),command=save_name)
        ent1.focus()

        # attaching the widgets for name input
        lab1.grid(row=0,column=0,sticky='')
        ent1.grid(row=0,column=1,sticky='')
        but1.grid(row=1,column=1,sticky='')
        
        self.fr1.wait_variable(wait_var)
        
        return(name)
    
    ########################## gui_player_name() end ################################
        
    def gui_disp_half_hands(self,players_lst,obj_half_deal_lst):
        """Displays the half hands(4 cards) of all players
        
        Takes as argument, players list and obj_half deal_lst.
        It attaches the four frames(fr_0,fr_1,fr_2,fr_3) for displaying the hands and the names of 
        the players.
        It creates the buttons for the half hands and attaches them and the name button in the 
        respective frames as well (button_lst_4_nme, button_lst_4_crd(list of lists)).
        It attaches a center frame(fr_center) as well with a clickable message widget(but_cen) and 
        detaches (the frame) at exit.
        
        The method is  called from obj_display_half_hands() in Deck(), through __init__ of Round_1() 
        via __init__ of Prepare_game()"""             
        
        self.players_lst=players_lst        
        
        some_var=tk.IntVar()
        
        # frames for showing the hands getting attached (to root window)
        self.fr_0.grid(column=1,row=2,sticky=tk.S,pady=40)
        self.fr_1.grid(column=2,row=1,sticky=tk.E,padx=40)        
        self.fr_2.grid(column=1,row=0,sticky=tk.N,pady=40)        
        self.fr_3.grid(column=0,row=1,sticky=tk.W,padx=40)
        
        # creating the name buttons and appending to a list
        # each button is created in each of the 4 frames in the list fr_lst
        button_lst_4_nme=[]
        for i in range(4):
            button_lst_4_nme.append(tk.Button(self.fr_lst[i],text=self.players_lst[i],\
                                              font=('GNU Unifont',15)))
            button_lst_4_nme[i].pack(side=tk.BOTTOM,pady=10)

        # creating the card buttons and appending to a list inside a list
        # each set of four buttons in the corresponding frame from the list fr_lst
        self.button_lst_4_crd=[[],[],[],[]]
        for j in range(4):
            for i in range(4):
                k=obj_half_deal_lst[j][i]
                self.button_lst_4_crd[j].append(tk.Button(self.fr_lst[j],text=k.form(),fg=k.colour(),\
                                                     font=('GNU Unifont',15)))
                self.button_lst_4_crd[j][i].pack(side=tk.LEFT)
        
        
        # to clear the frame fr_center(in root window) for other frames to come (button command)
        def clear_fr_cen():
            self.fr_center.grid_forget()
            some_var.set(1)
        
        # attaching the frame fr_center in root window
        self.fr_center.grid(column=1,row=1)
    
        # a center clickable-button to start first round bidding (half hand)
        but_cen=tk.Button(self.fr_center,text='Start bidding',font=('GNU Unifont',15),command=clear_fr_cen)
        but_cen.pack(side=tk.TOP,pady=10)
        but_cen.focus()
        
        self.fr_center.wait_variable(some_var)
        
    ############### gui_disp_half_hands() end #######################################
    
    def gui_half_bid_mes(self,first_bidder):
        """Window showing the lead bidder name before first round of bidding(half-bid) starts
        
        Takes as argument the round1 lead bidder name
        It attaches the the frame fr_hlf_bd_center to the root window and 
        the message widget, lab_mes and a clickable button, but_next to the frame. The label widgets, 
        (lab_self_call,_right_call,_mate_call,_left_call) for displaying the calls of each player 
        are attached on exit. but_next widget is detached on exit.
        
        The method is called from bid_half_hand() in Prepare_game() class."""
        
        some_var2=tk.IntVar()

        # to clear the bidding start message and to create the labels for half bid calls (button command)
        def hlf_bd_mes_forget():
            lab_mes.grid_forget()
            self.but_next.grid_forget()
            
            # attaching the labels for displaying half bid values (frame: fr_hlf_bd_center)
            # these are used in gui_half_bid_values() and gui_half_bid_entry() which are the methods 
            # that logically follow
            self.lab_self_call.grid(row=2,column=1,sticky='')
            self.lab_right_call.grid(row=1,column=2,sticky='')
            self.lab_mate_call.grid(row=0,column=1,sticky='')
            self.lab_left_call.grid(row=1,column=0,sticky='')
            
            some_var2.set(1)                   
        
        # this frame is positioned at the center cell of the self.rt window
        self.fr_hlf_bd_center.grid(column=1,row=1,sticky='NSEW')
        
        # a widget to display who starts the half bid (frame: fr_hlf_bd_center)
        lab_mes=tk.Label(self.fr_hlf_bd_center,text='Bidding starts with '+first_bidder,\
                        font=('GNU Unifont',15))
        lab_mes.grid(column=1,row=0,sticky='')
        
        # a next button - defined in __init__(), (frame: fr_hlf_bd_center)
        self.but_next.configure(command=hlf_bd_mes_forget)
        self.but_next.grid(column=1,row=1,sticky='')
        self.but_next.focus()
        
        self.fr_hlf_bd_center.wait_variable(some_var2)
        
    ############## gui_half_bid_mes() end ###########################################
    
    def gui_half_bid_values(self,bidder_indx,bid_val,calls):
        """Window showing the call values and passes in the half bid round
        
        Takes as argument, the bidder index, the bid value and a boolean to check if there has been a 
        call or not.
        It configures the message on the call labels according to the arguments. Clickable widget 
        but_next is attached(fr_half_bd_center)
        
        The method is called twice from bid_half_hand() in Prepare_game() class."""
        
        some_var4=tk.IntVar()
        
        # if someone has made a call in half bid
        if calls:
            self.lab_call_lst[bidder_indx].configure(text=self.players_lst[bidder_indx]+' calls '+str(bid_val))
        # i.e. if someone has passed a call in half bid
        else:
            self.lab_call_lst[bidder_indx].configure(text=self.players_lst[bidder_indx]+' passes ')

        # positioning the clickable-center button for going to next step (frame: fr_hlf_bd_center)
        # actually this button was already attached in gui_half_bid_mes(), so it would remain in the 
        # frame even if not attached here
        self.but_next.grid(row=1,column=1,sticky='')
        self.but_next.configure(command=lambda:some_var4.set(1))
        self.but_next.focus()
        
        self.fr_hlf_bd_center.wait_variable(some_var4)
        
    ############## gui_half_bid_values() end ########################################
    
    def gui_half_bid_entry(self):
        """Window for taking the bid value(half bid) as input from the player
        
        It detaches the but_next button and self_call label from fr_half_bd_center and 
        attaches a frame fr_half_bd_center_bot to it. 
        Widgets for taking input are attached to the center_bot frame and the frame is detached on exit.
        self_call widget is attached back to fr_half_bd_center on exit.
        The method gui_half_bid_values() logically follows this method. but_next button would 
        be attached in that method.
        
        The method is called from bid_half_hand() in Prepare_game() class."""
                
        half_bid_var=tk.StringVar()
        some_var3=tk.IntVar()
        
        # forgetting the clickable-next button and self_call label to focus on the bid entry
        self.but_next.grid_forget()
        self.lab_self_call.grid_forget()
        
        # to save bid value and clear some widgets and frame (button command)
        def save_hlf_bd_val():
            global half_bid_val
            half_bid_val=half_bid_var.get()
            # induvidual widgets getting detached as well in addition to their frame, as the frame 
            # is going to be used again
            self.lab_hlf_bd_val.grid_forget()
            self.ent_hlf_bd_val.grid_forget()
            self.but_hlf_bd_val.grid_forget()
            self.fr_hlf_bd_center_bot.grid_forget()
            # re-attaching the self_call label which was detached at the beginning of the current method
            # (frame: fr_hlf_bd_center)
            self.lab_self_call.grid(row=2,column=1,sticky='')

            some_var3.set(1)        
        
        # attaching the frame for player input        
        self.fr_hlf_bd_center_bot.grid(column=1,row=2,sticky='NSEW')
        # widgets for player input (frame: self.fr_hlf_bd_center_bot)
        self.lab_hlf_bd_val=tk.Label(self.fr_hlf_bd_center_bot,text='Enter bid value',font=('GNU Unifont',15))
        self.ent_hlf_bd_val=tk.Entry(self.fr_hlf_bd_center_bot,textvariable=half_bid_var,font=('GNU Unifont',15))
        self.but_hlf_bd_val=tk.Button(self.fr_hlf_bd_center_bot,text='Enter', font=('GNU Unifont',15),\
                                 command=save_hlf_bd_val)
        # attaching the widgets (frame: fr_hlf_bd_center_bot)
        self.lab_hlf_bd_val.grid(row=0,column=0,sticky='')
        self.ent_hlf_bd_val.grid(row=0,column=1,sticky='')
        self.but_hlf_bd_val.grid(row=1,column=1,sticky='')        
        self.ent_hlf_bd_val.focus()
        
        self.fr_hlf_bd_center.wait_variable(some_var3)
        
        return(half_bid_val)
        
    ############## gui_half_bid_entry() end #########################################
    
    def gui_half_bid_trump(self,bid_val):
        """The method takes the trump card input from the player if the player happens to be 
        the highest bidder in half bid round
        
        Takes as argument, the bid value to display the message before taking input
        All the call labels are detached(fr_half_bd_center). A message widget is created and 
        attached along with the half_bd_center_bot frame() and its widgets.
        All widgets in fr_half_bd_center are detached on exit and but_next is attached
        
        The method is called, if needed, from bid_half_hand() in Prepare_game() class."""
        
        # detaching call widgets (frame: fr_hlf_bd_center) to focus on player entry, the clickable-center
        # button is not detached yet
        self.lab_self_call.grid_forget()
        self.lab_right_call.grid_forget()
        self.lab_mate_call.grid_forget()
        self.lab_left_call.grid_forget()
        
        some_var6=tk.IntVar()
        trump_var=tk.StringVar()
        
        # (button command)
        def save_trump():
            global hlf_bd_trump
            hlf_bd_trump=trump_var.get()
            
            # detaching the frame and not the induvidual widgets as well coz this frame may not 
            # be getting used again
            self.fr_hlf_bd_center_bot.grid_forget()
            # changing the message on displya label (frame: fr_hlf_bd_center)
            self.lab_hlf_bd_mes_fnl.configure(text='Trump card set by '+self.players_lst[0])
            # re-attaching and reconfiguring the clickable-next button, which was detached in the 
            # take_trump() button command function
            self.but_next.configure(text='Deal full hand',command=lambda:some_var6.set(1))
            self.but_next.grid(column=1,row=1,sticky='')
            self.but_next.focus()            
        
        # (button command)
        def take_trump():
            self.but_next.grid_forget()
            # re-attaching the below frame aft it got detached in gui_half_bid_entry()
            self.fr_hlf_bd_center_bot.grid(column=1,row=2,sticky='NSEW')
            # new widgets for taking trump input (frame: fr_hlf_bd_center_bot)
            self.lab_hlf_bd_trmp=tk.Label(self.fr_hlf_bd_center_bot,text='Enter trump card',font=('GNU Unifont',15))
            self.ent_hlf_bd_trmp=tk.Entry(self.fr_hlf_bd_center_bot,textvariable=trump_var,font=('GNU Unifont',15))
            self.but_hlf_bd_trmp=tk.Button(self.fr_hlf_bd_center_bot,text='Enter', font=('GNU Unifont',15),\
                                     command=save_trump)
           
            self.lab_hlf_bd_trmp.grid(row=0,column=0,sticky='')
            self.ent_hlf_bd_trmp.grid(row=0,column=1,sticky='')
            self.but_hlf_bd_trmp.grid(row=1,column=1,sticky='')            
            self.ent_hlf_bd_trmp.focus()
        
        # label displaying the highest bidder in half bid (frame: fr_hlf_bd_center)
        self.lab_hlf_bd_mes_fnl=tk.Label(self.fr_hlf_bd_center,\
                    text=self.players_lst[0]+' made the highest bid '+str(bid_val),font=('GNU Unifont',15))
        self.lab_hlf_bd_mes_fnl.grid(row=0,column=1,sticky='')
        
        # this button though detached in gui_hlf_bd_entry(), gets re-attached in gui_hlf_bd_values() 
        # which 'succeeds' the entry() method and 'precedes' the current method (frame: fr_hlf_bd_center)
        self.but_next.configure(command=take_trump)
        self.but_next.focus()
                
        self.fr_hlf_bd_center.wait_variable(some_var6)        
        return(hlf_bd_trump)
        
    ############## gui_half_bid_trump() end #########################################
    
    def gui_half_bid_declare(self,bidder_indx,bid_val):
        """Window for declaring the highest bidder of half bid round, for the three comp hands
        
        Takes as argument the highest bidder index and the corresponding bid value.
        It detaches all the bid call labels and displays message label regarding the highest bidder 
        and configures the already attached but_next button.
        
        The method is called from bid_half_hand() in Prepare_game() class."""
        
        # all the labels displaying bid call are detached (frame: fr_hlf_bd_center)
        self.lab_self_call.grid_forget()
        self.lab_right_call.grid_forget()
        self.lab_mate_call.grid_forget()
        self.lab_left_call.grid_forget()
        
        some_var5=tk.IntVar()
        
        # button command to configure messages displayed
        def disp_val():
            self.lab_hlf_bd_mes_fnl.configure(text='Trump card set by '+self.players_lst[bidder_indx])
            self.but_next.configure(text='Deal full hand',command= lambda: some_var5.set(1))
            self.but_next.focus()
        
        # label for displaying the highest bidder message (frame: fr_hlf_bd_center)
        self.lab_hlf_bd_mes_fnl=tk.Label(self.fr_hlf_bd_center,\
                            text=self.players_lst[bidder_indx]+' made the highest bid '+str(bid_val),\
                                   font=('GNU Unifont',15))
        self.lab_hlf_bd_mes_fnl.grid(row=0,column=1,sticky='')
        
        # clickable-button(already attached from gui_half_bid_values) is configured
        self.but_next.configure(command=disp_val)
        self.but_next.focus()
        
        self.fr_hlf_bd_center.wait_variable(some_var5)
        
    ############## gui_half_bid_declare() end #######################################
    
    def gui_disp_full_hands(self,highest_bidder_indx,trump_revealed,trump_card,obj_deal_lst_copy,situation):
        """Window for displaying the full set of hands
        
        Takes as argument the highest bidder index, boolean on whether trump is revealed or not(not 
        really required), trump_card, obj_deal_lst_copy and the situation variable indicating whether 
        the call is just after half bid or after the full bid.
        
        
        The method is called through obj_display_hands() in Deck(), which is called at the end of 
        bid_half_hand()-(situation==0) and also at the end of bid_full_hand()-(situation==1) in 
        Prepare_game() class."""
    
        
        some_var13=tk.IntVar()
        
        # situation==0 corresponds to display before full bid, situation==1 for aft full bid.
        if situation==0:
            
            some_var7=tk.IntVar()
            
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

            # the trump card set in half bid will not be available in obj_deal_copy(for the comp hands), 
            # and the button for that wouldn't be created(situ==0). But if player was the highest bidder, 
            # the button corresponding to trump card is being removed here.
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

            # attaching the frame fr_fll_bd_center to the center of root window 
            self.fr_fll_bd_center.grid(column=1,row=1,sticky='NSEW')
            
            # configuring and attaching the clickable-button at the center (frame: fr_fll_bd_center)
            self.but_fll_nxt.configure(command=lambda:some_var7.set(1))
            self.but_fll_nxt.grid(row=1,column=1,sticky='')
            self.but_fll_nxt.focus()

            self.fr_fll_bd_center.wait_variable(some_var7)
            
        elif situation==1:
        # i.e. the full hand display method is being called after bidding is over and round1 to start
            
            some_var13=tk.IntVar()
            
            if self.lab_full_bd_mes_fnl.winfo_ismapped():
                self.lab_full_bd_mes_fnl.grid_forget()
            
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
                
            
            # button command to detach fr_fll_bd_center and attach fr_game_center with widgets
            def clear_fll_bd_fr2():
                
                if self.fr_fll_bd_center.winfo_ismapped():
#                     print("\ndebug print - fr_fll_bd_center is packed")
                    self.fr_fll_bd_center.grid_forget()
                
                # attaching the frame fr_game_center to the center of root window
                self.fr_game_center.grid(column=1,row=1,sticky='NSEW')

                # creating and attaching the clickable-button but_game_nxt (frame: fr_game_center)
                # the frame did not show the button when defined in init and just attached here.??
                self.but_game_nxt=tk.Button(self.fr_game_center,text='Round 1',font=('GNU Unifont',15))
                self.but_game_nxt.grid(row=1,column=1,sticky='')
                
                self.but_game_nxt.configure(command=lambda:some_var13.set(1))
                self.but_game_nxt.focus()
#                 print("\nprint for debug in gui_disp_full_hands after 2nd bid()\n")
#                 print("1_some_var13 is set to: \n",some_var13.get())

            # attaching and configuring the clickable-button (frame: fr_fll_bd_center)
            self.but_fll_nxt.configure(text='Start game',command= clear_fll_bd_fr2)
            self.but_fll_nxt.grid(column=1,row=1,sticky='')
            self.but_fll_nxt.focus()
            
            self.fr_game_center.wait_variable(some_var13)
        
    ############### gui_disp_full_hands() end #######################################
    
    def gui_full_bid_mes(self,first_bidder):
    # called right at the beginning of bid_full_hand() in Prepare_game()
        
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
    # called from bid_full_hand() at the beginning of the while loop 'while self.bid2_counter<8:' 
    # in Prepare_game()
                
        full_bid_var=tk.StringVar()
        some_var9=tk.IntVar()
        
        self.but_fll_nxt.grid_forget()
        
        self.lab_self_fcall.grid(row=2,column=1,sticky='')
        # the above line is to make sure that self.lab_sefl_fcall.grid_forget() which comes later 
        # wont throw an error(say if player is starting the bid)
        self.lab_right_fcall.grid(row=1,column=2,sticky='')
        self.lab_mate_fcall.grid(row=0,column=1,sticky='')
        self.lab_left_fcall.grid(row=1,column=0,sticky='')
            
        
        def save_full_bd_val():
            global full_bid_val
            full_bid_val=full_bid_var.get()
            
            lab_full_bd_val.grid_forget()
            ent_full_bd_val.grid_forget()
            but_full_bd_val.grid_forget()
            self.fr_fll_bd_center_bot.grid_forget()
            # should the widgets in the frame be induvidually unpacked if the frame is to 
            # be packed again for other widgets?
        
            some_var9.set(1)
            
        
        self.lab_self_fcall.grid_forget()
        
        # creating a frame in the bottom cell (col=1,rw=2) of the fll_bd_center frame
        # to take full bid entry from player
        self.fr_fll_bd_center_bot=tk.Frame(self.fr_fll_bd_center,bg='white')
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
    # called from bid_full_hand() in Prepare_game() after checking the self.bid2_value in
    # 'if (self.bid2_value>self.bid2_value_final):' and with the argument calls=True/False 
    # based on the result

        
        some_var10=tk.IntVar()
        
    
        if calls:
        # someone has made a call in the 2nd round bid
            self.lab_fcall_lst[bidder_indx].configure(text=self.players_lst[bidder_indx]+' calls '+str(bid_val))

        else:
        # someone has passed a call in 2nd round bid
            self.lab_fcall_lst[bidder_indx].configure(text=self.players_lst[bidder_indx]+' passes ')

        # attaching the labels for 2nd bid calls - these labels are created in gui_full_bid_mes()
        self.lab_self_fcall.grid(row=2,column=1,sticky='')
        self.lab_right_fcall.grid(row=1,column=2,sticky='')
        self.lab_mate_fcall.grid(row=0,column=1,sticky='')
        self.lab_left_fcall.grid(row=1,column=0,sticky='')
        
        # creating a label for the final message of 2nd round bidding(full bid)
        self.lab_full_bd_mes_fnl=tk.Label(self.fr_fll_bd_center,text='',font=('GNU Unifont',15))
        
        # the below button is created in gui_disp_fll_hands() in situation==0, in frame 
        # fr_fll_bd_center
        self.but_fll_nxt.configure(command=lambda:some_var10.set(1))
        self.but_fll_nxt.grid(row=1,column=1,sticky='')
        self.but_fll_nxt.focus()
        
        self.fr_fll_bd_center.wait_variable(some_var10)
        
    ############## gui_full_bid_values() end ########################################
    
    def gui_full_bid_trump(self,bid_val):
    # called from bid_full_hand() in Prepare_game()
        
        # detatching the labels used for calls in full bid (frame: fr_fll_bd_center)
        self.lab_self_fcall.grid_forget()
        self.lab_right_fcall.grid_forget()
        self.lab_mate_fcall.grid_forget()
        self.lab_left_fcall.grid_forget()
        
        some_var11=tk.IntVar()
        trump_var=tk.StringVar()
        
        # detatching the center button as well (frame: fr_fll_bd_center)
        self.but_fll_nxt.grid_forget()
        
        self.fr_game_center=tk.Frame(self.rt, background='white')
        self.fr_game_center.columnconfigure((0,1,2),weight=1)
        self.fr_game_center.rowconfigure((0,1,2),weight=1)
        
        # an additional frame in the bottom middle cell of fr_game_center for player input
        self.fr_game_center_bot=tk.Frame(self.fr_game_center,background='white')
        self.fr_game_center_bot.columnconfigure((0,1),weight=1)
        self.fr_game_center_bot.rowconfigure((0,1),weight=1)
        
#         def declare_f():
            
#             self.lab_full_bd_mes_fnl.configure(text='Trump card set by '+self.players_lst[0])
#             self.but_fll_nxt.configure(text='>>')
#             self.but_fll_nxt.configure(command= lambda: some_var11.set(1))
#             self.but_fll_nxt.focus()
        
        def save_trump_f():
            global full_bd_trump
            full_bd_trump=trump_var.get()
            
            self.lab_full_bd_trmp.grid_forget()
            self.ent_full_bd_trmp.grid_forget()
            self.but_full_bd_trmp.grid_forget()
            # this below frame may be used again, so unpacking all buttons as well before the frame
            self.fr_fll_bd_center_bot.grid_forget()
            
#             self.but_fll_nxt.configure(command=declare_f)
#             self.but_fll_nxt.grid(column=1,row=1,sticky='')
#             self.but_fll_nxt.focus()

            self.lab_full_bd_mes_fnl.configure(text='Trump card set by '+self.players_lst[0])
            self.but_fll_nxt.configure(text='>>',command= lambda: some_var11.set(1))
            self.but_fll_nxt.grid(column=1,row=1,sticky='')
            self.but_fll_nxt.focus()
            
        
#         def take_trump_f():
#             self.but_fll_nxt.grid_forget()
#             self.lab_full_bd_trmp=tk.Label(self.fr_fll_bd_center_bot,text='Enter trump card',font=('GNU Unifont',15))
#             self.ent_full_bd_trmp=tk.Entry(self.fr_fll_bd_center_bot,textvariable=trump_var,font=('GNU Unifont',15))
#             self.but_full_bd_trmp=tk.Button(self.fr_fll_bd_center_bot,text='Enter', font=('GNU Unifont',15),\
#                                      command=save_trump_f)

#             self.fr_fll_bd_center_bot.grid(column=1,row=2,sticky='NSEW')
            
#             self.lab_full_bd_trmp.grid(row=0,column=0,sticky='')
#             self.ent_full_bd_trmp.grid(row=0,column=1,sticky='')
#             self.but_full_bd_trmp.grid(row=1,column=1,sticky='')            
#             self.ent_full_bd_trmp.focus()
        
        self.lab_full_bd_mes_fnl.configure(text=self.players_lst[0]+' made the highest bid '+str(bid_val))
        self.lab_full_bd_mes_fnl.grid(row=0,column=1,sticky='')        
#         self.but_fll_nxt.configure(command=take_trump_f)
#         self.but_fll_nxt.grid(column=1,row=1,sticky='')
#         self.but_fll_nxt.focus()
        self.lab_full_bd_trmp=tk.Label(self.fr_fll_bd_center_bot,text='Enter trump card',font=('GNU Unifont',15))
        self.ent_full_bd_trmp=tk.Entry(self.fr_fll_bd_center_bot,textvariable=trump_var,font=('GNU Unifont',15))
        self.but_full_bd_trmp=tk.Button(self.fr_fll_bd_center_bot,text='Enter', font=('GNU Unifont',15),\
                                 command=save_trump_f)

        self.fr_fll_bd_center_bot.grid(column=1,row=2,sticky='NSEW')

        self.lab_full_bd_trmp.grid(row=0,column=0,sticky='')
        self.ent_full_bd_trmp.grid(row=0,column=1,sticky='')
        self.but_full_bd_trmp.grid(row=1,column=1,sticky='')            
        self.ent_full_bd_trmp.focus()
        
        
        self.fr_fll_bd_center.wait_variable(some_var11)        
        return(full_bd_trump)
        
    ############## gui_full_bid_trump() end #########################################
    
    def gui_full_bid_declare(self,bidder_indx,bid_val,no_call):
    # called from bid_full_hand() in Prepare_game()
        
        self.lab_self_fcall.grid_forget()
        self.lab_right_fcall.grid_forget()
        self.lab_mate_fcall.grid_forget()
        self.lab_left_fcall.grid_forget()
        
        global some_var12
        some_var12=tk.IntVar()
        
        self.fr_game_center=tk.Frame(self.rt, background='white')
        self.fr_game_center.columnconfigure((0,1,2),weight=1)
        self.fr_game_center.rowconfigure((0,1,2),weight=1)
        
        # an additional frame in the bottom middle cell of fr_game_center for player input
        self.fr_game_center_bot=tk.Frame(self.fr_game_center,background='white')
        self.fr_game_center_bot.columnconfigure((0,1),weight=1)
        self.fr_game_center_bot.rowconfigure((0,1),weight=1)
        
#         def set_var():
#             some_var12.set(1)
        
        def clear_fll_bd_fr1():
            
            self.fr_fll_bd_center.grid_forget()
            
            self.fr_game_center.grid(column=1,row=1,sticky='NSEW')

        
            self.but_game_nxt=tk.Button(self.fr_game_center,text='Round1',font=('GNU Unifont',15))
            self.but_game_nxt.grid(column=1,row=1,sticky='')
            self.but_game_nxt.focus()
#             print("1_some_var12 is set to: \n",some_var12.get())
            
            # creating a list to hold the card buttons played in gui_card_played
            self.but_r1_played_card_lst=[]
        
            self.but_game_nxt.configure(command=lambda:some_var12.set(1))
            # the below code was causing problem since it is a duplicate of what happens in 
            # disp_full_hands when called through obj_display_hands() - not tested enough
#             self.but_game_nxt.configure(command=set_var)
#             self.but_game_nxt.focus()
#             print("\nprint for debug in gui_full_bid_declare()\n")
#             print("2_some_var12 is set to: \n",some_var12.get())
#             some_var12.set(1)
#             some_var12.set(1)
        
        def disp_val_f():
            self.lab_full_bd_mes_fnl.configure(text='Trump card set by '+self.players_lst[bidder_indx])
            self.but_fll_nxt.configure(text='>>')
            self.but_fll_nxt.configure(command= lambda: some_var12.set(1))
#             self.but_fll_nxt.configure(command= clear_fll_bd_fr2)
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
            self.but_fll_nxt.configure(command= clear_fll_bd_fr1)
            self.but_fll_nxt.focus()
            
        
        self.fr_game_center.wait_variable(some_var12)
        
    ############## gui_full_bid_declare() end #######################################
    
    
    #----------------------------- round1 widgets ----------------------------------#
    
    
    def gui_card_played(self,turn_index,card_played):
        """
        This method is called from the end of round1_lead_logic() and round1_follow_logic() in Round_1().
        trump_revealed status is to be checked and trump_card_button is to be dealt with
        """
        
        some_var14=tk.IntVar() 

        self.but_r1_played_card_lst=[]
        
        for i in self.button_lst_4_crd[turn_index]:
            if i['text']==card_played.form():
                # this is where the played card is removed from the shown hand(button_lst_4_crd)
                i.pack_forget()
                
                # a new button for the played card is formed and attached according to the 
                # turn_index and appended to the list which holds these buttons
                self.but_r1_played_card_lst.append(tk.Button(self.fr_game_center,text=card_played.form(),\
                                          fg=card_played.colour(),font=('GNU Unifont',15)))
                # attaching the buttons based on the turn index. Each button is given a name as detaching 
                # them by accessing through list index doesnot seem to work in gui_round1_summary() method
                if turn_index==0:
                    self.but_r1_player_card=self.but_r1_played_card_lst[-1]
                    self.but_r1_player_card.grid(column=1,row=2,pady=20)
                elif turn_index==1:
                    self.but_r1_right_card=self.but_r1_played_card_lst[-1]
                    self.but_r1_right_card.grid(column=2,row=1,padx=20)
                elif turn_index==2:
                    self.but_r1_mate_card=self.but_r1_played_card_lst[-1]
                    self.but_r1_mate_card.grid(column=1,row=0,pady=20)
                elif turn_index==3:
                    self.but_r1_left_card=self.but_r1_played_card_lst[-1]
                    self.but_r1_left_card.grid(column=0,row=1,padx=20)
                else:
                    print('\nSomething wrong abt turn_index')
        
#         def nxt_hnd():
#             some_var14.set(1)
                    
        self.but_game_nxt.configure(text='>>',command=lambda:some_var14.set(1))
        self.but_game_nxt.grid(column=1,row=1)
        self.but_game_nxt.focus()
        
        self.fr_game_center.wait_variable(some_var14)
        
    ############## gui_card_played() end ############################################
    
    def gui_round1_card_entry(self):
        """
        This method is used whenever the player(not comp) has to input a card, 
        either while leading the round or following in the round
        The method brings up the widgets specific to taking input.
        The method is called from round1_lead_logic() and round1_follow_logic() in Round_1()
        """
        
        some_var15=tk.IntVar()
        round1_card=tk.StringVar()
        
        def save_round1_card():
            global round1_entry
            round1_entry=round1_card.get()

            self.fr_game_center_bot.grid_forget()

            some_var15.set(1)
                    
        # detaching the clickable next button (frame: fr_game_center)
        self.but_game_nxt.grid_forget()
        
        # attaching the bottom frame in fr_game_center for player input
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
        """
        This method deals with the situation of trump call by player in round1
        Not applicable to comp hands and only for the player.
        This method is called from round1_follow_logic() in Round_1().
        """
        
#         ret_val=0
        ret_var=tk.IntVar()
    
#         # to remove widgets from round1_card_entry
#         self.fr_game_center_bot.grid_forget()
        
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
    
    def gui_round1_trump_reveal(self,turn_index,trump_card,highest_bidder_index):
        """
        This method is called from round1_follow_logic() in Round_1()
        The method with the situ when trump is called (by comp hand) and revealed and the 
        trump_card/trump_card2 button is to be revealed i.e. replaced with the form() of trump_card
        """
        
        some_var16 = tk.IntVar()
        
        def trump_reveal():
            self.but_trump_card.configure(text=trump_card.form(),bg='white',fg=trump_card.colour())
            # adding the new card created to list for card buttons, so that when that card is 
            # played, it can be removed from the button list as well like other cards
#             self.button_lst_4_crd[turn_index].append(self.but_trump_card)
            # the trump card needs to be added to the list of highest bidder and not the 
            # current_turn_index
            self.button_lst_4_crd[highest_bidder_index].append(self.but_trump_card)

#             print(f"\ndebug print - turn_index = {turn_index}")
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
    
    def gui_round1_summary(self,point_oppo_team,point_player_team,round2_lead_player):
        """
        This method displays the summary at the end of round1, called from round1_paly() in Round_1()
        """
    
        some_var17=tk.IntVar()
        
        # button command
        def round2_lead():
            self.lb_point_oppo_team.grid_forget()
            self.lb_point_player_team.grid_forget()
            self.lb_r2_lead=tk.Label(self.fr_game_center,text='Round 2 starts with: '+round2_lead_player,\
                               font=('GNU Unifont',15))
            self.lb_r2_lead.grid(column=1,row=0,sticky='')
            self.but_game_nxt.configure(text='>>',command=lambda:some_var17.set(1))
            self.but_game_nxt.focus()
            
        # button command
        def points():
            # using grid_forget with list iteration does not seem to work, it detaches only the last 
            # button in list. Therefore each card in list is given separate name and detached (why?)
            self.but_r1_player_card.grid_forget()
            self.but_r1_right_card.grid_forget()
            self.but_r1_mate_card.grid_forget()
            self.but_r1_left_card.grid_forget()
            # labels for displaying each team points (frame: fr_game_center)
            self.lb_point_oppo_team=tk.Label(self.fr_game_center,text='Oppo_team: '+str(point_oppo_team),\
                                        font=('GNU Unifont',15))
            self.lb_point_player_team=tk.Label(self.fr_game_center,text='Your_team: '+str(point_player_team),\
                                         font=('GNU Unifont',15))
            self.lb_point_oppo_team.grid(column=1,row=0,sticky='')
            self.lb_point_player_team.grid(column=1,row=2,sticky='')
            # clickable next button (frame: fr_game_center)
            self.but_game_nxt.configure(text='>>',command=round2_lead)
            self.but_game_nxt.focus()
        
        # configuring and attaching clickable next button (frame: fr_game_center)
        self.but_game_nxt.configure(text='Points taken',command=points)
        self.but_game_nxt.grid(column=1,row=1,stick='')
        self.but_game_nxt.focus()
                
        self.fr_game_center.wait_variable(some_var17)
        
    ############## gui_round1_summary() end #########################################
    
    
    #----------------------------- round2 widgets ----------------------------------#
    
    
    def gui_card_played2(self,turn_index,card_played):
        """
        This method is called from the end of round2_lead_logic() and round2_follow_logic() in Round_2().
        trump_revealed status is to be checked and trump_card_button is to be dealt with
        """
        
        some_var14b=tk.IntVar() 

        self.but_r2_played_card_lst=[]
        
        for i in self.button_lst_4_crd[turn_index]:
            if i['text']==card_played.form():
                # this is where the played card is removed from the shown hand(button_lst_4_crd)
                i.pack_forget()
                
                #to remove the widget displaying round2 lead
                self.lb_r2_lead.grid_forget()
                
                # a new button for the played card is formed and attached according to the 
                # turn_index and appended to the list which holds these buttons
                self.but_r2_played_card_lst.append(tk.Button(self.fr_game_center,text=card_played.form(),\
                                          fg=card_played.colour(),font=('GNU Unifont',15)))
                # attaching the buttons based on the turn index. Each button is given a name as detaching 
                # them by accessing through list index doesnot seem to work in gui_round2_summary() method
                if turn_index==0:
                    self.but_r2_player_card=self.but_r2_played_card_lst[-1]
                    self.but_r2_player_card.grid(column=1,row=2,pady=20)
                elif turn_index==1:
                    self.but_r2_right_card=self.but_r2_played_card_lst[-1]
                    self.but_r2_right_card.grid(column=2,row=1,padx=20)
                elif turn_index==2:
                    self.but_r2_mate_card=self.but_r2_played_card_lst[-1]
                    self.but_r2_mate_card.grid(column=1,row=0,pady=20)
                elif turn_index==3:
                    self.but_r2_left_card=self.but_r2_played_card_lst[-1]
                    self.but_r2_left_card.grid(column=0,row=1,padx=20)
                else:
                    print('\nSomething wrong abt turn_index')
        
                    
        self.but_game_nxt.configure(text='>>',command=lambda:some_var14b.set(1))
        self.but_game_nxt.grid(column=1,row=1)
        self.but_game_nxt.focus()
        
        self.fr_game_center.wait_variable(some_var14b)
        
    ############## gui_card_played2() end ############################################
    
    def gui_round2_card_entry(self):
        """
        This method is used whenever the player(not comp) has to input a card, 
        either while leading the round or following in the round
        The method brings up the widgets specific to taking input.
        The method is called from round2_lead_logic() and round2_follow_logic() in Round_2()
        """
        
        some_var16=tk.IntVar()
        round2_card=tk.StringVar()
        
        def save_round2_card():
            global round2_entry
            round2_entry=round2_card.get()

            self.fr_game_center_bot.grid_forget()

            some_var16.set(1)
                    
        #to remove the widget displaying round2 lead
        self.lb_r2_lead.grid_forget()
        
        # detaching the clickable next button (frame: fr_game_center)
        self.but_game_nxt.grid_forget()
        
        # attaching the bottom frame in fr_game_center for player input
        self.fr_game_center_bot.grid(column=1,row=2,sticky='NSEW')

        
        # this is nw in a frame inside the cell at (2,1) of the fr_game_center
        self.lab_round2_card=tk.Label(self.fr_game_center_bot,text='Enter card',font=('GNU Unifont',15))
        self.ent_round2_card=tk.Entry(self.fr_game_center_bot,textvariable=round2_card,font=('GNU Unifont',15))
        self.lab_round2_card.grid(row=0,column=0,sticky='')
        self.ent_round2_card.grid(row=0,column=1,sticky='')
        self.ent_round2_card.focus()

        self.but_round2_card=tk.Button(self.fr_game_center_bot,text='Enter', font=('GNU Unifont',15),\
                                 command=save_round2_card)        
        self.but_round2_card.grid(row=1,column=1,sticky='')
                        
        
        self.fr_game_center.wait_variable(some_var16)
        
        return(round2_entry)
        
    ############## gui_round2_card_entry() end ######################################
    
    def gui_round2_trump_call_instance(self,turn_index):
        """
        This method deals with the situation of trump call by a player in round1
        This method is called from round2_follow_logic() in Round_2().
        """
        
        ret_var=tk.IntVar()
        
        # to remove widgets from round1_card_entry
        self.lab_round1_card.grid_forget()
        self.ent_round1_card.grid_forget()
        
        def ret1():
            """
            For the situation when trump is called.
            """
            global ret_val
            ret_val=1
            ret_var.set(1)
            bt_plyr_trmp_choice1.grid_forget()
            bt_plyr_trmp_choice2.grid_forget()
            self.fr_game_center_bot.grid_forget()
            self.but_game_nxt.configure(text='Revealing trump')
            self.but_game_nxt.grid(column=1,row=1)
            
        def ret2():
            """
            For the situation when trum is not called.
            """
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
            # below comments apply to round1 - modify as required
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
        
    ############## gui_round2_trump_call_instance() end #############################
    
    def gui_round2_trump_reveal(self,turn_index,trump_card,highest_bidder_index):
        """
        This method is called from round2_follow_logic() in Round_2()
        The method with the situ when trump is called (by comp hand) and revealed and the 
        trump_card/trump_card2 button is to be revealed i.e. replaced with the form() of trump_card
        """
        
        some_var16b = tk.IntVar()
        
        def trump_reveal():
            self.but_trump_card.configure(text=trump_card.form(),bg='white',fg=trump_card.colour())
            # adding the new card created to list for card buttons, so that when that card is 
            # played, it can be removed from the button list as well like other cards
            self.button_lst_4_crd[highest_bidder_index].append(self.but_trump_card)
            if turn_index:
                # checking since lb_trump_call is not packed for turn_index==0
                lb_trump_call.grid_forget()
            self.but_game_nxt.configure(text='Trump revealed',command=lambda:some_var16b.set(1))
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
        
        self.fr_game_center.wait_variable(some_var16b)
    
    ############## gui_round2_trump_reveal() end ####################################
    
    def gui_round2_summary(self,point_oppo_team,point_player_team,round3_lead_player):
        """
        This method displays the summary at the end of round2, called from round2_play() in Round_2()
        """
    
        some_var17b=tk.IntVar()
        
        # button command
        def round3_lead():
            self.lb_point_oppo_team.grid_forget()
            self.lb_point_player_team.grid_forget()
            self.lb_r3_lead=tk.Label(self.fr_game_center,text='Round 3 starts with: '+round3_lead_player,\
                               font=('GNU Unifont',15))
            self.lb_r3_lead.grid(column=1,row=0,sticky='')
            self.but_game_nxt.configure(text='>>',command=lambda:some_var17b.set(1))
            self.but_game_nxt.focus()
            
        # button command
        def points():
            # using grid_forget with list iteration does not seem to work, it detaches only the last 
            # button in list. Therefore each card in list is given separate name and detached (why?)
            self.but_r2_player_card.grid_forget()
            self.but_r2_right_card.grid_forget()
            self.but_r2_mate_card.grid_forget()
            self.but_r2_left_card.grid_forget()
            # labels for displaying each team points (frame: fr_game_center)
            self.lb_point_oppo_team=tk.Label(self.fr_game_center,text='Oppo_team: '+str(point_oppo_team),\
                                        font=('GNU Unifont',15))
            self.lb_point_player_team=tk.Label(self.fr_game_center,text='Your_team: '+str(point_player_team),\
                                         font=('GNU Unifont',15))
            self.lb_point_oppo_team.grid(column=1,row=0,sticky='')
            self.lb_point_player_team.grid(column=1,row=2,sticky='')
            # clickable next button (frame: fr_game_center)
            self.but_game_nxt.configure(text='>>',command=round3_lead)
            self.but_game_nxt.focus()
        
        # configuring and attaching clickable next button (frame: fr_game_center)
        self.but_game_nxt.configure(text='Points taken',command=points)
        self.but_game_nxt.grid(column=1,row=1,stick='')
        self.but_game_nxt.focus()
                
        self.fr_game_center.wait_variable(some_var17b)
        
    ############## gui_round2_summary() end #########################################
    
    
    #----------------------------- round3 widgets ----------------------------------#
    
    
    def gui_card_played3(self,turn_index,card_played):
        """
        This method is called from the end of round3_lead_logic() and round3_follow_logic() in Round_3().
        trump_revealed status is to be checked and trump_card_button is to be dealt with
        """
        
        some_var14c=tk.IntVar() 

        self.but_r3_played_card_lst=[]
        
        for i in self.button_lst_4_crd[turn_index]:
            if i['text']==card_played.form():
                # this is where the played card is removed from the shown hand(button_lst_4_crd)
                i.pack_forget()
                
                #to remove the widget displaying round3 lead
                self.lb_r3_lead.grid_forget()
                
                # a new button for the played card is formed and attached according to the 
                # turn_index and appended to the list which holds these buttons
                self.but_r3_played_card_lst.append(tk.Button(self.fr_game_center,text=card_played.form(),\
                                          fg=card_played.colour(),font=('GNU Unifont',15)))
                # attaching the buttons based on the turn index. Each button is given a name as detaching 
                # them by accessing through list index doesnot seem to work in gui_round2_summary() method
                if turn_index==0:
                    self.but_r3_player_card=self.but_r3_played_card_lst[-1]
                    self.but_r3_player_card.grid(column=1,row=2,pady=20)
                elif turn_index==1:
                    self.but_r3_right_card=self.but_r3_played_card_lst[-1]
                    self.but_r3_right_card.grid(column=2,row=1,padx=20)
                elif turn_index==2:
                    self.but_r3_mate_card=self.but_r3_played_card_lst[-1]
                    self.but_r3_mate_card.grid(column=1,row=0,pady=20)
                elif turn_index==3:
                    self.but_r3_left_card=self.but_r3_played_card_lst[-1]
                    self.but_r3_left_card.grid(column=0,row=1,padx=20)
                else:
                    print('\nSomething wrong abt turn_index')
        
                    
        self.but_game_nxt.configure(text='>>',command=lambda:some_var14c.set(1))
        self.but_game_nxt.grid(column=1,row=1)
        self.but_game_nxt.focus()
        
        self.fr_game_center.wait_variable(some_var14c)
        
    ############## gui_card_played3() end ############################################
    
    def gui_round3_card_entry(self):
        """
        This method is used whenever the player(not comp) has to input a card, 
        either while leading the round or following in the round
        The method brings up the widgets specific to taking input.
        The method is called from round3_lead_logic() and round3_follow_logic() in Round_3()
        """
        
        some_var16c=tk.IntVar()
        round3_card=tk.StringVar()
        
        def save_round3_card():
            global round3_entry
            round3_entry=round3_card.get()

            self.fr_game_center_bot.grid_forget()

            some_var16c.set(1)
                    
        #to remove the widget displaying round3 lead
        self.lb_r3_lead.grid_forget()
        
        # detaching the clickable next button (frame: fr_game_center)
        self.but_game_nxt.grid_forget()
        
        # attaching the bottom frame in fr_game_center for player input
        self.fr_game_center_bot.grid(column=1,row=2,sticky='NSEW')

        
        # this is nw in a frame inside the cell at (2,1) of the fr_game_center
        self.lab_round3_card=tk.Label(self.fr_game_center_bot,text='Enter card',font=('GNU Unifont',15))
        self.ent_round3_card=tk.Entry(self.fr_game_center_bot,textvariable=round3_card,font=('GNU Unifont',15))
        self.lab_round3_card.grid(row=0,column=0,sticky='')
        self.ent_round3_card.grid(row=0,column=1,sticky='')
        self.ent_round3_card.focus()

        self.but_round3_card=tk.Button(self.fr_game_center_bot,text='Enter', font=('GNU Unifont',15),\
                                 command=save_round3_card)        
        self.but_round3_card.grid(row=1,column=1,sticky='')
                        
        
        self.fr_game_center.wait_variable(some_var16c)
        
        return(round3_entry)
        
    ############## gui_round3_card_entry() end #######################################
    
    def gui_round3_trump_call_instance(self,turn_index):
        """
        This method deals with the situation of trump call by a player in round1
        This method is called from round3_follow_logic() in Round_3().
        """
        
        ret_var=tk.IntVar()
        
        # to remove widgets from round2_card_entry
        # find some other way
        self.lab_round1_card.grid_forget()
        self.ent_round1_card.grid_forget()
        self.lab_round2_card.grid_forget()
        self.ent_round2_card.grid_forget()
        
        def ret1():
            """
            For the situation when trump is called.
            """
            global ret_val
            ret_val=1
            ret_var.set(1)
            bt_plyr_trmp_choice1.grid_forget()
            bt_plyr_trmp_choice2.grid_forget()
            self.fr_game_center_bot.grid_forget()
            self.but_game_nxt.configure(text='Revealing trump')
            self.but_game_nxt.grid(column=1,row=1)
            
        def ret2():
            """
            For the situation when trum is not called.
            """
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
            # below comments apply to round1 - modify as required
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
        
    ############## gui_round3_trump_call_instance() end #############################
    
    def gui_round3_trump_reveal(self,turn_index,trump_card,highest_bidder_index):
        """
        This method is called from round3_follow_logic() in Round_3()
        The method with the situ when trump is called (by comp hand) and revealed and the 
        trump_card/trump_card2 button is to be revealed i.e. replaced with the form() of trump_card
        """
        
        some_var16c = tk.IntVar()
        
        def trump_reveal():
            self.but_trump_card.configure(text=trump_card.form(),bg='white',fg=trump_card.colour())
            # adding the new card created to list for card buttons, so that when that card is 
            # played, it can be removed from the button list as well like other cards
            self.button_lst_4_crd[highest_bidder_index].append(self.but_trump_card)
            if turn_index:
                # checking since lb_trump_call is not packed for turn_index==0
                lb_trump_call.grid_forget()
            self.but_game_nxt.configure(text='Trump revealed',command=lambda:some_var16c.set(1))
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
        
        self.fr_game_center.wait_variable(some_var16c)
    
    ############## gui_round3_trump_reveal() end ####################################
    
    def gui_round3_summary(self,point_oppo_team,point_player_team,round4_lead_player):
        """
        This method displays the summary at the end of round3, called from round3_play() in Round_3()
        """
    
        some_var17c=tk.IntVar()
        
        # button command
        def round4_lead():
            self.lb_point_oppo_team.grid_forget()
            self.lb_point_player_team.grid_forget()
            self.lb_r4_lead=tk.Label(self.fr_game_center,text='Round 4 starts with: '+round4_lead_player,\
                               font=('GNU Unifont',15))
            self.lb_r4_lead.grid(column=1,row=0,sticky='')
            self.but_game_nxt.configure(text='>>',command=lambda:some_var17c.set(1))
            self.but_game_nxt.focus()
            
        # button command
        def points():
            # using grid_forget with list iteration does not seem to work, it detaches only the last 
            # button in list. Therefore each card in list is given separate name and detached (why?)
            self.but_r3_player_card.grid_forget()
            self.but_r3_right_card.grid_forget()
            self.but_r3_mate_card.grid_forget()
            self.but_r3_left_card.grid_forget()
            # labels for displaying each team points (frame: fr_game_center)
            self.lb_point_oppo_team=tk.Label(self.fr_game_center,text='Oppo_team: '+str(point_oppo_team),\
                                        font=('GNU Unifont',15))
            self.lb_point_player_team=tk.Label(self.fr_game_center,text='Your_team: '+str(point_player_team),\
                                         font=('GNU Unifont',15))
            self.lb_point_oppo_team.grid(column=1,row=0,sticky='')
            self.lb_point_player_team.grid(column=1,row=2,sticky='')
            # clickable next button (frame: fr_game_center)
            self.but_game_nxt.configure(text='>>',command=round4_lead)
            self.but_game_nxt.focus()
        
        # configuring and attaching clickable next button (frame: fr_game_center)
        self.but_game_nxt.configure(text='Points taken',command=points)
        self.but_game_nxt.grid(column=1,row=1,stick='')
        self.but_game_nxt.focus()
                
        self.fr_game_center.wait_variable(some_var17c)
        
    ############## gui_round3_summary() end #########################################
    
    
    #----------------------------- round4 widgets ----------------------------------#
    
    
    def gui_card_played4(self,turn_index,card_played):
        """
        This method is called from the end of round4_lead_logic() and round4_follow_logic() in Round_4().
        trump_revealed status is to be checked and trump_card_button is to be dealt with
        """
        
        some_var14d=tk.IntVar() 

        self.but_r4_played_card_lst=[]
        
        for i in self.button_lst_4_crd[turn_index]:
            if i['text']==card_played.form():
                # this is where the played card is removed from the shown hand(button_lst_4_crd)
                i.pack_forget()
                
                #to remove the widget displaying round4 lead
                self.lb_r4_lead.grid_forget()
                
                # a new button for the played card is formed and attached according to the 
                # turn_index and appended to the list which holds these buttons
                self.but_r4_played_card_lst.append(tk.Button(self.fr_game_center,text=card_played.form(),\
                                          fg=card_played.colour(),font=('GNU Unifont',15)))
                # attaching the buttons based on the turn index. Each button is given a name as detaching 
                # them by accessing through list index doesnot seem to work in gui_round3_summary() method
                if turn_index==0:
                    self.but_r4_player_card=self.but_r4_played_card_lst[-1]
                    self.but_r4_player_card.grid(column=1,row=2,pady=20)
                elif turn_index==1:
                    self.but_r4_right_card=self.but_r4_played_card_lst[-1]
                    self.but_r4_right_card.grid(column=2,row=1,padx=20)
                elif turn_index==2:
                    self.but_r4_mate_card=self.but_r4_played_card_lst[-1]
                    self.but_r4_mate_card.grid(column=1,row=0,pady=20)
                elif turn_index==3:
                    self.but_r4_left_card=self.but_r4_played_card_lst[-1]
                    self.but_r4_left_card.grid(column=0,row=1,padx=20)
                else:
                    print('\nSomething wrong abt turn_index')
        
                    
        self.but_game_nxt.configure(text='>>',command=lambda:some_var14d.set(1))
        self.but_game_nxt.grid(column=1,row=1)
        self.but_game_nxt.focus()
        
        self.fr_game_center.wait_variable(some_var14d)
        
    ############## gui_card_played4() end ############################################
    
    def gui_round4_card_entry(self):
        """
        This method is used whenever the player(not comp) has to input a card, 
        either while leading the round or following in the round
        The method brings up the widgets specific to taking input.
        The method is called from round4_lead_logic() and round4_follow_logic() in Round_4()
        """
        
        some_var16d=tk.IntVar()
        round4_card=tk.StringVar()
        
        def save_round4_card():
            global round4_entry
            round4_entry=round4_card.get()

            self.fr_game_center_bot.grid_forget()

            some_var16d.set(1)
                    
        #to remove the widget displaying round4 lead
        self.lb_r4_lead.grid_forget()
        
        # detaching the clickable next button (frame: fr_game_center)
        self.but_game_nxt.grid_forget()
        
        # attaching the bottom frame in fr_game_center for player input
        self.fr_game_center_bot.grid(column=1,row=2,sticky='NSEW')

        
        # this is nw in a frame inside the cell at (2,1) of the fr_game_center
        self.lab_round4_card=tk.Label(self.fr_game_center_bot,text='Enter card',font=('GNU Unifont',15))
        self.ent_round4_card=tk.Entry(self.fr_game_center_bot,textvariable=round4_card,font=('GNU Unifont',15))
        self.lab_round4_card.grid(row=0,column=0,sticky='')
        self.ent_round4_card.grid(row=0,column=1,sticky='')
        self.ent_round4_card.focus()

        self.but_round4_card=tk.Button(self.fr_game_center_bot,text='Enter', font=('GNU Unifont',15),\
                                 command=save_round4_card)        
        self.but_round4_card.grid(row=1,column=1,sticky='')
                        
        
        self.fr_game_center.wait_variable(some_var16d)
        
        return(round4_entry)
        
    ############## gui_round4_card_entry() end #######################################
    
    def gui_round4_trump_call_instance(self,turn_index):
        """
        This method deals with the situation of trump call by a player in round1
        This method is called from round4_follow_logic() in Round_4().
        """
        
        ret_var=tk.IntVar()
        
        # to remove widgets from round1, round2, round3_card_entry
        # find some other way than adding each round labels here
        # this is done so because trump call instance happen only once and it can happen in any round
        # from 1 - 7, so each round currently need the below set of codes removing previous round widgets
        self.lab_round1_card.grid_forget()
        self.ent_round1_card.grid_forget()
        self.lab_round2_card.grid_forget()
        self.ent_round2_card.grid_forget()
        self.lab_round3_card.grid_forget()
        self.ent_round3_card.grid_forget()
        
        def ret1():
            """
            For the situation when trump is called.
            """
            global ret_val
            ret_val=1
            ret_var.set(1)
            bt_plyr_trmp_choice1.grid_forget()
            bt_plyr_trmp_choice2.grid_forget()
            self.fr_game_center_bot.grid_forget()
            self.but_game_nxt.configure(text='Revealing trump')
            self.but_game_nxt.grid(column=1,row=1)
            
        def ret2():
            """
            For the situation when trum is not called.
            """
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
            # below comments apply to round1 - modify as required
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
        
    ############## gui_round4_trump_call_instance() end #############################
    
    def gui_round4_trump_reveal(self,turn_index,trump_card,highest_bidder_index):
        """
        This method is called from round4_follow_logic() in Round_4()
        The method with the situ when trump is called (by comp hand) and revealed and the 
        trump_card/trump_card2 button is to be revealed i.e. replaced with the form() of trump_card
        """
        
        some_var16d = tk.IntVar()
        
        def trump_reveal():
            self.but_trump_card.configure(text=trump_card.form(),bg='white',fg=trump_card.colour())
            # adding the new card created to list for card buttons, so that when that card is 
            # played, it can be removed from the button list as well like other cards
            self.button_lst_4_crd[highest_bidder_index].append(self.but_trump_card)
            if turn_index:
                # checking since lb_trump_call is not packed for turn_index==0
                lb_trump_call.grid_forget()
            self.but_game_nxt.configure(text='Trump revealed',command=lambda:some_var16d.set(1))
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
        
        self.fr_game_center.wait_variable(some_var16d)
    
    ############## gui_round4_trump_reveal() end ####################################
    
    def gui_round4_summary(self,point_oppo_team,point_player_team,round5_lead_player):
        """
        This method displays the summary at the end of round4, called from round4_play() in Round_4()
        """
    
        some_var17d=tk.IntVar()
        
        # button command
        def round5_lead():
            self.lb_point_oppo_team.grid_forget()
            self.lb_point_player_team.grid_forget()
            self.lb_r5_lead=tk.Label(self.fr_game_center,text='Round 5 starts with: '+round5_lead_player,\
                               font=('GNU Unifont',15))
            self.lb_r5_lead.grid(column=1,row=0,sticky='')
            self.but_game_nxt.configure(text='>>',command=lambda:some_var17d.set(1))
            self.but_game_nxt.focus()
            
        # button command
        def points():
            # using grid_forget with list iteration does not seem to work, it detaches only the last 
            # button in list. Therefore each card in list is given separate name and detached (why?)
            self.but_r4_player_card.grid_forget()
            self.but_r4_right_card.grid_forget()
            self.but_r4_mate_card.grid_forget()
            self.but_r4_left_card.grid_forget()
            # labels for displaying each team points (frame: fr_game_center)
            self.lb_point_oppo_team=tk.Label(self.fr_game_center,text='Oppo_team: '+str(point_oppo_team),\
                                        font=('GNU Unifont',15))
            self.lb_point_player_team=tk.Label(self.fr_game_center,text='Your_team: '+str(point_player_team),\
                                         font=('GNU Unifont',15))
            self.lb_point_oppo_team.grid(column=1,row=0,sticky='')
            self.lb_point_player_team.grid(column=1,row=2,sticky='')
            # clickable next button (frame: fr_game_center)
            self.but_game_nxt.configure(text='>>',command=round5_lead)
            self.but_game_nxt.focus()
        
        # configuring and attaching clickable next button (frame: fr_game_center)
        self.but_game_nxt.configure(text='Points taken',command=points)
        self.but_game_nxt.grid(column=1,row=1,stick='')
        self.but_game_nxt.focus()
                
        self.fr_game_center.wait_variable(some_var17d)
        
    ############## gui_round4_summary() end #########################################
    
    
    #----------------------------- round5 widgets ----------------------------------#
    
    
    def gui_card_played5(self,turn_index,card_played):
        """
        This method is called from the end of round5_lead_logic() and round5_follow_logic() in Round_5().
        trump_revealed status is to be checked and trump_card_button is to be dealt with
        """
        
        some_var14e=tk.IntVar() 

        self.but_r5_played_card_lst=[]
        
        for i in self.button_lst_4_crd[turn_index]:
            if i['text']==card_played.form():
                # this is where the played card is removed from the shown hand(button_lst_4_crd)
                i.pack_forget()
                
                #to remove the widget displaying round5 lead
                self.lb_r5_lead.grid_forget()
                
                # a new button for the played card is formed and attached according to the 
                # turn_index and appended to the list which holds these buttons
                self.but_r5_played_card_lst.append(tk.Button(self.fr_game_center,text=card_played.form(),\
                                          fg=card_played.colour(),font=('GNU Unifont',15)))
                # attaching the buttons based on the turn index. Each button is given a name as detaching 
                # them by accessing through list index doesnot seem to work in gui_round5_summary() method
                if turn_index==0:
                    self.but_r5_player_card=self.but_r5_played_card_lst[-1]
                    self.but_r5_player_card.grid(column=1,row=2,pady=20)
                elif turn_index==1:
                    self.but_r5_right_card=self.but_r5_played_card_lst[-1]
                    self.but_r5_right_card.grid(column=2,row=1,padx=20)
                elif turn_index==2:
                    self.but_r5_mate_card=self.but_r5_played_card_lst[-1]
                    self.but_r5_mate_card.grid(column=1,row=0,pady=20)
                elif turn_index==3:
                    self.but_r5_left_card=self.but_r5_played_card_lst[-1]
                    self.but_r5_left_card.grid(column=0,row=1,padx=20)
                else:
                    print('\nSomething wrong abt turn_index')
        
                    
        self.but_game_nxt.configure(text='>>',command=lambda:some_var14e.set(1))
        self.but_game_nxt.grid(column=1,row=1)
        self.but_game_nxt.focus()
        
        self.fr_game_center.wait_variable(some_var14e)
        
    ############## gui_card_played5() end ############################################
    
    def gui_round5_card_entry(self):
        """
        This method is used whenever the player(not comp) has to input a card, 
        either while leading the round or following in the round
        The method brings up the widgets specific to taking input.
        The method is called from round5_lead_logic() and round5_follow_logic() in Round_5()
        """
        
        some_var16e=tk.IntVar()
        round5_card=tk.StringVar()
        
        def save_round5_card():
            global round5_entry
            round5_entry=round5_card.get()

            self.fr_game_center_bot.grid_forget()

            some_var16e.set(1)
                    
        #to remove the widget displaying round5 lead
        self.lb_r5_lead.grid_forget()
        
        # detaching the clickable next button (frame: fr_game_center)
        self.but_game_nxt.grid_forget()
        
        # attaching the bottom frame in fr_game_center for player input
        self.fr_game_center_bot.grid(column=1,row=2,sticky='NSEW')

        
        # this is nw in a frame inside the cell at (2,1) of the fr_game_center
        self.lab_round5_card=tk.Label(self.fr_game_center_bot,text='Enter card',font=('GNU Unifont',15))
        self.ent_round5_card=tk.Entry(self.fr_game_center_bot,textvariable=round5_card,font=('GNU Unifont',15))
        self.lab_round5_card.grid(row=0,column=0,sticky='')
        self.ent_round5_card.grid(row=0,column=1,sticky='')
        self.ent_round5_card.focus()

        self.but_round5_card=tk.Button(self.fr_game_center_bot,text='Enter', font=('GNU Unifont',15),\
                                 command=save_round5_card)        
        self.but_round5_card.grid(row=1,column=1,sticky='')
                        
        
        self.fr_game_center.wait_variable(some_var16e)
        
        return(round5_entry)
        
    ############## gui_round5_card_entry() end #######################################
    
    def gui_round5_trump_call_instance(self,turn_index):
        """
        This method deals with the situation of trump call by a player in round1
        This method is called from round5_follow_logic() in Round_5().
        """
        
        ret_var=tk.IntVar()
        
        # to remove widgets from round1, round2, round3, round4_card_entry
        # find some other way than adding each round labels here
        # this is done so because trump call instance happen only once and it can happen in any round
        # from 1 - 7, so each round currently need the below set of codes removing previous round widgets
        self.lab_round1_card.grid_forget()
        self.ent_round1_card.grid_forget()
        self.lab_round2_card.grid_forget()
        self.ent_round2_card.grid_forget()
        self.lab_round3_card.grid_forget()
        self.ent_round3_card.grid_forget()
        self.lab_round4_card.grid_forget()
        self.ent_round4_card.grid_forget()
        
        def ret1():
            """
            For the situation when trump is called.
            """
            global ret_val
            ret_val=1
            ret_var.set(1)
            bt_plyr_trmp_choice1.grid_forget()
            bt_plyr_trmp_choice2.grid_forget()
            self.fr_game_center_bot.grid_forget()
            self.but_game_nxt.configure(text='Revealing trump')
            self.but_game_nxt.grid(column=1,row=1)
            
        def ret2():
            """
            For the situation when trum is not called.
            """
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
            # below comments apply to round1 - modify as required
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
        
    ############## gui_round5_trump_call_instance() end ##############################
    
    def gui_round5_trump_reveal(self,turn_index,trump_card,highest_bidder_index):
        """
        This method is called from round5_follow_logic() in Round_5()
        The method with the situ when trump is called (by comp hand) and revealed and the 
        trump_card/trump_card2 button is to be revealed i.e. replaced with the form() of trump_card
        """
        
        some_var16e = tk.IntVar()
        
        def trump_reveal():
            self.but_trump_card.configure(text=trump_card.form(),bg='white',fg=trump_card.colour())
            # adding the new card created to list for card buttons, so that when that card is 
            # played, it can be removed from the button list as well like other cards
            self.button_lst_4_crd[highest_bidder_index].append(self.but_trump_card)
            if turn_index:
                # checking since lb_trump_call is not packed for turn_index==0
                lb_trump_call.grid_forget()
            self.but_game_nxt.configure(text='Trump revealed',command=lambda:some_var16e.set(1))
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
        
        self.fr_game_center.wait_variable(some_var16e)
    
    ############## gui_round5_trump_reveal() end #####################################
    
    def gui_round5_summary(self,point_oppo_team,point_player_team,round6_lead_player):
        """
        This method displays the summary at the end of round5, called from round5_play() in Round_5()
        """
    
        some_var17e=tk.IntVar()
        
        # button command
        def round6_lead():
            self.lb_point_oppo_team.grid_forget()
            self.lb_point_player_team.grid_forget()
            self.lb_r6_lead=tk.Label(self.fr_game_center,text='Round 6 starts with: '+round6_lead_player,\
                               font=('GNU Unifont',15))
            self.lb_r6_lead.grid(column=1,row=0,sticky='')
            self.but_game_nxt.configure(text='>>',command=lambda:some_var17e.set(1))
            self.but_game_nxt.focus()
            
        # button command
        def points():
            # using grid_forget with list iteration does not seem to work, it detaches only the last 
            # button in list. Therefore each card in list is given separate name and detached (why?)
            self.but_r5_player_card.grid_forget()
            self.but_r5_right_card.grid_forget()
            self.but_r5_mate_card.grid_forget()
            self.but_r5_left_card.grid_forget()
            # labels for displaying each team points (frame: fr_game_center)
            self.lb_point_oppo_team=tk.Label(self.fr_game_center,text='Oppo_team: '+str(point_oppo_team),\
                                        font=('GNU Unifont',15))
            self.lb_point_player_team=tk.Label(self.fr_game_center,text='Your_team: '+str(point_player_team),\
                                         font=('GNU Unifont',15))
            self.lb_point_oppo_team.grid(column=1,row=0,sticky='')
            self.lb_point_player_team.grid(column=1,row=2,sticky='')
            # clickable next button (frame: fr_game_center)
            self.but_game_nxt.configure(text='>>',command=round6_lead)
            self.but_game_nxt.focus()
        
        # configuring and attaching clickable next button (frame: fr_game_center)
        self.but_game_nxt.configure(text='Points taken',command=points)
        self.but_game_nxt.grid(column=1,row=1,stick='')
        self.but_game_nxt.focus()
                
        self.fr_game_center.wait_variable(some_var17e)
        
    ############## gui_round5_summary() end #########################################
    
    
    #----------------------------- round6 widgets ----------------------------------#
    
    
    def gui_card_played6(self,turn_index,card_played):
        """
        This method is called from the end of round6_lead_logic() and round6_follow_logic() in Round_6().
        trump_revealed status is to be checked and trump_card_button is to be dealt with
        """
        
        some_var14f=tk.IntVar() 

        self.but_r6_played_card_lst=[]
        
        for i in self.button_lst_4_crd[turn_index]:
            if i['text']==card_played.form():
                # this is where the played card is removed from the shown hand(button_lst_4_crd)
                i.pack_forget()
                
                #to remove the widget displaying round6 lead
                self.lb_r6_lead.grid_forget()
                
                # a new button for the played card is formed and attached according to the 
                # turn_index and appended to the list which holds these buttons
                self.but_r6_played_card_lst.append(tk.Button(self.fr_game_center,text=card_played.form(),\
                                          fg=card_played.colour(),font=('GNU Unifont',15)))
                # attaching the buttons based on the turn index. Each button is given a name as detaching 
                # them by accessing through list index doesnot seem to work in gui_round5_summary() method
                if turn_index==0:
                    self.but_r6_player_card=self.but_r6_played_card_lst[-1]
                    self.but_r6_player_card.grid(column=1,row=2,pady=20)
                elif turn_index==1:
                    self.but_r6_right_card=self.but_r6_played_card_lst[-1]
                    self.but_r6_right_card.grid(column=2,row=1,padx=20)
                elif turn_index==2:
                    self.but_r6_mate_card=self.but_r6_played_card_lst[-1]
                    self.but_r6_mate_card.grid(column=1,row=0,pady=20)
                elif turn_index==3:
                    self.but_r6_left_card=self.but_r6_played_card_lst[-1]
                    self.but_r6_left_card.grid(column=0,row=1,padx=20)
                else:
                    print('\nSomething wrong abt turn_index')
        
                    
        self.but_game_nxt.configure(text='>>',command=lambda:some_var14f.set(1))
        self.but_game_nxt.grid(column=1,row=1)
        self.but_game_nxt.focus()
        
        self.fr_game_center.wait_variable(some_var14f)
        
    ############## gui_card_played6() end ############################################
    
    def gui_round6_card_entry(self):
        """
        This method is used whenever the player(not comp) has to input a card, 
        either while leading the round or following in the round
        The method brings up the widgets specific to taking input.
        The method is called from round6_lead_logic() and round6_follow_logic() in Round_6()
        """
        
        some_var16f=tk.IntVar()
        round6_card=tk.StringVar()
        
        def save_round6_card():
            global round6_entry
            round6_entry=round6_card.get()

            self.fr_game_center_bot.grid_forget()

            some_var16f.set(1)
                    
        #to remove the widget displaying round6 lead
        self.lb_r6_lead.grid_forget()
        
        # detaching the clickable next button (frame: fr_game_center)
        self.but_game_nxt.grid_forget()
        
        # attaching the bottom frame in fr_game_center for player input
        self.fr_game_center_bot.grid(column=1,row=2,sticky='NSEW')

        
        # this is nw in a frame inside the cell at (2,1) of the fr_game_center
        self.lab_round6_card=tk.Label(self.fr_game_center_bot,text='Enter card',font=('GNU Unifont',15))
        self.ent_round6_card=tk.Entry(self.fr_game_center_bot,textvariable=round6_card,font=('GNU Unifont',15))
        self.lab_round6_card.grid(row=0,column=0,sticky='')
        self.ent_round6_card.grid(row=0,column=1,sticky='')
        self.ent_round6_card.focus()

        self.but_round6_card=tk.Button(self.fr_game_center_bot,text='Enter', font=('GNU Unifont',15),\
                                 command=save_round6_card)        
        self.but_round6_card.grid(row=1,column=1,sticky='')
                        
        
        self.fr_game_center.wait_variable(some_var16f)
        
        return(round6_entry)
        
    ############## gui_round6_card_entry() end #######################################
    
    def gui_round6_trump_call_instance(self,turn_index):
        """
        This method deals with the situation of trump call by a player in round1
        This method is called from round6_follow_logic() in Round_6().
        """
        
        ret_var=tk.IntVar()
        
        # to remove widgets from round1, round2, round3, round4, round5_card_entry
        # find some other way than adding each round labels here
        # this is done so because trump call instance happen only once and it can happen in any round
        # from 1 - 7, so each round currently need the below set of codes removing previous round widgets
        self.lab_round1_card.grid_forget()
        self.ent_round1_card.grid_forget()
        self.lab_round2_card.grid_forget()
        self.ent_round2_card.grid_forget()
        self.lab_round3_card.grid_forget()
        self.ent_round3_card.grid_forget()
        self.lab_round4_card.grid_forget()
        self.ent_round4_card.grid_forget()
        self.lab_round5_card.grid_forget()
        self.ent_round5_card.grid_forget()
        
        def ret1():
            """
            For the situation when trump is called.
            """
            global ret_val
            ret_val=1
            ret_var.set(1)
            bt_plyr_trmp_choice1.grid_forget()
            bt_plyr_trmp_choice2.grid_forget()
            self.fr_game_center_bot.grid_forget()
            self.but_game_nxt.configure(text='Revealing trump')
            self.but_game_nxt.grid(column=1,row=1)
            
        def ret2():
            """
            For the situation when trum is not called.
            """
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
            # below comments apply to round1 - modify as required
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
        
    ############## gui_round6_trump_call_instance() end ##############################
    
    def gui_round6_trump_reveal(self,turn_index,trump_card,highest_bidder_index):
        """
        This method is called from round6_follow_logic() in Round_6()
        The method with the situ when trump is called (by comp hand) and revealed and the 
        trump_card/trump_card2 button is to be revealed i.e. replaced with the form() of trump_card
        """
        
        some_var16f = tk.IntVar()
        
        def trump_reveal():
            self.but_trump_card.configure(text=trump_card.form(),bg='white',fg=trump_card.colour())
            # adding the new card created to list for card buttons, so that when that card is 
            # played, it can be removed from the button list as well like other cards
            self.button_lst_4_crd[highest_bidder_index].append(self.but_trump_card)
            if turn_index:
                # checking since lb_trump_call is not packed for turn_index==0
                lb_trump_call.grid_forget()
            self.but_game_nxt.configure(text='Trump revealed',command=lambda:some_var16f.set(1))
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
        
        self.fr_game_center.wait_variable(some_var16f)
    
    ############## gui_round6_trump_reveal() end #####################################
    
    def gui_round6_summary(self,point_oppo_team,point_player_team,round7_lead_player):
        """
        This method displays the summary at the end of round6, called from round6_play() in Round_6()
        """
    
        some_var17f=tk.IntVar()
        
        # button command
        def round7_lead():
            self.lb_point_oppo_team.grid_forget()
            self.lb_point_player_team.grid_forget()
            self.lb_r7_lead=tk.Label(self.fr_game_center,text='Round 7 starts with: '+round7_lead_player,\
                               font=('GNU Unifont',15))
            self.lb_r7_lead.grid(column=1,row=0,sticky='')
            self.but_game_nxt.configure(text='>>',command=lambda:some_var17f.set(1))
            self.but_game_nxt.focus()
            
        # button command
        def points():
            # using grid_forget with list iteration does not seem to work, it detaches only the last 
            # button in list. Therefore each card in list is given separate name and detached (why?)
            self.but_r6_player_card.grid_forget()
            self.but_r6_right_card.grid_forget()
            self.but_r6_mate_card.grid_forget()
            self.but_r6_left_card.grid_forget()
            # labels for displaying each team points (frame: fr_game_center)
            self.lb_point_oppo_team=tk.Label(self.fr_game_center,text='Oppo_team: '+str(point_oppo_team),\
                                        font=('GNU Unifont',15))
            self.lb_point_player_team=tk.Label(self.fr_game_center,text='Your_team: '+str(point_player_team),\
                                         font=('GNU Unifont',15))
            self.lb_point_oppo_team.grid(column=1,row=0,sticky='')
            self.lb_point_player_team.grid(column=1,row=2,sticky='')
            # clickable next button (frame: fr_game_center)
            self.but_game_nxt.configure(text='>>',command=round7_lead)
            self.but_game_nxt.focus()
        
        # configuring and attaching clickable next button (frame: fr_game_center)
        self.but_game_nxt.configure(text='Points taken',command=points)
        self.but_game_nxt.grid(column=1,row=1,stick='')
        self.but_game_nxt.focus()
                
        self.fr_game_center.wait_variable(some_var17f)
        
    ############## gui_round6_summary() end ##########################################
    
    
    #----------------------------- round7 widgets ----------------------------------#
    
    
    
    
