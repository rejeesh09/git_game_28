#####################################################################
from cards import Cards ## to make card objects inside Deck()
import pickle ## to dump deal_lst to txt file and load for debugging
import numpy as np 
# all three modules above are used in the obj_deal() method in Deck() class, could have been called inside
# the method itself. But done here just to make all imports explicit within each module

import tkinter as tk
# for gui
#####################################################################
####################################################################
class Deck():
    def __init__(self,dictn_of_card_objects,tkntr_rt):
        # the argument is a dictionary of 32 card objects created separately using the Cards() class
        #1.###### var1
        #d1)
        self.card_obj=dictn_of_card_objects
        #d2)
        self.suit=['spade','hearts','clubs','diamonds']
        #d3)
        self.suit_inp=['s','h','c','d']
        self.suit_dictn={'spade':0,'hearts':1,'clubs':2,'diamonds':3}
        #d4)
        self.suit_uni=['\u2660','\u2665','\u2663','\u2666'] #overriding?
        #d5)
        self.red_begin='\033[31m'
        #d6)
        self.red_end='\033[0m' # or normal begin
        #d7)
        self.rank=['7','8','Q','K','10','A','9','J'] #overriding?
        
        # making a list for checking if input is legal
        #d8)
        self.legal_card_lst=[]
        for z in self.suit_inp:
            self.legal_card_lst.extend([x+z for x in self.rank])

        # making the game deck of 32 cards # overriding?
        #d9)
        self.cards_no_colr=[]
        for y in self.suit_uni:
            self.cards_no_colr.extend([x+y for x in self.rank])

        # making a dictionary for ordering hands based on dictionary value
        # {'7♠': 0, '8♠': 1, 'Q♠': 2,..'9♦': 30, 'J♦': 31}
        # dictionary with objects
        #2.###### var2
        #d10)
        self.obj_dictn_of_deck_with_value=dict([self.card_obj[card_index],card_index] \
                                              for card_index in range(32))
        
        # making a dictionary of points 
        # these points to be used for comparison and have to be 
        # converted to int before adding/counting points in a round
        #d11)
        self.points_lst_8=[0.01,0.02,0.03,0.04,1.00,1.01,2.00,3.00]
        #d12)
        self.points_lst_32=[]
        for i in range(4):
            self.points_lst_32.extend(self.points_lst_8)
        
        # {'7♠': 0.01, '8♠': 0.02,...'9♦': 2.0, 'J♦': 3.0}
        # dictionary with objects
        #3.###### var3
        #d13)
        self.obj_dictn_of_card_points=dict([self.card_obj[i],self.points_lst_32[i]] for i in range(32))
        
        # player names
        #d14)
        
        # gui window for taking input
        self.rt=tkntr_rt
#         self.rt.geometry('1600x900')
#         self.rt.title('Game window')
#         self.rt.configure(bg='black')
        
        fr1=tk.Frame(self.rt)
        fr1.pack(side=tk.TOP, pady=300)

        name_var=tk.StringVar()
        self.name=name_var.get()
        wait_var=tk.IntVar()
        
        def clear_fr1():
            fr1.pack_forget()
            wait_var.set(1)
#             lab2.pack_forget()
#             but2.pack_forget()
#             lab3=tk.Label(fr1,text="Close and continue to python prompt",font=('GNU Unifont',30))
#             lab3.pack(side=tk.TOP)
#             but3=tk.Button(fr1,text="Close",font=('GNU Unifont',30),command=self.rt.destroy)
#             but3.pack(side=tk.TOP)

        def save_name():
            global name, lab2, but2
            name=name_var.get()
            
            lab1.grid_forget()
            ent1.grid_forget()
            but1.grid_forget()
            
            lab2=tk.Label(fr1,text='Name entered is: '+name,font=('GNU Unifont',30))
            but2=tk.Button(fr1, text='Continue',font=('GNU Unifont',30),command=clear_fr1)
            lab2.pack()
            but2.pack()
        
        lab1=tk.Label(fr1,text='Name:',font=('GNU Unifont',20))
        ent1=tk.Entry(fr1,textvariable=name_var,font=('GNU Unifont',20))
        but1=tk.Button(fr1,text='Enter', font=('GNU Unifont',20),command=save_name)

        lab1.grid(row=0,column=0,sticky='')
        ent1.grid(row=0,column=1,sticky='')
        but1.grid(row=1,column=1,sticky='')
        
        fr1.wait_variable(wait_var)
        
#         self.rt.mainloop()
        #############################
        
        self.player_name=name.capitalize()

#         self.player_name=input('\nEnter your name: ').capitalize()
        while (not self.player_name) or (self.player_name.isspace()):
            print('\nPlease enter atleast one character for name ')
            self.player_name=input('\nEnter you name: ').capitalize()
        #4.###### var4
        #d15)
        self.players_lst=[self.player_name,'Oppo_right','Mate','Oppo_left']
        
    ##################################################################
    # for dealing out the four hands object-based
    #D1)
    def obj_deal(self,hold,custom_deal):
        self.cards_copy=self.cards_no_colr.copy()
        if not (hold or custom_deal):
            # gui message
            
#             fr2=tk.Frame(self.rt)
#             fr2.pack(side=tk.TOP, pady=300)
            
#             lab3=tk.Label(fr2, text='No hold or custom',font=('GNU Unicode',30))
#             lab3.pack()
            
            #############
            print('\nNo hold or no custom')
            #5.########## var5
            self.obj_deal_lst=[[],[],[],[]]
            for i in range(32):
                if i//8==0:
                    d=np.random.choice(self.cards_copy)
                    d2=Cards(d)
                    self.obj_deal_lst[0].append(d2)
                    self.cards_copy.remove(d)
                if i//8==1:
                    d=np.random.choice(self.cards_copy)
                    d2=Cards(d)
                    self.obj_deal_lst[1].append(d2)
                    self.cards_copy.remove(d)
                if i//8==2:
                    d=np.random.choice(self.cards_copy)
                    d2=Cards(d)
                    self.obj_deal_lst[2].append(d2)
                    self.cards_copy.remove(d)
                if i//8==3:
                    d=np.random.choice(self.cards_copy)
                    d2=Cards(d)
                    self.obj_deal_lst[3].append(d2)
                    self.cards_copy.remove(d)
            
            # handling probable redeal situations except no trump
            # no point in a hand, all J's in one hand and all cards of a suit in a hand
            # haven't really tested for errors here
            j_count=0
            self.suit_count=0
            redeal_count=0
            
            for h in range(4):
                if sum(int(i.point()) for i in self.obj_deal_lst[h]) == 0:
                    print("\n{} has no points, redealing".format(self.players_lst[h]))
                    redeal_count+=1
                    self.obj_deal(False,False)
                for i in self.obj_deal_lst[h]:
                    if i.rank()=='J':
                        j_count+=1
                if j_count==4:
                    print("\n{} has all J's, redealing".format(self.players_lst[h]))
                    redeal_count+=1
                    self.obj_deal(False,False)
                j_count=0
                
                # to check if any of the hands have all the 8 cards in a suit
                for i in range(7):
                    if self.obj_deal_lst[h][i].suit()==self.obj_deal_lst[h][i+1].suit():
                        self.suit_count+=1
                if self.suit_count==8:
                    print('\n{} has all cards of the suit {}'.format(self.players_lst[h],\
                                                                self.obj_deal_lst[h][0].suit()))
                    redeal_count+=1
                    self.obj_deal(False)
                self.suit_count=0
                    
                    
            if not redeal_count:
                
                #gui message
                
#                 lab4=tk.Label(fr2,text='All hands are good to go',font=('GNU Unicode',30))
#                 lab4.pack()
                
#                 def clear_fr2():
#                     fr2.pack_forget()
                
#                 but3=tk.Button(fr2,text='Deal',font=('GNU Unicode',30),command=clear_fr2)
#                 but3.pack()
                
                ############
                print('\nAll hands are good to go')

                # saving a copy for debugging 
                f=open("last_deal.txt","wb")
                pickle.dump(self.obj_deal_lst,f)
                f.close()
        elif custom_deal:
            f=open("custom_dealt_hand.txt","rb")
            self.obj_deal_lst=pickle.load(f)
            f.close()
        else:
            f=open("last_deal.txt","rb")
            self.obj_deal_lst=pickle.load(f)
            f.close()
    
    ##################################################################          
    # for sorting half the hand, object based
    #D2)
    def obj_sort_half_hands(self):
        #5.b.#### var5.b
        self.obj_half_deal_lst=[]
        for ih1 in self.obj_deal_lst:
            self.obj_half_deal_lst.append(ih1[0:4])
        for kh in range(4):
            for ih in range(4):                
                for jh in range(ih+1,4):
                    q2 = self.obj_half_deal_lst[kh][jh]
                    q1 = self.obj_half_deal_lst[kh][ih]
                    if q1.value() > q2.value():
                        self.obj_half_deal_lst[kh].insert(ih,q2)
                        self.obj_half_deal_lst[kh].pop(jh+1)
                    else:
                        continue
    
    ##################################################################
    # for displaying half hand
    #D3)
    def obj_display_half_hands(self,tkntr_rt):
        
        # gui window display
        self.rt=tkntr_rt
        fr_0=tk.Frame(self.rt,background='DeepSkyBlue4')
        fr_0.pack(side=tk.BOTTOM)

        fr_1=tk.Frame(self.rt,background='DeepSkyBlue4')
        fr_1.pack(side=tk.RIGHT)

        fr_2=tk.Frame(self.rt,background='DeepSkyBlue4')
        fr_2.pack(side=tk.TOP)

        fr_3=tk.Frame(self.rt,background='DeepSkyBlue4')
        fr_3.pack(side=tk.LEFT)

        fr_lst=[fr_0,fr_1,fr_2,fr_3]

        button_lst_4_nme=[]
        for i in range(4):
            button_lst_4_nme.append(tk.Button(fr_lst[i],text=self.players_lst[i],font=('GNU Unifont',15)))
            button_lst_4_nme[i].pack(side=tk.BOTTOM,pady=10)


        button_lst_4_crd=[[],[],[],[]]
        for j in range(4):
            for i in range(4):
                k=self.obj_half_deal_lst[j][i]
                button_lst_4_crd[j].append(tk.Button(fr_lst[j],text=k.form(),fg=k.colour(),font=('GNU Unifont',15)))
                button_lst_4_crd[j][i].pack(side=tk.LEFT)

        some_var=tk.IntVar()
        
        fr_center=tk.Frame(self.rt,background='black')
        fr_center.pack()
        but_cen=tk.Button(fr_center,text='Continue',command=lambda:some_var.set(1))
        but_cen.pack(side=tk.TOP,pady=300)
        
        fr_center.wait_variable(some_var)
#         self.rt.mainloop()
        
        ####################
        
        print('\n')
        for indxx in range(4):
            print("{}: ".format(self.players_lst[indxx]))
            for itemm in self.obj_half_deal_lst[indxx]:
                print(itemm.show(),end=' ')
            print("\n")

    ##################################################################
    # for sorting the hands dealt, object based
    #D4)
    def obj_sort_hands(self):
        #5.c.#### var5.c
        self.obj_deal_lst_copy=[dl[:] for dl in self.obj_deal_lst]
        # use the above method or deepcopy from copy for compound objects, normal copies are just pointers 
        # to the original compound object (list/dict/tuple...)
        # obj_deal_lst is the original dealt hand and obj_deal_lst_copy is the sorted hand
        for k in range(4):
            for i in range(8):                
                for j in range(i+1,8):
                    q2 = self.obj_deal_lst_copy[k][j]
                    q1 = self.obj_deal_lst_copy[k][i]
                    if q1.value() > q2.value():
                        self.obj_deal_lst_copy[k].insert(i,q2)
                        self.obj_deal_lst_copy[k].pop(j+1)
                    else:
                        continue
                
        # to keep a list that doesn't change
        self.obj_deal_lst_sorted=[sr[:] for sr in self.obj_deal_lst_copy]
        # every time a card is played, it will be removed from obj_deal_lst_copy and 
        # obj_dictn_of_cards_grouped
        
        # dictionary of players with their hands
        #6.###### var6
        self.obj_dictn_of_players_and_hand = dict([self.players_lst[i],\
                                                   self.obj_deal_lst_sorted[i]] for i in range(4))

    ##################################################################          
    # for displaying the hands object based
    #D5)
    def obj_display_hands(self,show_updated):
        if not show_updated:
            print('\n')
            for key in self.obj_dictn_of_players_and_hand:
                print("{}: ".format(key))
                for value in self.obj_dictn_of_players_and_hand[key]:
                    print(value.show(),end=' ')
                print("\n")
        else:
        # if show_updated value is True, then display without already played cards and even trump removed if
        # trump card is not yet revealed - to be used for successive rounds
            print('\n')
            for key in range(4):
                print("{}: ".format(self.players_lst[key]))
                for carrd in self.obj_deal_lst_copy[key]:
                # deal_lst_copy is the updated list of cards in hand after each round
                    print(carrd.show(),end=' ')
                print("\n")
    
    ##################################################################
    # making induvidual dictionaries of grouped cards for Oppo_right, Mate and Oppo_left
    #D6)
    def obj_induvidual_dictns(self):
        #7.###### var7
        self.obj_dictn_of_cards_grouped=dict()
        # for printing out the dictionary
        self.dictn_of_cards_grouped=dict()
        
#         for i in range(1,4):
        for i in range(4):
            self.obj_spade_cards=[]
            self.obj_hearts_cards=[]
            self.obj_clubs_cards=[]
            self.obj_diamonds_cards=[]
            self.spade_cards=[]
            self.hearts_cards=[]
            self.clubs_cards=[]
            self.diamonds_cards=[]
            for k in self.obj_deal_lst_copy[i]:
                if k.suit()=='spade':
                    self.obj_spade_cards.append(k)
                    self.spade_cards.append(k.form())
                if k.suit()=='hearts':
                    self.obj_hearts_cards.append(k)
                    self.hearts_cards.append(k.form())
                if k.suit()=='clubs':
                    self.obj_clubs_cards.append(k)
                    self.clubs_cards.append(k.form())
                if k.suit()=='diamonds':
                    self.obj_diamonds_cards.append(k)
                    self.diamonds_cards.append(k.form())
            self.obj_induv_dictn={0:self.obj_spade_cards,1:self.obj_hearts_cards,2:self.obj_clubs_cards,\
                              3:self.obj_diamonds_cards}
            self.induv_dictn={0:self.spade_cards,1:self.hearts_cards,\
                                   2:self.clubs_cards,3:self.diamonds_cards}
            self.obj_dictn_of_cards_grouped.update({i:self.obj_induv_dictn})
            self.dictn_of_cards_grouped.update({i:self.induv_dictn})
            
    ##################################################################
    # making half dictionaries of grouped cards for Oppo_right, Mate and Oppo_left
    #D7)
    def obj_half_dictns(self):
        #7.b.###### var7
        self.obj_half_dictn_of_cards_grouped=dict()
        
#         for i in range(1,4):
        for i in range(4):
            self.obj_spade_cards_half=[]
            self.obj_hearts_cards_half=[]
            self.obj_clubs_cards_half=[]
            self.obj_diamonds_cards_half=[]
            for k in self.obj_half_deal_lst[i]:
                if k.suit()=='spade':
                    self.obj_spade_cards_half.append(k)
                if k.suit()=='hearts':
                    self.obj_hearts_cards_half.append(k)
                if k.suit()=='clubs':
                    self.obj_clubs_cards_half.append(k)
                if k.suit()=='diamonds':
                    self.obj_diamonds_cards_half.append(k)
            self.obj_induv_dictn_half={0:self.obj_spade_cards_half,1:self.obj_hearts_cards_half,\
                            2:self.obj_clubs_cards_half,3:self.obj_diamonds_cards_half}
            self.obj_half_dictn_of_cards_grouped.update({i:self.obj_induv_dictn_half})

