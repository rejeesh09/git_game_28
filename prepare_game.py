#!/usr/bin/env python
# coding: utf-8

# ## importing Cards() class and making dictionary of cards

# In[ ]:


from cards import Cards
# importing the class - Cards()
#######################################################################


# making objects of Cards()
# spade-\u2660, hearts-\u2665, clubs-\u2663, diamonds-\u2666
suit_uni=['\u2660','\u2665','\u2663','\u2666']
rank=['7','8','Q','K','10','A','9','J']
        
# making the game deck of 32 cards
# ['7♠', '8♠','Q♠',...,'9♦','J♦']
cards_no_colr=[]
for y in suit_uni:
    cards_no_colr.extend([x+y for x in rank])

# dictn_of_cards is a dictionary of 32 Cards objects
# {0: <__main__.Cards object at ..>,.., 32: 31: <__main__.Cards object at..}
i=range(32)
dictn_of_cards=dict.fromkeys(i,'')
for j in range(32):
    dictn_of_cards[j]=Cards(cards_no_colr[j])
#######################################################################


# ## importing Deck() class - parent class of Prepare_game()

# In[1]:


from deck import Deck
# importing the class - Deck()
# this import is done to allow this .py file to run independently as a module
# and not for making the class variables(ones with self prefix(even inside methods)) and methods
# available to the child class. Those are available by default by virture of being a child.
#######################################################################


# ## Prepare_game() class

# In[2]:


# have to include two methods bid() and set_trump()
class Prepare_game(Deck):
    ###################################################################
    def __init__(self,hold):
        # methods from Deck()
        super().__init__(dictn_of_cards) #??? in which namespace does dictn_of_cards reside?
        # looks like when doing from prepare_game import Prepare_game, the whole prepare_game.py script 
        # is run first and then the class Prepare_game() is imported from it
        # All the (15*) variables(attributes) in Deck()'s init() are now constructed by the above line
        super().obj_deal(hold)
        super().obj_sort_half_hands()
        super().obj_display_half_hands()
        super().obj_sort_hands()
        super().obj_induvidual_dictns() # makes obj_dictn_of_cards_grouped, which is used 
        #throughout to make decision on card to be played
        super().obj_half_dictns() # makes grouped dictn of half hand
#         super().obj_display_hands()
        # (6 out of 7) methods of Deck are constructed here
        
        ###############################################################
        #8.###### var8
        #p1)
        self.obj_played_card_lst=[] # this could be cleared after each round
        #p2)
        self.obj_played_card_lst_of_32=[]
        
        # this dictionary holds the highest card of the round and the corresponding turn index
        # only the turn_index is actually needed
        #9.###### var9
        #p3)
        self.obj_dictn_of_highest_card_and_turn=dict()
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
        #to be updated when entry added to dictn['trump'] lst
        ###############################################################

    ###################################################################
    # init() end ######################################################
    
    #P1)
    def trump_verify(self,trump):
        # checks and converts the trump input to unicode and then to Card object        
        control_count=0
        self.trump=trump
        self.inp_cpy=self.trump
        self.inp_cpy.strip(" ") # doesn't seem to work
        self.inp_cpy.replace(" ","") # this seems to work only for space inside the string
        ###############################################################
        if self.inp_cpy.capitalize() not in self.legal_card_lst:
            print('\nYou did not enter a valid card')
            self.player_input=input('\nEnter the card rank followed by the first letter of the suit, eg.' 
                +'\n7s or ah or 10d etc.: ').lower()
            self.trump_verify(self.player_input)
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
        # ?????????? # this following set of code repeated the no.of times a wrong entry is
        # given without the check for control_count==0
        if control_count==0:
            if self.inp_uni_obj not in self.obj_dictn_of_players_and_hand[self.player_name]:
                print('\nEntered card not in hand')
                self.player_input=input('\nEnter the card rank followed by the first letter of the suit, eg.' 
                    +'\n7s or ah or 10d etc.: ').lower()
                self.trump_verify(self.player_input)
            else:
                control_count+=1
        # returns the input, converted to Cards object
        return(self.inp_uni_obj)
    
    ###################################################################
    # trump_verify end ################################################
    
    #P2)
    def bid_half_hand(self,hold):
        import numpy as np
        import pickle
        
        if not hold:
            # selecting the first turn for bidding randomly
            self.bid_turn_index=np.random.randint(4)
            # saving a copy for debugging 
            fb=open("last_starting_bid_turn.txt","wb")
            pickle.dump(self.bid_turn_index,fb)
            fb.close()
        else:
            fb=open("last_starting_bid_turn.txt","rb")
            self.bid_turn_index=pickle.load(fb)
            fb.close()

        print('\nStarting bid_turn_index is: ',self.bid_turn_index)
        
        self.bid_value_final=13 # to make sure min starting bid value is 14
        
        # to stop bidding after two rounds
        self.bid_counter=0
        # to stop bidding if both team mates passes
        self.bid_counter_lst=[0]
        
        found=False
        # to hold the index of suits with len()==2 for cases 3 and 2
        count_2_lst=[]
        # to hold the index of suits with len()==1 for cases 3 and 2
        count_1_lst=[]

        while self.bid_counter<8:
            # taking bid input if bid_turn_index==0
            if self.bid_turn_index==0:
                self.bid_value_inp=input('\nEnter your bid (any non-digit input will be considered as pass): ')
                if self.bid_value_inp.isdigit():
                    self.bid_value=int(self.bid_value_inp)
                    while not (13<self.bid_value<21): # setting 21 limit for half hand bid
                        self.bid_value_inp=input('\nYou did not enter a legal bid value (14-20). Pls try again: ')
                        if self.bid_value_inp.isdigit():
                            self.bid_value=int(self.bid_value_inp)
                        elif self.bid_counter==0:
                            # minimum call
                            print('\nBid set to 14 as atleast minimum call mandatory in first bid')
                            self.bid_value=14
                        else:
                            # passing bid
                            self.bid_value=self.bid_value_final-1
                elif self.bid_counter==0:
                    # minimum call
                    print('\nBid set to 14 as atleast minimum call mandatory in first bid')
                    self.bid_value=14
                else:
                    # passing bid
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
                        if ((self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][i][-1].rank()=='J') and                            (self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][i][-2].rank()=='9') and                            (self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][i][-3].rank()=='A')):
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
                            if ((self.obj_half_deal_lst[self.bid_turn_index][0].rank()=='J') and                                (self.obj_half_deal_lst[self.bid_turn_index][-1].rank()=='J')) or                                ((self.obj_half_deal_lst[self.bid_turn_index][-2].rank()=='J') and                                (self.obj_half_deal_lst[self.bid_turn_index][-1].rank()=='J')):
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
                            elif (self.obj_half_deal_lst[self.bid_turn_index][0].rank()=='J') or                                 (self.obj_half_deal_lst[self.bid_turn_index][-1].rank()=='J'):
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
                        # case 3.a
                        # if there are two J's
                        if (self.obj_half_deal_lst[self.bid_turn_index][1].rank()=='J') and                             (self.obj_half_deal_lst[self.bid_turn_index][3].rank()=='J'):
                            if (self.obj_half_deal_lst[self.bid_turn_index][0].point()) >=                                 (self.obj_half_deal_lst[self.bid_turn_index][2].point()):
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
                            if (self.obj_half_deal_lst[self.bid_turn_index][1].point()) >=                                 (self.obj_half_deal_lst[self.bid_turn_index][3].point()):
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
                        # case 2.a
                        # 2-suit has J and both of the 1-suits also have J - tot 3 J's
                        if (self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][count_2_lst[0]]                            [-1].rank() == 'J') and                             ((self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][count_1_lst[0]]                            [0].rank() == 'J') and                             (self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][count_1_lst[1]]                            [0].rank() == 'J')):
                            # make bid of upto 17
                            #print('\nreached 273')
                            if self.bid_value_final<17:
                                self.bid_value=max(self.bid_value_final+1,15)# min call of 15
                                # select lower card as trump (only 2 cards, other is J)
                                self.trump_card=self.obj_half_dictn_of_cards_grouped[self.bid_turn_index]                                [count_2_lst[0]][0]
#                             found=True
                        # case 2.b
                        # 2-suit has J and one off the 1-suits also have J - tot 2 J's
                        elif (self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][count_2_lst[0]]                            [-1].rank() == 'J') and                             ((self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][count_1_lst[0]]                            [0].rank() == 'J') or                             (self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][count_1_lst[1]]                            [0].rank() == 'J')):
                            # make bid of upto 16
                            #print('\nreached 289')
                            if self.bid_value_final<16:
                                self.bid_value=max(self.bid_value_final+1,15)# min call of 15
                                # select lower card as trump (only 2 cards, other is J)
                                self.trump_card=self.obj_half_dictn_of_cards_grouped[self.bid_turn_index]                                [count_2_lst[0]][0]
#                             found=True
                        # case 2.c
                        # only 2-suit has J
                        elif (self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][count_2_lst[0]]                            [-1].rank() == 'J'):
                            # make bid of upto 15
                            #print('\nreached 301')
                            if self.bid_value_final<15:
                                self.bid_value=self.bid_value_final+1
                                # select lower card as trump (only 2 cards, other is J)
                                self.trump_card=self.obj_half_dictn_of_cards_grouped[self.bid_turn_index]                                [count_2_lst[0]][0]
#                             found=True
                        # case 2.d
                        # 2-suit doesn't have J but both 1-suits have J
                        elif ((self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][count_1_lst[0]]                            [0].rank() == 'J') and                             (self.obj_half_dictn_of_cards_grouped[self.bid_turn_index][count_1_lst[1]]                            [0].rank() == 'J')):
                            # make bid of upto 15
                            #print('\nreached 315')
                            if self.bid_value_final<15:
                                self.bid_value=self.bid_value_final+1
                                # select higher card of 2-suit (no J in that suit)
                                self.trump_card=self.obj_half_dictn_of_cards_grouped[self.bid_turn_index]                                [count_2_lst[0]][-1]
#                             found=True
                        # case 2.e
                        # 2-suit does't have J and only 1 other J or no J at all
                        else:
                            # make bid of upto 14
                            #print('\nreached 326')
                            if self.bid_value_final<14:
                                self.bid_value=self.bid_value_final+1
                                # select higher card of 2-suit (no J in that suit)
                                self.trump_card=self.obj_half_dictn_of_cards_grouped[self.bid_turn_index]                                [count_2_lst[0]][-1]
#                             found=True                     
                    else:
                        # len(count_1_lst) will be 4 in this case
                        #case1
                        ###################################################################                       
                        j_count2=0
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
                                    self.trump_card=self.obj_half_deal_lst[self.bid_turn_index]                                    [p_i_holder_lst[1]]
#                                 found=True
                            # case 1.c
                            # one J or no J in hand 
                            else:
                                # make bid of upto 14
                                #print('\nreached 390')
                                if self.bid_value_final<14:
                                    self.bid_value=self.bid_value_final+1
                                    # select card with highest point and not J(index=p_i_*lst[2])
                                    self.trump_card=self.obj_half_deal_lst[self.bid_turn_index]                                    [p_i_holder_lst[1]]
#                                 found=True
                        ###################################################################
                        # case 1 end ######################################################
            
            if self.bid_value>self.bid_value_final:
                self.bid_value_final=self.bid_value
                self.highest_bidder_index=self.bid_turn_index
                print('\n{} calls {}'.format(self.players_lst[self.bid_turn_index],self.bid_value_final))
                self.bid_turn_index=(self.bid_turn_index+1)%4
                self.bid_counter+=1
                self.bid_counter_lst.append(self.bid_counter)
                found=False
                count_1_lst.clear()
                count_2_lst.clear()               
            else:
                print('\n{} passes'.format(self.players_lst[self.bid_turn_index]))
                self.bid_turn_index=(self.bid_turn_index+2)%4
                self.bid_counter+=2
                self.bid_counter_lst.append(self.bid_counter)
                found=False
                count_1_lst.clear()
                count_2_lst.clear()
            
            # to stop bidding aft successive passes by team mates
            if (len(self.bid_counter_lst)>2) and ((self.bid_counter_lst[-1] - self.bid_counter_lst[-3])>3):
                break
        
        print('\n{} made the highest bid: {}'.format(self.players_lst[self.highest_bidder_index],                                                    self.bid_value_final))
        print('\n',self.bid_counter)
        
        # if player is not highest bidder i.e index!=0       
        if self.highest_bidder_index:
            self.trump_set=True
            self.trump_suit=self.trump_card.suit()
            self.trump_suit_index=self.suit.index(self.trump_suit)
            print('\nTrump card set by {}'.format(self.players_lst[self.highest_bidder_index]))
            
            # need to remove trump card from the obj_dictn_of_cards_grouped to make sure it is not 
            # played until trump is revealed
            self.obj_dictn_of_cards_grouped[self.highest_bidder_index]                                            [self.trump_suit_index].remove(self.trump_card)
        # if player is the highest bidder
        else:
            self.player_input=input('\nEnter the card for setting as trump:'
                +'\nrank followed by the first letter of the suit, eg.'
                +'\n7s or ah or 10d etc.: '
                +'\n(or 0 to stop game) ').lower()

            # trump input converted to object
            self.obj_trump_checked=self.trump_verify(self.player_input)
            self.trump_set=True
            self.trump_suit=self.obj_trump_checked.suit()
            self.trump_suit_index=self.suit.index(self.trump_suit)
            # storing the trump input to the variable used by all hands(from Prepare_game())
            self.trump_card=self.obj_trump_checked
            print('\nTrump card set by {}: {}'.format(self.players_lst[0],self.obj_trump_checked.form()))


        # displaying full hands
        self.obj_display_hands()

    ###################################################################
    # bid_half_hand() end #############################################
    
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
    
    #P4)
    # to insert the trump card back in highest bidder dictn once trump is revealed
    def insert_trump_card_back(self):
        leng=len(self.obj_dictn_of_cards_grouped[self.highest_bidder_index][self.trump_suit_index])
        if leng:
            for i in range(leng):
                itema=self.obj_dictn_of_cards_grouped[self.highest_bidder_index][self.trump_suit_index][i]
                if itema.point()>self.trump_card.point():
                    # insert at the position i
                    self.obj_dictn_of_cards_grouped[self.highest_bidder_index]                    [self.trump_suit_index].insert(i,self.trump_card)
                    break
                else:
                    if i!=leng-1:
                        continue
                    else:
                        # insert at the end
                        self.obj_dictn_of_cards_grouped[self.highest_bidder_index]                            [self.trump_suit_index].append(self.trump_card)
        else:
            # insert at the end, this will be the only element
            self.obj_dictn_of_cards_grouped[self.highest_bidder_index]                [self.trump_suit_index].append(self.trump_card)
            
    ###################################################################
    # insert_trump_card_back() end ####################################
            
    
    

