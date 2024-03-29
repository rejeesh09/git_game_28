#########################################################################
#unfolder - finding and replacing unfolder with itself helps to unfold all the code.
from round_1 import Round_1
# Round_*1() class is where the first round of the game takes place(i.e. round1_play() method in Round_*1())
# so the round*1_play() method has to be called from Round_*2 and round*2_play() from Round_*3 and so on
########################################################################
from cards import Cards
#Cards() class is explicitly called in inp_parse_check_modified() to make card objects

import time
import sys
# sys used in inp_parse_check to exit 
# sys and time used in follow_logic to print played cards with delay before taking player inp

# added on 05/10/2022 since there is randomness in each round play and hence the card played
# in each round should be reloadable for debugging purposes
import random
import pickle
#########################################################################
class Round_2(Round_1):
    """
    Module/class where round*2 of game takes place.
    
    Methods:
            __init__()
            inp_parse_check_modified()
            round*2_lead_logic()
            round*2_follow_logic()
            round*2_play()
    
    __docu_end"""
    
    def __init__(self,hold,custom_deal,tkntr_rt):
        """
        __init__() method of Round_2.
        
        Arguments: 
                hold - type(bool)
                custom_deal - type(bool)
                tkntr_rt - type(Tkinter object - root window)
        
        Methods:
                Only inherited methods
        
        Attributes:
                Only inherited variables
        
        __docu_end"""
        
        self.hold=hold
        self.custom_deal=custom_deal
        self.tkntr_rt=tkntr_rt
        # don't think these arguments to be passed below have to be made self as done above.
        super().__init__(self.hold,self.custom_deal,self.tkntr_rt)
        # kind of creating an object instance of Round_1() class with the above __init__()
        super().round1_play()
        # similarly round*2_play(to be defined){as well as super().__init__()} 
        # can be called in __init__() of class Round_3(Round_2) and so on.
        
        
        #---------------edit-06102022----------------------------
        # scalable versions of all round specific variables used
        # only for variables/attributes and not methods
        # methods -> both round_* class methods and gui methods
        # the below set is to be repeated with modification in each round
        # others are defined in Round_1
        
        self.round_no = 2  
        self.round_cards[self.round_no] = {}
        
        #---------------edit-06102022----------------------------
        
        # the below statement is just for aesthetic purposes when code folding is used
        place_holder = 0
        
    ###################################################################
    #__init__() method end---------------------------------------------
    
    def inp_parse_check_modified(self,inp,which_suit):
        """
        This method in Round_2() class is a modification of inp_parse_check() in Round_1 and takes 
        as additional input the suit of the lead card in the round.
        This makes it easier to check validity of card in follow_logic rounds and was done separately 
        for not messing up the inp_parse_check method in round*1 which was left as it was.
        This is partly a result of broken/ad hoc/once in a while code development.
        It is to be used in the follow_logic()(follow_logic only) methods of round*2 and all subsequent rounds.
        
        Arguments:
                inp - type(str)
                which_suit - type(int)
        
        Methods:
                Only inherited methods

        Attributes:
                control_count - type(int)
                s_name_dict - type(dict)
                self.rnd - type(int)
                self.ld_suit_name - type(str)
                ...
                
        __docu_end"""
        
        # checks and converts the input to unicode and then to Card object        
        #import sys
        # to use sys.exit()
        control_count=0
        
        # modification made from inp_parse_check
        s_name_dict = {0:'spade',1:'hearts',2:'clubs',3:'diamonds'}
        self.rnd = which_suit
        self.ld_suit_name = s_name_dict[self.rnd]
        
        self.inp=inp
        self.inp_cpy=self.inp #??
        self.inp_cpy.strip(" ") # doesn't seem to work
        self.inp_cpy.replace(" ","") # this seems to work only for space inside the string
        ###############################################################
        if self.inp=='0':
        #1) to stop game by giving 0 as input; what's a better way? can't seem to do it w/o exception/tb
            try:
                sys.exit(0)
            except SystemExit as e:
                print('\nGame has been stopped\n')
                sys.tracebacklimit = None
                sys.exit(e)
        ###############################################################
        if self.inp_cpy.capitalize() not in self.legal_card_lst:
        #2) checkin for a legal card entry
            print('\nYou did not enter a valid card')
            self.player_input=input('\nEnter the card rank followed by the first letter of the suit, eg.' 
                +'\n7s or ah or 10d etc.: ').lower().strip()
            self.inp_parse_check_modified(self.player_input,self.rnd)
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
        if control_count==0:
            if self.inp_uni_obj not in self.obj_dictn_of_players_and_hand[self.player_name]:
            #3) played card not in hand
                print('\nEntered card not in hand')
                self.player_input=input('\nEnter the card rank followed by the first letter of the suit, eg.' 
                    +'\n7s or ah or 10d etc.: ').lower().strip()
                self.inp_parse_check_modified(self.player_input,self.rnd)
            elif (not self.trump_revealed) and (self.inp_uni_obj==self.trump_card):
            #4) if facedown card is played
                if self.round_no == 8:
                # allowed if round*8 is being played, i.e. only card left - added on 20/01/2023
                    control_count += 1
                else:
                    print('\nFace down card cannot be played unless revealed')
                    self.player_input=input('\nEnter the card rank followed by the first letter of the suit, eg.' 
                        +'\n7s or ah or 10d etc.: ').lower().strip()
                    self.inp_parse_check_modified(self.player_input,self.rnd)
            elif (self.highest_bidder_index==0) and (not len(self.obj_played_card_lst)) and \
                (self.inp_uni_obj.suit()==self.obj_trump_checked.suit()) and (not self.trump_revealed):
            #5) opening a round with trump by highest bidder(Player)
                if len(self.obj_deal_lst_copy[self.turn_index]) == \
                len(self.obj_dictn_of_cards_grouped[self.turn_index][self.trump_suit_index]):
                # allowed if only trump suit left in hand - added on 20/01/2023 p.s. this doesn't 
                # actually matter here as this method is called in only the follow_logic methods
                    control_count += 1
                else:
                    print('\nYou cannot play from trump suit now')
                    self.player_input=input('\nEnter the card rank followed by the first letter of the suit, eg.' 
                        +'\n7s or ah or 10d etc.: ').lower().strip()
                    self.inp_parse_check_modified(self.player_input,self.rnd)
            elif (len(self.obj_played_card_lst)) and (len(self.obj_dictn_of_cards_grouped[self.turn_index]\
                [self.rnd])) and (self.inp_uni_obj.suit()!=self.ld_suit_name):
            #6) lead suit in hand but played another card(this wouldn't apply for face down trump card
            # as it is separately taken care of)
                if self.turn_index == self.highest_bidder_index and \
                self.round_lead_suit_index[self.round_no] == self.trump_suit_index and \
                (len(self.obj_dictn_of_cards_grouped[self.turn_index]\
                [self.round_lead_suit_index[self.round_no]])) == 1:
                # this situation corresponds to the only card of the lead suit in hand being the face down
                # trump card, i.e. trump not revealed yet.
                    control_count+=1
                else:
                    print('\nYou have to play from the same suit as of lead card')
                    self.player_input=input('\nEnter the card rank followed by the first letter of the suit, eg.' 
                        +'\n7s or ah or 10d etc.: ').lower().strip()
                    self.inp_parse_check_modified(self.player_input,self.rnd)
            else:
                control_count+=1
        # returns the input, converted to Cards object
        return(self.inp_uni_obj)
    
    ###################################################################
    #inp_parse_check_modified() method end-----------------------------
       
    def round2_lead_logic(self):
        """
        Method for the leading hand in round*2.
        
        Arguments:
                nil
        
        Methods:
                Only inherited methods
        
        Attributes:
                self.turn_index - type(int)
                ...
        
        __docu_end"""
        
        self.turn_index=self.round_lead_index[self.round_no]
        
        if not self.turn_index:
        # i.e. player gets to start 
        
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            # round*2 gui window for taking lead card input(i.e. if self.player leading the round)
            self.player_input=self.gui_handle.gui_card_entry[self.round_no]()
            # the object gui_handle of the Widgets() class is created in Deck() class in 
            # deck.py module
            self.player_input=self.player_input.lower().strip()
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

            #15.######### var15
            self.round_lead_card[self.round_no]=self.inp_parse_check(self.player_input)
        else:
        # the strategy is changed from 05/10/2022
        # an option is chosen randomly and depending on the choice either the maximum- 
        # point card or the minimum point card or a completely random card is played
        
            # if not a debugging round
            if not self.hold and self.round_till_which_written <= self.round_no:
                option = random.choice([1,2,3])

                if option == 1:
                    # play the card with the max point, last one if multiple choices
                    mx=max(crdd.point() for crdd in self.obj_deal_lst_copy[self.turn_index])
                    for crdd in self.obj_deal_lst_copy[self.turn_index]:
                        if crdd.point()==mx:
                            self.round_lead_card[self.round_no]=crdd

                elif option == 2:
                    # play the card with the min point, last one if multiple choices
                    mi=min(crdd.point() for crdd in self.obj_deal_lst_copy[self.turn_index])
                    for crdd in self.obj_deal_lst_copy[self.turn_index]:
                        if crdd.point()==mi:
                            self.round_lead_card[self.round_no]=crdd

                else:
                    # play a random card from hand
                    crdd = random.choice(self.obj_deal_lst_copy[self.turn_index])
                    self.round_lead_card[self.round_no]=crdd               

            # debugging is going on
            else:
                # loading the previously played round*2 lead card
                f=open(self.cards_in_round_filenames[self.round_no],"rb")
                self.round_cards[self.round_no] = pickle.load(f)
                self.round_lead_card[self.round_no]=self.round_cards[self.round_no][self.turn_index]
                f.close()

        # adding lead card to round*_cards
        self.round_cards[self.round_no][self.turn_index] = self.round_lead_card[self.round_no]
        
        ###############################################################
                        
        # printing out the card played
        print('\n')
#         time.sleep(0.5)
        sys.stdout.write(self.players_lst[self.turn_index]+': ')
#         time.sleep(0.5)
        sys.stdout.write(self.round_lead_card[self.round_no].show())
        ###############################################################  
        
        
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # gui window for round*2 lead card
        self.gui_handle.gui_card_played[self.round_no](self.turn_index,self.round_lead_card[self.round_no])
        # the object gui_handle of the Widgets() class is created in Deck() class in 
        # deck.py module
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
        # adding inp to lst and dictionaries
        self.obj_played_card_lst.append(self.round_lead_card[self.round_no])
        self.obj_dictn_of_highest_card_and_turn['suit']=[self.turn_index,self.round_lead_card[self.round_no]]

        self.obj_dictn_of_played_card_and_player[self.players_lst[self.turn_index]]\
        .append(self.round_lead_card[self.round_no])

        self.obj_dictn_of_played_card_and_suit[self.round_lead_card[self.round_no].suit()].append(self.round_lead_card[self.round_no])
        
        # updating an additional dictionary from 18/09/2022
        self.obj_dictn_of_player_index_and_hand[self.turn_index].remove(self.round_lead_card[self.round_no])
        
        #16.######### var16
        self.round_lead_card_suit[self.round_no]=self.round_lead_card[self.round_no].suit()
        self.round_lead_suit_index[self.round_no]=self.suit_dictn[self.round_lead_card_suit[self.round_no]]
        #17.######### var17
        self.round_highest_point_sofar[self.round_no]=self.round_lead_card[self.round_no].point()
        
        #-----------------------edit-05102022--------------------------
        # incrementing the count of the suit of which the card is played
        self.cards_in_suit_so_far[self.round_lead_card_suit[self.round_no]] += 1
        #-----------------------edit-05102022--------------------------
        
        # removing card played from lst and dictn
        self.obj_deal_lst_copy[self.turn_index].remove(self.round_lead_card[self.round_no])
        self.obj_dictn_of_cards_grouped[self.turn_index]\
                                        [self.round_lead_suit_index[self.round_no]].remove(self.round_lead_card[self.round_no])    
    
    ###################################################################
    #round*2_lead_logic() method end-----------------------------------
      
    def round2_follow_logic(self,suit_played):
        
        # logic followed by turns_index 1,2 and 3
        self.x=suit_played
        self.card_found=True # currently no use for this
        self.i1=False
        self.i2=False
        self.i3=False
        self.i4=False
        found=False

        ############################################################
        # point_sofar was made a func since it could not be defined b/w if and elif statemets
        def point_sofar():
            return(sum(int(i.point()) for i in self.obj_played_card_lst))
        ############################################################
        #round*2_follow_logic()'s point_sofar() function end ########


        # round*2_follow_logic() main body###################################


        # turn_index!=0, i.e. engine to play
        if self.turn_index:
            
            # normal play - not last hand repeat for debugging
            if not self.hold and self.round_till_which_written <= self.round_no:
        
                # if played suit in hand
                if len(self.obj_dictn_of_cards_grouped[self.turn_index][self.x]) != 0:
                    #print('\nreached line 733')

                    #------------------------edits-05102022------------------              
                    option = random.choice([1,2])

                    # playing according to some logic - option 1
                    if option == 1:
                        #if only one card in hand, has to play that card
                        if len(self.obj_dictn_of_cards_grouped[self.turn_index][self.x]) == 1:
                            # playing the only card of the lead suit of the round
                            self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][self.x][-1]

                        # if someone has played trump in round
                        elif self.obj_dictn_of_highest_card_and_turn['trump']:

                            #if teammate played the highest trump
                            if abs(self.obj_dictn_of_highest_card_and_turn['trump'][0] \
                                   - self.turn_index) == 2:
                                # playing highest card of the lead suit of the round
                                self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][self.x][-1]
                            else:
                                # playing lowest card of the lead suit of the round
                                self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][self.x][0]

                        # if J played by teammate and trump has not been played
                        elif abs(self.obj_dictn_of_highest_card_and_turn['suit'][0] - self.turn_index) == 2 \
                        and self.obj_dictn_of_highest_card_and_turn['suit'][1].rank() == 'J':
                            # playing highest card of the lead suit of the round
                            self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][self.x][-1]

                        # if J in hand and less than 4 cards of suit played so far, then play the J
                        elif self.obj_dictn_of_cards_grouped[self.turn_index][self.x][-1].rank() == 'J' and \
                        self.cards_in_suit_so_far[self.round_lead_card[self.round_no].suit()] < 4:
                            # playing the J of the lead suit of the round
                            self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][self.x][-1]

                        # any other situation
                        else:
                            # playing lowest card of the lead suit of the round
                            self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][self.x][0]

                    # option 2 - playing randomly from the lead suit
                    else:
                        self.card_played = random.choice(self.obj_dictn_of_cards_grouped\
                                                         [self.turn_index][self.x])

                    # updating highest point in round, if applicable
                    if self.card_played.point() > self.round_highest_point_sofar[self.round_no]:
                        # updating highest point
                        self.round_highest_point_sofar[self.round_no]=self.card_played.point()
                        # updating dictionary of highest card and its turn
                        self.obj_dictn_of_highest_card_and_turn['suit'].clear()
                        self.obj_dictn_of_highest_card_and_turn['suit'].extend(\
                                                                [self.turn_index,self.card_played])                  

                    # removing played card from hand
                    self.obj_dictn_of_cards_grouped[self.turn_index][self.x].remove(self.card_played)
                    #------------------------edits-05102022------------------


                # if played suit not in hand
                else:

                    # play the card with the min point remaining in hand (last card if many)
                    mi=min(crdd.point() for crdd in self.obj_deal_lst_copy[self.turn_index])
                    for crdd in self.obj_deal_lst_copy[self.turn_index]:
                        if crdd.point()==mi:
                            self.card_played=crdd

    #                 self.card_played=self.obj_dictn_of_players_and_hand[self.players_lst[self.turn_index]][-1]
                    suit_name = self.card_played.suit()
                    suit_no = self.suit_dictn[suit_name]

                    # removing played card from hand
                    self.obj_dictn_of_cards_grouped[self.turn_index][suit_no].remove(self.card_played)
            
            # debugging is going on - last round repeat
            else:
                # loading the previously played round*2 card
                f=open(self.cards_in_round_filenames[self.round_no],"rb")
                self.round_cards[self.round_no] = pickle.load(f)
                self.card_played=self.round_cards[self.round_no][self.turn_index]
                f.close()
                
                # updating highest point in round, if applicable
                if (self.card_played.suit() == self.round_lead_card[self.round_no].suit()) and \
                (self.card_played.point() > self.round_highest_point_sofar[self.round_no]):
                    # updating highest point
                    self.round_highest_point_sofar[self.round_no]=self.card_played.point()
                    # updating dictionary of highest card and its turn
                    self.obj_dictn_of_highest_card_and_turn['suit'].clear()
                    self.obj_dictn_of_highest_card_and_turn['suit'].extend(\
                                                            [self.turn_index,self.card_played])                  

                suit_name = self.card_played.suit()
                suit_no = self.suit_dictn[suit_name]
                
                # removing played card from hand
                self.obj_dictn_of_cards_grouped[self.turn_index][suit_no].remove(self.card_played)
                #------------------------edits-------------------


        #---------------------------------------------------------------------------------------
        
        # turn_index==0, taking input
        else:
        # i.e self.turn_index==0
            # taking player input
            played=False
#             time.sleep(0.5)
            if not len(self.obj_dictn_of_cards_grouped[0][self.round_lead_suit_index[self.round_no]]):
            # played suit not in hand
                if not self.trump_revealed:

                    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                    # gui window display
                    # the gui disp method of Widget() class in widget_manager module is called by its object
                    # gui_handle which was created earlier in __init__() of Deck()
                    self.check_val=self.gui_handle.gui_trump_call_instance[self.round_no](self.turn_index)
                    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

                    if self.check_val:
                        self.trump_revealed=True
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        # gui window display
                        # the gui disp method of Widget() class in widget_manager module is called by its object
                        # gui_handle which was created earlier in __init__() of Deck()
                        self.gui_handle.gui_trump_reveal[self.round_no](self.turn_index,\
                                                                self.trump_card,self.highest_bidder_index)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

                        # inserting the trump card back into the highest bidder dictionary 
                        # (if not player)
                        if self.highest_bidder_index:
                            self.insert_trump_card_back()
                        
                        if len(self.obj_dictn_of_cards_grouped[0][self.trump_suit_index]):
                        # trump called and trump present
                            if self.turn_index==self.highest_bidder_index:
                            # player was highest bidder
#                                 input("\nHave to play trump card itself: 'Enter'")
                                self.card_played=self.trump_card
                                
                                # the below lines have been commented out, since gui_round*2_card_played 
                                # needs to be called only once and only at the end of this 
                                # follow_logic() method
                                #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                # gui window for round1 (follow card)
                                # self.gui_handle.gui_round*2_card_played(self.turn_index,self.card_played)
                                # the object gui_handle of the Widgets() class is created in Deck() 
                                # class in deck.py module
                                #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                
                            else:
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                # gui window for taking card input
                                self.player_input=self.gui_handle.gui_card_entry[self.round_no]()
                                self.player_input=self.player_input.lower().strip()
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                self.card_played=self.inp_parse_check_modified(self.player_input,self.x)
                                # making sure a trump is played
                                while (self.card_played.suit()!=self.trump_suit):
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                    # gui window for taking card input
                                    self.player_input=self.gui_handle.gui_card_entry[self.round_no]()
                                    self.player_input=self.player_input.lower().strip()
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                    self.card_played=self.inp_parse_check_modified(self.player_input,self.x)

                            self.trump_played_in_round=True
                            self.obj_dictn_of_highest_card_and_turn['trump'].clear()
                            self.obj_dictn_of_highest_card_and_turn['trump'].extend(\
                                                                        [self.turn_index,self.card_played])
                            played=True
                if not played:
                # trump is already revealed or trump called but no trump card in hand 
                # or trump not called                    
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                    # gui window for taking card input
                    self.player_input=self.gui_handle.gui_card_entry[self.round_no]()
                    self.player_input=self.player_input.lower().strip()
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                    
                    self.card_played=self.inp_parse_check_modified(self.player_input,self.x)
        
                    if self.trump_revealed and (self.card_played.suit==self.trump_suit):
                        self.trump_played_in_round=True
                        if self.card_played.point()>self.obj_dictn_of_highest_card_and_turn['trump']\
                                                                                            [1].point():
                            self.obj_dictn_of_highest_card_and_turn['trump'].clear()
                            self.obj_dictn_of_highest_card_and_turn['trump'].extend(\
                                                                        [self.turn_index,self.card_played])
            else:
                # played suit in hand                
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                # gui window for taking card input
                self.player_input=self.gui_handle.gui_card_entry[self.round_no]()
                self.player_input=self.player_input.lower().strip()
#                 print("player inp in round*2 is :",self.player_input)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

                self.card_played=self.inp_parse_check_modified(self.player_input,self.x)

                # updating highest point sofar - need to check if this has to be used from round*2
                # this is being updated only coz of doubt whether this has already been used to 
                # check conditions
                self.round_highest_point_sofar[self.round_no]=max(self.card_played.point(),self.round_highest_point_sofar[self.round_no])
#??????????????????????????????????????????????????????????????????????????????????
                # the below if statement did not have len() before was just if not self.obj_dic..
                # though the code had not thrown any error before with that line, it is being changed 
                # as it doesn't make any sense. come back and see if code throws error in this regard in
                # future
                if (not len(self.obj_dictn_of_highest_card_and_turn['suit'])) or \
                    (self.obj_dictn_of_highest_card_and_turn['suit'][1].point()<self.card_played.point()):
                    self.obj_dictn_of_highest_card_and_turn['suit']=[self.turn_index,self.card_played]
                    #print('\nreached line 845')
            
            # need to remove card from grouped_dictn
            self.obj_dictn_of_cards_grouped[self.turn_index]\
                    [self.suit_dictn[self.card_played.suit()]].remove(self.card_played)
        
        #---------------------------------------------------------------------------------------
        
        # adding card to round*2_cards for saving in file
        self.round_cards[self.round_no][self.turn_index] = self.card_played
        
        # adding card to played card lst
        self.obj_played_card_lst.append(self.card_played)

        # updating the two dictionaries(player and suit) for played card
        self.obj_dictn_of_played_card_and_player[self.players_lst[self.turn_index]]\
        .append(self.card_played)
        self.obj_dictn_of_played_card_and_suit[self.card_played.suit()]\
        .append(self.card_played)
        
        #-----------------------edit-05102022--------------------------
        # incrementing the count of the suit from which the card is played
        self.cards_in_suit_so_far[self.card_played.suit()] += 1
        #-----------------------edit-05102022--------------------------
        
        # updating an additional dictionary from 18/09/2022
        self.obj_dictn_of_player_index_and_hand[self.turn_index].remove(self.card_played)
        
        #print('\nreached line 847')
        
        # removing the card played from deal_lst_copy. it is already removed from grouped dictn
        self.obj_deal_lst_copy[self.turn_index].remove(self.card_played)

        
        # printing out the card played
        
        print('\n')
#         time.sleep(0.5)
        sys.stdout.write(self.players_lst[self.turn_index]+': ')
        # could have been acheived with print('name'+': ', end=' ') as well
#         time.sleep(0.5)
        sys.stdout.write(self.card_played.show())
        
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # gui window for round*2 (follow card)
        self.gui_handle.gui_card_played[self.round_no](self.turn_index,self.card_played)
        # the object gui_handle of the Widgets() class is created in Deck() class in 
        # deck.py module
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        # the below statements only purpose is to make the function look good when code folding 
        # is done. the last comment lines are shown when code-folded, so a harmless statement 
        # which is not comment solves that problem
        just_a_place_holder = 0
        
    ###################################################################
    #round*2_follow_logic() method end---------------------------------

    def round2_play(self):
                
        while(len(self.obj_played_card_lst)<4):

            # calling the round*2 lead_logic for the first turn
            if len(self.obj_played_card_lst)==0:                
                self.round2_lead_logic()

            # updating turn_index - this is actually the player index
            self.turn_index=(self.turn_index+1)%4 # to cycle through 0,1,2,3
            
            # updating turn_in_round_index
            self.turn_in_round_index=len(self.obj_played_card_lst)# not +1 since list index start from 0

            # calls the follow_logic by passing suit value of the lead suit
            self.round2_follow_logic(self.round_lead_suit_index[self.round_no])

        # writing all cards played in round together to file for debugging
        # each card can be accessed with turn_index from round_cards list which contains all cards in list
        # writing the cards to file only if all 4 cards in round has been played such that the previous 
        # file would stay even if the game stops mid round due to some reason
        if len(self.round_cards[self.round_no]) == 4:
            f=open(self.cards_in_round_filenames[self.round_no],"wb")
            pickle.dump(self.round_cards[self.round_no],f)
            f.close()
            
            # to keep a track of till which round the cards where written to 
            # file in case the game is stopped mid round
            self.round_till_which_written = self.round_no
        
        # determining round*3_lead_index
        if len(self.obj_dictn_of_highest_card_and_turn['trump'])==0:
            key = self.obj_dictn_of_highest_card_and_turn['suit'][0]
        else:
            key = self.obj_dictn_of_highest_card_and_turn['trump'][0]

        #self.round*3_lead_index=key
        #self.round*3_lead_player=self.players_lst[key]
        
        #--------------------------edit-06102022------------------------
        next_round = self.round_no + 1

        self.round_lead_index[next_round] = key
        self.round_lead_player[next_round] = self.players_lst[key]
        #--------------------------edit-06102022------------------------
        
        # calculating points scored by each team
        if key in [0,2]:
            self.point_player_team=sum(int(i.point()) for i in self.obj_played_card_lst)
            self.point_oppo_team=0
        else:
            self.point_oppo_team=sum(int(i.point()) for i in self.obj_played_card_lst)
            self.point_player_team=0
            
        # storing points for the whole game
        self.point_player_team_sofar += self.point_player_team
        self.point_oppo_team_sofar += self.point_oppo_team

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # gui window display
        # the gui disp method of Widget() class in widget_manager module is called by its object
        # gui_handle which was created earlier in __init__() of Deck()
        self.gui_handle.gui_summary[self.round_no](self.point_oppo_team,self.point_player_team,\
                                          self.round_lead_player[next_round])
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        time.sleep(0.5)
        print('\n')
        print(20*' '+'Mate:'+'{}'.format(self.obj_dictn_of_played_card_and_player['Mate'][1].show()))
        print('Oppo_left:'+'{}'.format(self.obj_dictn_of_played_card_and_player\
                                       ['Oppo_left'][1].show()),end=' ')
        print(21*' '+'Oppo_right:'+'{}'.format(self.obj_dictn_of_played_card_and_player\
                                               ['Oppo_right'][1].show()))
        print(20*' '+'{}:'.format(self.players_lst[0]),end=' ')
        print(self.obj_dictn_of_played_card_and_player[self.players_lst[0]][1].show())
        print("\nRound-2 - starting from {}, counter_clockwise: ".format\
              (self.players_lst[self.round_lead_index[self.round_no]]),end=' ')        
        for i in self.obj_played_card_lst:
            print(i.show(),end=' ')
        print('')
        print('\nround-3_lead_index: ',self.round_lead_index[next_round])
        print('\nPoints scored - Your_team:{} , Oppo_team:{}'.format(\
                                    self.point_player_team,self.point_oppo_team))
        
        #-----------------------------edit-07102022------------------------------
        c_list = [i.form_alpha_num() for i in self.obj_played_card_lst]
        lead = str(self.round_lead_index[self.round_no])
        wr_str = lead + ":" + " ".join(c_list) + "\n"
        
        gdf = open(self.game_data_file_name,'a')
        gdf.write(wr_str)

        gdf.writelines(["#round-3\n","#-------------------------\n"])
        gdf.close()
        
        #-----------------------------edit-07102022------------------------------
        
        # updating and clearing variables
        self.obj_played_card_lst_of_32.extend(self.obj_played_card_lst)
        self.obj_played_card_lst.clear()
        self.obj_dictn_of_highest_card_and_turn['suit'].clear()
        self.obj_dictn_of_highest_card_and_turn['trump'].clear()
        
    ###################################################################
    #round*2_play() method end-----------------------------------------
    

#######################################################################
#round_*2() class end--------------------------------------------------
