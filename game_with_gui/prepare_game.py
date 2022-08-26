#######################################################################
from cards import Cards
# importing the class - Cards()

# making the game deck of 32 cards
# ['7♠', '8♠','Q♠',...,'9♦','J♦']
# spade-\u2660, hearts-\u2665, clubs-\u2663, diamonds-\u2666
suit_uni=['\u2660','\u2665','\u2663','\u2666']
rank=['7','8','Q','K','10','A','9','J']
        
cards_no_colr=[]
for y in suit_uni:
    cards_no_colr.extend([x+y for x in rank])

# dictn_of_cards is a dictionary of 32 Cards objects,
# dictn_of_cards = {0: <__main__.Cards object at ..>,.., 32: 31: <__main__.Cards object at..}
i=range(32)
dictn_of_cards=dict.fromkeys(i,'')
for j in range(32):
    dictn_of_cards[j]=Cards(cards_no_colr[j])
#######################################################################
#######################################################################
from deck import Deck
# importing the class - Deck()
# Each module needs to have all the classes that are being explicitly used, 
# available in their own 'namespace'
#######################################################################
#######################################################################
import numpy as np
import pickle
# both the above modules are used in the bid_half_hand() method in Prepare_game()

# import tkinter as tk
# for gui
# import widget_manager as wm
# widget_manager is a module to collect all gui related code in one place
# search for the term unfolder using the find and replace option under the edit tab(f in comm mode) and 
# replace it with the same to get all the folded blocks of code unblocked. or else 
# searching using ctl-f will not yield results from the folded blocks
#######################################################################
class Prepare_game(Deck):
    def __init__(self,hold,custom_deal,tkntr_rt):
        # methods from Deck()
        super().__init__(dictn_of_cards,tkntr_rt) #??? in which namespace does dictn_of_cards reside?
        # looks like when doing from prepare_game import Prepare_game, the whole prepare_game.py script 
        # is run first and then the class Prepare_game() is imported from it
        # All the (15*) variables(attributes) in Deck()'s init() are now constructed by the above line
        super().obj_deal(hold,custom_deal)
        super().obj_sort_half_hands()
        super().obj_display_half_hands()
        super().obj_sort_hands()
        super().obj_induvidual_dictns() # makes obj_dictn_of_cards_grouped, which is used 
        #throughout to make decision on card to be played
        super().obj_half_dictns() # makes grouped dictn of half hand
        # super().obj_display_hands(False)
        # obj_display_hands(True/False) is called in the bid_half_hand() method below, after trump is set
        # Pass False as argument to display the original hands and pass True to display hands updated 
        # after the round
        # (6 out of 7) methods of Deck are constructed here
        
        ###############################################################
        #8.###### var8
        #p1)
        self.obj_played_card_lst=[] # this could be cleared after each round
        #p2)
        self.obj_played_card_lst_of_32=[]
        
        #9.###### var9
        #p3)
        self.obj_dictn_of_highest_card_and_turn=dict()
        # this dictionary holds the highest card of the round and the corresponding turn index
        # only the turn_index is actually needed
        self.obj_dictn_of_highest_card_and_turn['suit']=[]
        self.obj_dictn_of_highest_card_and_turn['trump']=[]

        # played card dictionary with player and played card dictionary with suit
        #10.##### var10
        #p4)
        self.obj_dictn_of_played_card_and_player={item:[] for item in self.players_lst}
        #11.##### var11
        #p5)
        self.obj_dictn_of_played_card_and_suit={item.lower():[] for item in self.suit}
        #12.##### var12
        #p6)
        self.point_player_team=0
        #13.##### var13
        #p7)
        self.point_oppo_team=0
        
        #13.2#### var13.2
        #p8)
        self.trump_set=False
        #13.3#### var13.3
        #p9)
        self.trump_revealed=False # this can be used to make decision on calling trump
        #13.4#### var13.4
        #p10)        
        self.trump_played_in_round=False # to check if trump played in round,
        # to be updated when entry added to dictn['trump'] lst
        

    ###################################################################
    # init() end ######################################################
    
    #P1)
    def trump_verify(self,trump,half_hand):
        # only for setting trump card, other checks for an input is done in inp_parse_check
        # checks and converts the trump input to unicode and then to Card object        
        control_count=0
        self.trump=trump
        self.half_hand=half_hand
        self.inp_cpy=self.trump
        self.inp_cpy.strip(" ") # doesn't seem to work
        self.inp_cpy.replace(" ","") # this seems to work only for space inside the string
        ###############################################################
        if self.inp_cpy.capitalize() not in self.legal_card_lst:
            print('\nYou did not enter a valid card')
            self.player_input=input('\nEnter the card rank followed by the first letter of the suit, eg.' 
                +'\n7s or ah or 10d etc.: ').lower()
            self.trump_verify(self.player_input,self.half_hand)
        else:
            if self.inp_cpy[-1]=='s':
                if self.inp_cpy[0]!='1':
                    self.inp_uni=self.inp_cpy[0].upper()+'\u2660'
                else:
                    self.inp_uni=self.inp_cpy[0].upper()+'0'+'\u2660'
            elif self.inp_cpy[-1]=='h':
                if self.inp_cpy[0]!='1':
                    self.inp_uni=self.inp_cpy[0].upper()+'\u2665'
                else:
                    self.inp_uni=self.inp_cpy[0].upper()+'0'+'\u2665'
            elif self.inp_cpy[-1]=='c':
                if self.inp_cpy[0]!='1':
                    self.inp_uni=self.inp_cpy[0].upper()+'\u2663'
                else:
                    self.inp_uni=self.inp_cpy[0].upper()+'0'+'\u2663'
            elif self.inp_cpy[-1]=='d':
                if self.inp_cpy[0]!='1':
                    self.inp_uni=self.inp_cpy[0].upper()+'\u2666'
                else:
                    self.inp_uni=self.inp_cpy[0].upper()+'0'+'\u2666'
        ###############################################################
        # input to object
        self.inp_uni_obj=Cards(self.inp_uni)
        ###############################################################
        # the counter is used since there are instructions in the functions 
        # which come after recursive call
        if self.half_hand:
            if control_count==0:
                if self.inp_uni_obj not in self.obj_half_deal_lst[self.highest_bidder_index]:
                    print('\nEntered card not in hand')
                    self.player_input=input('\nEnter the card rank followed by the first letter of the suit, eg.' 
                        +'\n7s or ah or 10d etc.: ').lower()
                    self.trump_verify(self.player_input,self.half_hand)
                else:
                    control_count+=1
        else:
            if control_count==0:
                if self.inp_uni_obj not in self.obj_deal_lst[self.highest_bidder2_index]:
                    print('\nEntered card not in hand')
                    self.player_input=input('\nEnter the card rank followed by the first letter of the suit, eg.' 
                        +'\n7s or ah or 10d etc.: ').lower()
                    self.trump_verify(self.player_input,self.half_hand)
                else:
                    control_count+=1
        # returns the input, converted to Cards object
        return(self.inp_uni_obj)
    
    ###################################################################
    # trump_verify end ################################################
    
    #P2)
    def bid_half_hand(self,hold,custom_deal):
        
        if not (hold or custom_deal):
        # the value of hold is either True or False depending on whether the last hand is to be 
        # repeated(for debugging pupose)
            self.bid_turn_index=np.random.randint(4)
            # selecting the first turn for bidding, randomly
            self.round1_lead_index=self.bid_turn_index
            # the one who starts the bid, starts/lead the first round. 
            # round1_lead_index will be used in Round_1() class.

            fb=open("last_starting_bid_turn.txt","wb")
            # saving a copy for debugging 
            # opening a file object in write-binary mode
            pickle.dump(self.bid_turn_index,fb)
            fb.close()
        elif custom_deal:
            fb=open("custom_starting_bid_turn.txt","rb")
            # opening a file object in read-binary mode
            self.bid_turn_index=pickle.load(fb)
            self.round1_lead_index=self.bid_turn_index
            fb.close()
        else:
        # i.e. True is passed as the value of argument 'hold', to this method,
        # (i.e. replaying last round - for debugging)
            fb=open("last_starting_bid_turn.txt","rb")
            # opening a file object in read-binary mode
            self.bid_turn_index=pickle.load(fb)
            self.round1_lead_index=self.bid_turn_index
            fb.close()
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^       
        # gui window for bid messages
        # displays the message as to who starts the bid
        self.gui_handle.gui_half_bid_mes(self.players_lst[self.bid_turn_index])
        # calling the appropriate method from widget_manager module using object(self.gui_handle) 
        # created in __init__() of Deck() class
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
#         print('\nStarting bid_turn_index is: ',self.bid_turn_index)
        
        self.bid_value_final=13 # to make sure min starting bid value is 14
        
        self.bid_counter=0
        # the above counter increments after every bid or pass and is used to stop bidding 
        # after two rounds
        self.bid_counter_lst=[0]
        # the above counter list is used to stop bidding if both team mates passes
        
        found=False
        count_2_lst=[]
        # the above list holds the indices of suits with len()==2 for cases 3 and 2
        count_1_lst=[]
        # the above list holds the indices of suits with len()==1 for cases 3 and 2

        while self.bid_counter<8:
            if self.bid_turn_index==0:
            # taking bid input if bid_turn_index==0
            
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                # gui window for taking bid value (now as an entry, better be options of buttons)                
                self.bid_value_inp=self.gui_handle.gui_half_bid_entry()
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                
#                 self.bid_value_inp=input('\nEnter your bid (any non-digit input will be considered as pass): ')
                if self.bid_value_inp.isdigit():
                    self.bid_value=int(self.bid_value_inp)
                    while not (13<self.bid_value<21): # setting 21 limit for half hand bid
                    # this inner while loop is executed when the bid value entered first is a digit but 
                    # not legit. another input is asked for and if the bid value is not legit, 
                    # even the second time, then the min value is set, if mandatory, or the bid_value is 
                    # set to be less than the bid_value_final(equal is also enough). At the end of each run  
                    # of the outer while loop, bid_value is compared with bid_value_final and a decision on
                    # whether the bid has been called or passed is taken
                        self.bid_value_inp=input('\nYou did not enter a legal bid value (14-20). Pls try again: ')
                        if self.bid_value_inp.isdigit():
                            self.bid_value=int(self.bid_value_inp)
                        elif self.bid_counter==0:
                            # minimum call
                            print('\nBid set to 14 as atleast minimum call mandatory in first bid')
                            self.bid_value=14
                        else:
                            # setting the bid_value to be less than the bid_value_final so that at the 
                            # end of the outer while loop, the condition satisfies a passing bid
                            self.bid_value=self.bid_value_final-1
                elif self.bid_counter==0:
                    # minimum call
                    print('\nBid set to 14 as atleast minimum call mandatory in first bid')
                    self.bid_value=14
                else:
                    # setting the bid_value to be less than the bid_value_final so that at the 
                    # end of the outer while loop, the condition satisfies a passing bid
                    self.bid_value=self.bid_value_final-1 # no need of minus 1 actually
                    
            else:
                for i in range(4):
                    # case 5
                    ########################################################################
                    # if there is a list of len 4, which means all other lsts be len 0
                    if len(self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][i])==4:
                        #print('\nreached case5')
                        # case 5.a
                        # if J,9 and A in hand
                        if ((self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][i][-1].rank()=='J') and \
                           (self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][i][-2].rank()=='9') and \
                           (self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][i][-3].rank()=='A')):
                            # make bid of upto 20 
                            #print('\nreached 83')
                            if self.bid_value_final<20:
                                self.bid_value=max(self.bid_value_final+1,16)# min call of 16
                                # select lowest card as trump
                                self.trump_card=self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][i][0]
                            found=True
                            break
                        # case 5.b
                        # if J along with any 3
                        elif self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][i][-1].rank()=='J':
                            # make bid of upto 19
                            #print('\nreached 94')
                            if self.bid_value_final<19:
                                self.bid_value=max(self.bid_value_final+1,16)# min call of 16
                                # select lowest card as trump
                                self.trump_card=self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][i][0]
                            found=True
                            break
                        # case 5.c
                        # no J but 9 along with any 3
                        elif self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][i][-1].rank()=='9':
                            # make bid of upto 18
                            #print('\nreached 105')
                            if self.bid_value_final<18:
                                self.bid_value=max(self.bid_value_final+1,16)# min call of 16
                                # select 2nd last card as trump
                                self.trump_card=self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][i][1]
                            found=True
                            break
                        # case 5.d
                        # highest card is A or 10 along with 3 other
                        elif self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][i][-1].rank() in ['A','10']:
                            # make bid of upto 17
                            #print('\nreached 116')
                            if self.bid_value_final<17:
                                self.bid_value=max(self.bid_value_final+1,15)# min call of 15
                                # select 2nd last card as trump
                                self.trump_card=self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][i][1]
                            found=True
                            break
                        # case 5.e
                        # only pointless 4 cards
                        else:
                            # make bid of upto 16
                            #print('\nreached 127')
                            if self.bid_value_final<16:
                                self.bid_value=max(self.bid_value_final+1,15)# min call of 15
                                # select lowest card as trump
                                self.trump_card=self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][i][0]
                            found=True
                            break
                    ########################################################################
                    # case 5 end ###########################################################
                if not found:
                    for i in range(4):
                        # case 4
                        ####################################################################
                        # if there is a list of len 3
                        if len(self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][i])==3:
                            #print('\nreached case4')
                            # case 4.a
                            # J of suit present and the 4th card is also another J
                            # the check is done using half_deal_lst (which is sorted)
                            if ((self.obj_half_deal_lst[self.bid_turn_index][0].rank()=='J') and \
                               (self.obj_half_deal_lst[self.bid_turn_index][-1].rank()=='J')) or \
                               ((self.obj_half_deal_lst[self.bid_turn_index][-2].rank()=='J') and \
                               (self.obj_half_deal_lst[self.bid_turn_index][-1].rank()=='J')):
                                # make bid of upto 18
                                #print('\nreached 151')
                                if self.bid_value_final<18:
                                    self.bid_value=max(self.bid_value_final+1,16)# min call of 16
                                    # select lowest card as trump
                                    self.trump_card=self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][i][0]
                                found=True
                                break
                            # case 4.b
                            # J of suit present but 4th card is not J
                            elif self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][i][-1].rank()=='J':
                                # make bid of upto 17
                                #print('\nreached 162')
                                if self.bid_value_final<17:
                                    self.bid_value=max(self.bid_value_final+1,15)# min call of 15
                                    # select lowest card as trump
                                    self.trump_card=self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][i][0]
                                found=True
                                break
                            # case 4.c
                            # no J of suit but the 4th card is a J
                            # checking against half_deal_lst
                            elif (self.obj_half_deal_lst[self.bid_turn_index][0].rank()=='J') or \
                                (self.obj_half_deal_lst[self.bid_turn_index][-1].rank()=='J'):
                                # make bid of upto 16
                                #print('\nreached 175')
                                if self.bid_value_final<16:
                                    self.bid_value=max(self.bid_value_final+1,15)
                                    # select 2nd last card as trump
                                    self.trump_card=self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][i][1]
                                found=True
                                break
                            else:
                                # make bid of upto 15
                                #print('\nreached 184')
                                if self.bid_value_final<15:
                                    self.bid_value=self.bid_value_final+1
                                    # select 2nd lowest card as trump
                                    self.trump_card=self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][i][1]
                                found=True
                                break
                        ####################################################################
                        # case 4 end #######################################################
                if not found:
                    for i in range(4):
                        if len(self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][i])==2:
                            count_2_lst.append(i)
                        elif len(self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][i])==1:
                            count_1_lst.append(i)
                    if len(count_2_lst)==2:
                        #case3
                        ####################################################################
                        # if there are two sets/suits of two cards each
                        # case 3.a
                        # if there are two J's
                        if (self.obj_half_deal_lst[self.bid_turn_index][1].rank()=='J') and \
                            (self.obj_half_deal_lst[self.bid_turn_index][3].rank()=='J'):
                            if (self.obj_half_deal_lst[self.bid_turn_index][0].point()) >= \
                                (self.obj_half_deal_lst[self.bid_turn_index][2].point()):
                                # make bid of upto 16
                                #print('\nreached 208')
                                if self.bid_value_final<16:
                                    self.bid_value=max(self.bid_value_final+1,15)# min call of 15
                                    # select higher card as trump
                                    self.trump_card=self.obj_half_deal_lst[self.bid_turn_index][0]
                                found=True
                            else:
                                # make bid of upto 16
                                #print('\nreached 217')
                                if self.bid_value_final<16:
                                    self.bid_value=self.bid_value_final+1
                                    # select higher card as trump
                                    self.trump_card=self.obj_half_deal_lst[self.bid_turn_index][2]
                                found=True
                        if not found:
                            for i in range(4):
                                # case 3.b
                                # only one J
                                if self.obj_half_deal_lst[self.bid_turn_index][i].rank()=='J':
                                    # make bid upto 15
                                    #print('\nreached 231')
                                    if self.bid_value_final<15:
                                        self.bid_value=self.bid_value_final+1
                                        # select the card along with J(half_deal_lst is sorted)
                                        self.trump_card=self.obj_half_deal_lst[self.bid_turn_index][i-1]
                                    found=True
                                    break
                        if not found:
                            # case 3.c
                            # no J's
                            if (self.obj_half_deal_lst[self.bid_turn_index][1].point()) >= \
                                (self.obj_half_deal_lst[self.bid_turn_index][3].point()):
                                # make bid of upto 14
                                #print('\nreached 244')
                                if self.bid_value_final<14:
                                    self.bid_value=self.bid_value_final+1
                                    # select higher point card as trump
                                    self.trump_card=self.obj_half_deal_lst[self.bid_turn_index][1]
                                found=True # found may not be needed from here on.. but sticking with it
                            else:
                                # make bid of upto 14
                                #print('\nreached 253')
                                if self.bid_value_final<14:
                                    self.bid_value=self.bid_value_final+1
                                    # select higher card as trump
                                    self.trump_card=self.obj_half_deal_lst[self.bid_turn_index][3]
                                found=True
                    elif len(count_1_lst)==2: # len(count_2_lst) will be one
                        #case2
                        ###################################################################
                        # if there is a suit of two cards and two other suits of single cards
                        # case 2.a
                        # 2-suit has J and both of the 1-suits also have J - tot 3 J's
                        if (self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][count_2_lst[0]]\
                            [-1].rank() == 'J') and \
                            ((self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][count_1_lst[0]]\
                            [0].rank() == 'J') and \
                            (self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][count_1_lst[1]]\
                            [0].rank() == 'J')):
                            # make bid of upto 17
                            #print('\nreached 273')
                            if self.bid_value_final<17:
                                self.bid_value=max(self.bid_value_final+1,15)# min call of 15
                                # select lower card as trump (only 2 cards, other is J)
                                self.trump_card=self.obj_half_dictn_of_cards_grouped[self.bid_turn_index]\
                                [count_2_lst[0]][0]
#                             found=True
                        # case 2.b
                        # the 2-suit has J and one of the 1-suits also have J - tot 2 J's
                        elif (self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][count_2_lst[0]]\
                            [-1].rank() == 'J') and \
                            ((self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][count_1_lst[0]]\
                            [0].rank() == 'J') or \
                            (self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][count_1_lst[1]]\
                            [0].rank() == 'J')):
                            # make bid of upto 16
                            #print('\nreached 289')
                            if self.bid_value_final<16:
                                self.bid_value=max(self.bid_value_final+1,15)# min call of 15
                                # select lower card as trump (only 2 cards, other is J)
                                self.trump_card=self.obj_half_dictn_of_cards_grouped[self.bid_turn_index]\
                                [count_2_lst[0]][0]
#                             found=True
                        # case 2.c
                        # only the 2-suit has J
                        elif (self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][count_2_lst[0]]\
                            [-1].rank() == 'J'):
                            # make bid of upto 15
                            #print('\nreached 301')
                            if self.bid_value_final<15:
                                self.bid_value=self.bid_value_final+1
                                # select lower card as trump (only 2 cards, other is J)
                                self.trump_card=self.obj_half_dictn_of_cards_grouped[self.bid_turn_index]\
                                [count_2_lst[0]][0]
#                             found=True
                        # case 2.d
                        # the 2-suit doesn't have J but both the 1-suits have J
                        elif ((self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][count_1_lst[0]]\
                            [0].rank() == 'J') and \
                            (self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][count_1_lst[1]]\
                            [0].rank() == 'J')):
                            # make bid of upto 15
                            #print('\nreached 315')
                            if self.bid_value_final<15:
                                self.bid_value=self.bid_value_final+1
                                # select higher card of 2-suit (no J in that suit)
                                self.trump_card=self.obj_half_dictn_of_cards_grouped[self.bid_turn_index]\
                                [count_2_lst[0]][-1]
#                             found=True
                        # case 2.e
                        # 2-suit does't have J and only 1 other J or no J at all
                        else:
                            # make bid of upto 14
                            #print('\nreached 326')
                            if self.bid_value_final<14:
                                self.bid_value=self.bid_value_final+1
                                # select higher card of 2-suit (no J in that suit)
                                self.trump_card=self.obj_half_dictn_of_cards_grouped[self.bid_turn_index]\
                                [count_2_lst[0]][-1]
#                             found=True                     
                    else:
                        # len(count_1_lst) will be 4 in this case
                        #case1
                        ################################################################### 
                        # all 4 cards are from different suits
                        j_count2=0
                        # to find the no.of J's in hand
                        p_i_holder_lst=[0.00,0] # holds point and index of a card
                        
                        for xy in self.obj_half_deal_lst[self.bid_turn_index]:
                            if xy.rank()=='J':
                                j_count2+=1
                        # case 1.a
                        # 3 J's in hand (4 J's is already ruled out)
                        if j_count2==3:
                            for xy in self.obj_half_deal_lst[self.bid_turn_index]:
                                if xy.rank()!='J':
                                    # make bid of upto 16
                                    #print('\nreached 347')
                                    if self.bid_value_final<16:
                                        self.bid_value=max(self.bid_value_final+1,15)# min call of 15
                                        # select non J card
                                        self.trump_card=xy
#                                     found=True
                                    break
                        else:
                            # making a lst that holds the point and index of the highest card
                            # which is not a J
                            for i in range(4):
                                    xy = self.obj_half_deal_lst[self.bid_turn_index][i]
                                    if (xy.point()!=3.00) and  (xy.point()>p_i_holder_lst[0]):
                                        p_i_holder_lst.clear()
                                        p_i_holder_lst.extend([xy.point(),i])
                            # case 1.b
                            # 2 J's in hand
                            if j_count2==2:                               
                                # make bid of upto 15
                                #print('\nreached 368')
                                if self.bid_value_final<15:
                                    self.bid_value=self.bid_value_final+1
                                    # select card with highest point and not J(index=p_i_*lst[2])
                                    self.trump_card=self.obj_half_deal_lst[self.bid_turn_index]\
                                    [p_i_holder_lst[1]]
#                                 found=True
                            # case 1.c
                            # one J or no J in hand 
                            else:
                                # make bid of upto 14
                                #print('\nreached 390')
                                if self.bid_value_final<14:
                                    self.bid_value=self.bid_value_final+1
                                    # select card with highest point and not J(index=p_i_*lst[2])
                                    self.trump_card=self.obj_half_deal_lst[self.bid_turn_index]\
                                    [p_i_holder_lst[1]]
#                                 found=True
                        ###################################################################
                        # case 1 end ######################################################
            
            if self.bid_value>self.bid_value_final:
                self.bid_value_final=self.bid_value
                self.highest_bidder_index=self.bid_turn_index
                
                self.highest_bidder1_index=self.highest_bidder_index
                # the above is to keep a copy of who was the highest bidder in round1, which will be
                # used for setting trump in round2 of bid(i.e. to see if a team mate had set trump in
                # first bid round)
                
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                # calling gui widget to display call message
                self.gui_handle.gui_half_bid_values(self.bid_turn_index,self.bid_value_final,calls=True)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                
                print('\n{} calls {}'.format(self.players_lst[self.bid_turn_index],self.bid_value_final))
                self.bid_turn_index=(self.bid_turn_index+1)%4
                self.bid_counter+=1
                self.bid_counter_lst.append(self.bid_counter)
                
                # resetting some variables used, to default values
                found=False
                count_1_lst.clear()
                count_2_lst.clear()               
            else:
                
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                
                # calling gui widget to display call message(pass)
                self.gui_handle.gui_half_bid_values(self.bid_turn_index,0,calls=False)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                
                print('\n{} passes'.format(self.players_lst[self.bid_turn_index]))
                self.bid_turn_index=(self.bid_turn_index+2)%4
                self.bid_counter+=2 # to skip the bidding chance of the current bidder's mate
                self.bid_counter_lst.append(self.bid_counter)
                
                #resetting some variables used, to default values
                found=False
                count_1_lst.clear()
                count_2_lst.clear()
            
            # to stop bidding aft successive passes by team mates
            if (len(self.bid_counter_lst)>2) and ((self.bid_counter_lst[-1] - self.bid_counter_lst[-3])>3):
                break

        #########################################
        
        print('\n{} made the highest bid: {}'.format(self.players_lst[self.highest_bidder_index],\
                                                    self.bid_value_final))
        print('\nbid_counter value: ',self.bid_counter)
        
        # if player is not highest bidder i.e index!=0       
        if self.highest_bidder_index:
            self.trump_set=True
            self.trump_suit=self.trump_card.suit()
            self.trump_suit_index=self.suit.index(self.trump_suit)
            print('\nTrump card set by {}'.format(self.players_lst[self.highest_bidder_index]))
            
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^            
            # gui window for declaring the bid and bidder after completing the half_bid
            self.gui_handle.gui_half_bid_declare(self.highest_bidder_index,self.bid_value_final)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            
            # need to remove trump card from the obj_dictn_of_cards_grouped to make sure it is not 
            # played until trump is revealed
            # this is done only for the 3 other players, since the condition is taken care of 
            # for player in inp_parse_check
            self.obj_dictn_of_cards_grouped[self.highest_bidder_index]\
                                            [self.trump_suit_index].remove(self.trump_card)
            self.obj_deal_lst_copy[self.highest_bidder_index].remove(self.trump_card)

        # if player is the highest bidder
        else:
            
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^            
            #gui window for taking trump input and declaring bidder if player bids highest
            self.player_input=self.gui_handle.gui_half_bid_trump(self.bid_value_final)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

            print('\nYour hand: ',end=' ')
            for i in self.obj_half_deal_lst[0][:4]:
                print(i.show(),end=' ')

            # trump input converted to object
            self.obj_trump_checked=self.trump_verify(self.player_input,True)
            # passing half_hand=True to verify for half hand bid
            self.trump_set=True
            self.trump_suit=self.obj_trump_checked.suit()
            self.trump_suit_index=self.suit.index(self.trump_suit)
            # storing the trump input to the variable used by all hands(from Prepare_game())
            self.trump_card=self.obj_trump_checked
            print('\nTrump card set by {}: {}'.format(self.players_lst[0],self.obj_trump_checked.form()))

        
        # displaying full hands/ pass True to see updated hands after each round
        self.obj_display_hands(self.highest_bidder_index,self.trump_revealed,self.trump_card,\
                               show_updated=False,situation=0)

    ###################################################################
    # bid_half_hand() end #############################################
    
    #P2.b)
    def bid_full_hand(self):
    # no need to use a hold value here as in bid_half_hand() as the starting bidder index here 
    # is taken from the bid_half_hand() method itself which makes sure that the same round is 
    # repeated if that was what was required.
        self.bid2_turn_index=self.round1_lead_index
        # the player who started the first round bidding gets to start the second round bidding as well,
        # round1_lead_index stores the value of the first bid_turn_index value which was generated 
        # randomly. bid_turn_index and similarly bid2_turn_index get updated during bids 
        
        
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # gui window for 2nd bid round message
        self.gui_handle.gui_full_bid_mes(self.players_lst[self.bid2_turn_index])
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#         print('\nStarting bid2_turn_index is: ',self.round1_lead_index)
        
        self.bid2_value_final=20 # to make sure min starting bid value is 21
        self.bid2_counter=0
        # the above counter increments after every bid or pass and is used to stop bidding 
        # after two rounds
        self.bid2_counter_lst=[0]
        # the above counter list is used to stop bidding if both team mates passes
        self.bid2_any_call=False
        # this is used to check if there was any bid at all with full hand
        
        
        # to carry on with various checks for finding a trump card
        found=False
        
        # making a list of J counts
        j_count_lst=[0,0,0,0]
        for k in range(4):
            for i in self.obj_deal_lst[k]:
                if i.rank()=='J':
                    j_count_lst[k]+=1
        
        # inserting the trump card of previous round back in hand for finding new trump in the 
        # 2nd round of bidding
        if self.highest_bidder_index!=0:
#             print('\nFirst round trump inserted back in first round highest bidder hand')
            self.insert_trump_card_back()
            # should be removed again if bid2_any_call is False at the end (i.e first round Trump is to stay)
        
        while self.bid2_counter<8:
            if self.bid2_turn_index==0:
            # taking bid input if bid_turn_index==0
            
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                # gui window for full_bid entry
                self.bid2_value_inp=self.gui_handle.gui_full_bid_entry()
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#                 self.bid2_value_inp=input('\nEnter your 2nd round bid (any non-digit input will be considered as pass: ')
                if self.bid2_value_inp.isdigit():
                    self.bid2_value=int(self.bid2_value_inp)
                    while not (20<self.bid2_value<28):
                    # to make sure that the bid value is between 20 and 28
##################### further look into whether 28 needs to be allowed in 2nd bid and how to incorporate 
                    # the 'thani' call (without trump)
                        self.bid2_value_inp=input('\nSorry, plz enter a bid value from 21-27: ')
                        if self.bid2_value_inp.isdigit():
                            self.bid2_value=int(self.bid2_value_inp)
                        else:
                            # the bid is being passed
                            self.bid2_value=self.bid2_value_final
                            # bid2_value>bid2_value_final is the condition for deciding whether a bid
                            # was made. setting it be equal would hence correspond to a pass
                            break
                else:
                # if a non-digit input was made, it will be considered a pass and bid2_value is 
                # set to be equal to bid2_value_final so that a pass decision can be made 
                # when the condition (bid2_value <= bid2_value_final) at the end of the 
                # outer while loop is satisfied. There is no need for a mandatory minimun call in 
                # the 2nd round.
                    self.bid2_value=self.bid2_value_final
            else:
                # conditions for making a bid of 21 or more for players 1-3
                for i in range(4):
#                     print('\nreached line 651, {} time'.format(i))
                    
                    # - 1) 4 trump cards without J but 9 - and a) three other J's, or b) two other J's and 
                    #      teammate had called atleast 18 in first bid - can call upto 22
                    if (len(self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i])==4 and\
                         self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i][-1].rank()=='9') \
                      and \
                       (   (j_count_lst[self.bid2_turn_index]==3) \
                          or \
                           ((j_count_lst[self.bid2_turn_index]==2) and ((self.bid2_turn_index+2)%4==self.\
                                 highest_bidder1_index) and (self.bid_value_final>17))\
                       ):
##################### actually need to check if team mate had made such a call, and not necessarily if 
                    # if she was the highest bidder in bid1
                        if self.bid2_value_final!=21:
                            self.bid2_value=21
                        else:
                            self.bid2_value=22
                        # i.e. make a call of 22 if highest bid in round is 21, else call 21 
                        self.trump_card2=self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i][1]
                        # the 2nd lowest card in the suit is kept as trump card
                        found=True
#                         print('\ncase 1 of 2nd round bid satisfied')
                        break # to break from the for loop
                    
                    
                    # - 2) 4 trump cards including J - and a) two other J's, or c) one other J but 3 cards 
                    #      in same suit with highest J or 9, or b) only one other J but team mate had 
                    #      called atleast 17 in first bid - can call upto 22
                    if (len(self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i])==4 and\
                         self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i][-1].rank()=='J') \
                      and \
                       (   (j_count_lst[self.bid2_turn_index]==3) \
                          or \
                           (   (j_count_lst[self.bid2_turn_index]==2) \
                              and \
                               (   ((self.bid2_turn_index+2)%4==self.highest_bidder1_index and \
                                    self.bid_value_final>16) \
                                  or \
                                   (True in list(map(lambda x: len(self.obj_dictn_of_cards_grouped\
                                    [self.bid2_turn_index][x])==3, \
                                    self.obj_dictn_of_cards_grouped[self.bid2_turn_index])))\
                               )\
                           )\
                       ):
                    # the last condition checks if there is a suit of length 3 in current bidder's hand
                    # for that , the map function returns True or False by testing elements of the iterable 
                    # against the expression in lambda function and the returned values are made into a list
                    # and the membership is checked
                    # eg. 
                    #     dictnu={1:[1,2,3,4],0:[],2:[1,5,6]}
                    #     if True in list(map(lambda x: len(dictnu[x])==3, dictnu)):
                    #     print('yes')
                    # end of eg.                    
                        if self.bid2_value_final!=21:
                            self.bid2_value=21
                        else:
                            self.bid2_value=22
                        # i.e. make a call of 22 if highest bid in round is 21, else call 21 
                        self.trump_card2=self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i][1]
                        # the 2nd lowest card in the suit is kept as trump card
                        found=True
#                         print('\ncase 2 of 2nd round bid satisfied')
                        break # to break from the for loop
                        
                    # - 3) 5 trump cards without J but 9 - and a) three other J's, or b) two other J's and 
                    #       team mate had called atleast 17 in first bid, or c) 1 other J with all three
                    #       cards from the same suit, or d) 1 J with team mate having 
                    #       called atleast 18 in round1 - can call till 22
                    if (len(self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i])==5) and\
                       (self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i][-1].rank()=='9') \
                      and \
                       (   (j_count_lst[self.bid2_turn_index]==3) \
                          or \
                           ((j_count_lst[self.bid2_turn_index]==2) and ((self.bid2_turn_index+2)%4==self.\
                               highest_bidder1_index) and (self.bid_value_final>16)\
                           ) \
                          or \
                           ((j_count_lst[self.bid2_turn_index]==1) and \
                                (   (True in list(map(lambda x: len(self.obj_dictn_of_cards_grouped\
                                        [self.bid2_turn_index][x])==3, \
                                        self.obj_dictn_of_cards_grouped[self.bid2_turn_index]))) \
                               or \
                                    (((self.bid2_turn_index+2)%4==self.highest_bidder1_index) and \
                                        (self.bid_value_final>17))\
                                )\
                           )
                       ):
                        if self.bid2_value_final!=21:
                            self.bid2_value=21
                        else:
                            self.bid2_value=22
                        # i.e. make a call of 22 if highest bid in round is 21, else call 21 
                        self.trump_card2=self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i][2]
                        # the 3rd lowest card in the suit is kept as trump card
                        found=True
#                         print('\ncase 3 of 2nd round bid satisfied')
                        break # to break from the for loop
                                        
                    # - 4) 5 trump cards with J - and a) two other J's, or b) one other J and 
                    #      team mate had called atleast 16 in first bid, or c) all three of same suit with
                    #      9 and team mate had called atleast 16 in first round - can call till 22
                    if (len(self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i])==5) and\
                       (self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i][-1].rank()=='J') \
                      and \
                       ((j_count_lst[self.bid2_turn_index]==3) \
                        or \
                        ( (((self.bid2_turn_index+2)%4==self.highest_bidder1_index) and \
                          (self.bid_value_final>15)) and \
                         (((j_count_lst[self.bid2_turn_index]==2)) or \
                         (True in list(map(lambda x: len(self.obj_dictn_of_cards_grouped\
                                [self.bid2_turn_index][x])==3, \
                                self.obj_dictn_of_cards_grouped[self.bid2_turn_index]))))
                        )\
                       ):
                        if self.bid2_value_final!=21:
                            self.bid2_value=21
                        else:
                            self.bid2_value=22
                        # i.e. make a call of 22 if highest bid in round is 21, else call 21 
                        self.trump_card2=self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i][2]
                        # the 3rd lowest card in the suit is kept as trump card
                        found=True
#                         print('\ncase 4 of 2nd round bid satisfied')
                        break # to break from the for loop
                    
                    # - 5) 6 trump cards without J but 9- and a) two other J's, or b) one other J and 
                    #      team mate had called atleast 17 in first bid, or c) no other J but 
                    #      team mate had called atleast 18 in first bid - can call till 22
                    if (len(self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i])==6) and\
                       (self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i][-1].rank()=='9') \
                      and \
                       ( (j_count_lst[self.bid2_turn_index]==2) \
                         or \
                         ((j_count_lst[self.bid2_turn_index]==1) and ((self.bid2_turn_index+2)%4==self.\
                               highest_bidder1_index) and (self.bid_value_final>16)) \
                         or \
                         (((self.bid2_turn_index+2)%4==self.highest_bidder1_index) and \
                          (self.bid_value_final>17))
                       ):
                        if self.bid2_value_final!=21:
                            self.bid2_value=21
                        else:
                            self.bid2_value=22
                        # i.e. make a call of 22 if highest bid in round is 21, else call 21 
                        self.trump_card2=self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i][2]
                        # the 3rd lowest card in the suit is kept as trump card
                        found=True
#                         print('\ncase 5 of 2nd round bid satisfied')
                        break # to break from the for loop
                    
                    # - 6) 6 trump cards with J - and a)two other J's, or b) 1 other J, or 
                    #      c) no other J but team mate had called atleast 16 in first bid, or d) both 
                    #      cards of same suit with 9
                    if (len(self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i])==6) and\
                       (self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i][-1].rank()=='J'):
                        # if other two are J's then can call upto 25
                        if j_count_lst[self.bid2_turn_index]==3:
                            self.bid2_value=min(self.bid2_value_final+1,25)
                            found=True
                        # if one other J then call upto 23
                        elif j_count_lst[self.bid2_turn_index]==2:
                            self.bid2_value=min(self.bid2_value_final+1,23)
                            found=True
                        # 
                        elif ((self.bid2_turn_index+2)%4==self.highest_bidder1_index and \
                             self.bid_value_final>15) \
                            or \
                             ((True in list(map(lambda x: len(self.obj_dictn_of_cards_grouped\
                                [self.bid2_turn_index][x])==2, \
                                self.obj_dictn_of_cards_grouped[self.bid2_turn_index]))) and \
                                 (self.obj_deal_lst_copy[self.bid2_turn_index][1].rank()=='9' or \
                                 self.obj_deal_lst_copy[self.bid2_turn_index][-1].rank()=='9')
                             ):
                            self.bid2_value=min(self.bid2_value_final+1,22)
                            found=True
                        if found:
                            self.trump_card2=self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i][2]
                            # the 3rd lowest card in the suit is kept as trump card
#                             print('\ncase 6 of 2nd round bid satisfied')
                            break # to break from the for loop
                            
                    # - 7) 7 trump cards without J - and a) another J, or b) no J but 
                    #      team mate had called atleast 17 in first bid
                    if (len(self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i])==7) and\
                       (self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i][-1].rank()=='9') \
                      and \
                        ((j_count_lst[self.bid2_turn_index]==1) \
                        or \
                        (((self.bid2_turn_index+2)%4==self.highest_bidder1_index) and \
                         (self.bid_value_final>16))
                        ):
                        self.bid2_value=min(self.bid2_value_final+1,23)
                        self.trump_card2=self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i][2]
                        # the 3rd lowest card in the suit is kept as trump card
                        found=True
#                         print('\ncase 7 of 2nd round bid satisfied')
                        break # to break from the for loop
                        
                    # - 8) 7 trump cards with J 
                    #      (8 is invalid - gets redealt in Deck())
                    if (len(self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i])==7) and\
                       (self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i][-1].rank()=='J'):
                        self.bid2_value=min(self.bid2_value_final+2,24)
                        self.trump_card2=self.obj_dictn_of_cards_grouped[self.bid2_turn_index][i][3]
                        # the 4rd lowest card in the suit is kept as trump card
                        found=True
#                         print('\ncase 8 of 2nd round bid satisfied')
                        break # to break from the for loop
                
                if not found:
                    self.bid2_value=self.bid2_value_final
            
                
            if (self.bid2_value>self.bid2_value_final):
                self.bid2_value_final=self.bid2_value
                self.highest_bidder2_index=self.bid2_turn_index
                
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                # gui window for full bid call display
                self.gui_handle.gui_full_bid_values(self.bid2_turn_index,self.bid2_value,calls=True)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                self.bid2_counter+=1
                self.bid2_turn_index=(self.bid2_turn_index+1)%4
                self.bid2_any_call=True                
            
            else:
                
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                # gui window for full bid call display(pass)
                self.gui_handle.gui_full_bid_values(self.bid2_turn_index,20,calls=False)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                
                if not self.bid2_any_call:
                    if not self.bid2_counter==3:
                    # bid2_counter==3 in the outer else means that all 4 players have passed, 
                    # so break loop in the else below
                        self.bid2_counter+=1
                        self.bid2_turn_index=(self.bid2_turn_index+1)%4
                    else:
                        break
                else:
                    self.bid2_counter+=2
                    self.bid2_turn_index=(self.bid2_turn_index+2)%4
            

            self.bid2_counter_lst.append(self.bid2_counter)
            if (len(self.bid2_counter_lst)>2) and ((self.bid2_counter_lst[-1] - self.bid2_counter_lst[-3])>3):
            # after successive passes the diff b/w the last and 3rd last bid2_counter values will be 4
                break
        
        print('\nbid2_counter value: ',self.bid2_counter)
        
        # if any call was made in bidding round 2
        if self.bid2_any_call:
            
            print('\n{} made the highest bid: {}'.format(self.players_lst[self.highest_bidder2_index],\
                self.bid2_value_final))
            
            self.highest_bidder_index=self.highest_bidder2_index
            # actually highest_bidder_index and highest_bidder2_index were kept separate and 
            # different sets of code written for trump_verify method. But to avoid writing extra
            # code for insert_trump_card_back and trump_distribution_good methods, highest_bidder_
            # index is being assigned the value of highest_bidder2_index now. Previous round's 
            # highest_bidder_index is available in highest_bidder1_index
            
            # if player is not highest bidder i.e index!=0       
            if self.highest_bidder2_index:
                self.trump_card=self.trump_card2
                self.trump_set=True
                self.trump_suit=self.trump_card.suit()
                self.trump_suit_index=self.suit.index(self.trump_suit)
                
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                # gui window for declaring 2nd bid round result
                self.gui_handle.gui_full_bid_declare(self.highest_bidder2_index, self.bid2_value_final,\
                                                    no_call=False)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                
                print('\nTrump card set by {}'.format(self.players_lst[self.highest_bidder2_index]))

                # need to remove trump card from the obj_dictn_of_cards_grouped to make sure it is not 
                # played until trump is revealed
                # this is done only for the 3 other players, since the condition is taken care of 
                # for player in inp_parse_check
                self.obj_dictn_of_cards_grouped[self.highest_bidder2_index]\
                                                [self.trump_suit_index].remove(self.trump_card)
                self.obj_deal_lst_copy[self.highest_bidder2_index].remove(self.trump_card)
            
            # if player is the highest bidder
            else:
                
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                # gui window for taking trump entry
                self.player_input=self.gui_handle.gui_full_bid_trump(self.bid2_value_final)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                

                # trump input converted to object
                self.obj_trump_checked=self.trump_verify(self.player_input,False)
                # passing half_hand=False to verify trump for full hand bid
                self.trump_set=True
                self.trump_suit=self.obj_trump_checked.suit()
                self.trump_suit_index=self.suit.index(self.trump_suit)
                # storing the trump input to the variable used by all hands(from Prepare_game())
                self.trump_card=self.obj_trump_checked
                print('\nTrump card set by {}: {}'.format(self.players_lst[0],self.obj_trump_checked.form()))
                
                
            # displaying full hands/ pass True to see updated hands after each round(option for terminal disp
            # not applicable for gui display)
            self.obj_display_hands(self.highest_bidder2_index,\
                                   self.trump_revealed,self.trump_card,show_updated=False,situation=1)

        else:
#             print('\nEveryone passed in 2nd bid round')
            # this is a problem due to gradual developing of code. initially the code ran for only
            # half hand. in that scenario,
            # after half bid, trump_card was removed from the hands 1-3,(dictn_of_cards_grouped and 
            # deal_lst_copy) to prevent playing trump/face down card before trump_reveal. but it is now 
            # inserted back before full bid for obvious reasons. But if there are no new calls in full 
            # bid, the previous trump remains and it has to be once again removed from the highest 
            # bidder's hand(only for hands 1-3)
            if self.highest_bidder_index:
                self.obj_dictn_of_cards_grouped[self.highest_bidder_index]\
                                                [self.trump_suit_index].remove(self.trump_card)
                self.obj_deal_lst_copy[self.highest_bidder_index].remove(self.trump_card)
#             print('\nFirst round trump removed from first round highest bidder hand')

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            # gui window for declaring 2nd bid round result
            self.gui_handle.gui_full_bid_declare(self.highest_bidder1_index,0,no_call=True)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

            print('\nNo one called 21 or above, so trump set by {} stays for the call of {} '.format(self.\
                    players_lst[self.highest_bidder1_index],self.bid_value_final))    
        
            
    ###################################################################
    # bid_full_hand() end #############################################
    
    #P3)
    # to check if the team who lost bid has atleast one card from the trump suit
    # this cld be called and checked in init of round1 to do a redeal if needed
    def trump_distrb_good(self):
        trump_count=0
        ij1=(self.highest_bidder_index+1)%4
        ij2=(self.highest_bidder_index+3)%4
        for itt in self.obj_deal_lst[ij1]:
            if itt.suit()==self.trump_suit:
                trump_count+=1
        for itt in self.obj_deal_lst[ij2]:
            if itt.suit()==self.trump_suit:
                trump_count+=1
        if not trump_count:
            return(False)
        else:
            return(True)
        
        
    ###################################################################
    # trump_distrb_good() end #########################################
    
    #P4)
    # to insert the trump card back in highest bidder dictn once trump is revealed
    def insert_trump_card_back(self):
        # to insert back in dictn
        leng=len(self.obj_dictn_of_cards_grouped[self.highest_bidder_index][self.trump_suit_index])
        if leng:
            for i in range(leng):
                itema=self.obj_dictn_of_cards_grouped[self.highest_bidder_index][self.trump_suit_index][i]
                if itema.point()>self.trump_card.point():
                    # insert at the position i
                    self.obj_dictn_of_cards_grouped[self.highest_bidder_index]\
                    [self.trump_suit_index].insert(i,self.trump_card)
                    break
                else:
                    if i!=leng-1:
                        continue
                    else:
                        # insert at the end
                        self.obj_dictn_of_cards_grouped[self.highest_bidder_index]\
                            [self.trump_suit_index].append(self.trump_card)
        else:
            # insert at the end, this will be the only element
            self.obj_dictn_of_cards_grouped[self.highest_bidder_index]\
                [self.trump_suit_index].append(self.trump_card)
        
        # to insert back in deal_lst_copy
        leng2=len(self.obj_deal_lst_copy[self.highest_bidder_index])
        if leng2:
            for i in range(leng2):
                caard=self.obj_deal_lst_copy[self.highest_bidder_index][i]
                if caard.value()>self.trump_card.value():
                    self.obj_deal_lst_copy[self.highest_bidder_index].insert(i,self.trump_card)
                    break
                else:
                    if i!=leng2-1:
                        continue
                    else:
                        self.obj_deal_lst_copy[self.highest_bidder_index].append(self.trump_card)
        else:
            self.obj_deal_lst_copy[self.highest_bidder_index].append(self.trump_card)
                    
            
    ###################################################################
    # insert_trump_card_back() end ####################################
            
    
    
