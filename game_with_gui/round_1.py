########################################################################
from cards import Cards
# importing the class - Cards() since the class is explicitly called in the inp_parse_check() method 
# in Round_1()
# from deck import Deck ## Deck() class is not required explicitly in this module
# ######################################################################
########################################################################
from prepare_game import Prepare_game
########################################################################
import time
import sys
# sys used in inp_parse_check to exit 
# sys and time used in follow_logic to print played cards with delay before taking player inp
# search for the term unfolder using the find and replace option under the edit tab(f in comm mode) and 
# replace it with the same to get all the folded blocks of code unblocked. or else 
# searching using ctl-f will not yield results from the folded blocks
#######################################################################
class Round_1(Prepare_game):
    def __init__(self,hold,custom_deal,tkntr_rt):
#         self.hold=hold
#         self.custom_deal=custom_deal
        super().__init__(hold,custom_deal,tkntr_rt)
        # All 15 variables in init() and 6 out of 7 methods of Deck class and all 10 variables 
        # in init() of Prepare_game class are constructed by the above line
#         input("\nStart bidding: 'Enter' ")

        # calling the bid_half_hand method in Prepare_game()
        super().bid_half_hand(hold,custom_deal)
        # obj_display_hands(False) is called/included within(at the end of) bid_half_hand()
        
#         input("\nStart 2nd bidding: 'Enter' ")
        super().bid_full_hand()
    
#         print("\nprint for debug after bid_full_hand() call in __init__ of Round_1()\n")
        
        # redealing if trump_distrb_good() returns false
        # this has not been tested for errors
        while not super().trump_distrb_good():
            print('\nRedealing since only one team has trump cards')
            # hold and custom_deal are set to False since it's a redeal
            super().__init__(False,False)
            # keeping the same bid_turn_index as the last normal deal
            super().bid_half_hand(True,False)
            super().bid_full_hand() # added on 24/09/2022 - not tested
            
        #-----------------------edit-05102022--------------------------
        self.cards_in_suit_so_far = {'spade':0,'hearts':0,'clubs':0,'diamonds':0}
        #-----------------------edit-05102022--------------------------
        
        #---------------edit-06102022----------------------------
        # scalable verisions of all round specific variables used
        # only for variables/attributes and not methods
        # methods -> both round_* class methods and gui methods
        
        self.round_no = 1 
        
        self.round_cards = {}
        self.round_cards[self.round_no] = {}
        # self.round_cards is a dictionary of dictionaries
        # it is a more explicit information of who played which card in round than 
        # obj_played_card_list but mostly redundant as the info can anyways be inferred by using
        # round_lead_index. It is anyways being used to write to file cards in each round that 
        # is retrieved if game is being played in debug mode. Necessitated by the randomsness in 
        # play from round*2-7.
        
        
        self.round_lead_index = {}
        self.round_lead_index[self.round_no] = self.round1_lead_index # it comes from prepare_game()
        self.round_lead_player = {}
        self.round_lead_card = {}
        self.round_lead_card_suit = {}
        self.round_lead_suit_index = {}
        self.round_highest_point_sofar = {}
        
        # filenames for writing each round cards
        self.cards_in_round_filenames = {1:'./pickle_dump/round1_cards.dat',\
                                         2:'./pickle_dump/round2_cards.dat',\
                                         3:'./pickle_dump/round3_cards.dat',\
                                         4:'./pickle_dump/round4_cards.dat',\
                                         5:'./pickle_dump/round5_cards.dat',\
                                         6:'./pickle_dump/round6_cards.dat',\
                                         7:'./pickle_dump/round7_cards.dat',\
                                         8:'./pickle_dump/round8_cards.dat'}
        
        #---------------edit-06102022----------------------------
    
    ###################################################################
    def inp_parse_check(self,inp):
        """
        This method which takes the input string as argument is used to check the 
        validity of the input string in round*1(both lead and follow round) and 
        the lead_logic() of all subsequent rounds
        A different method defined in Round_2(), inp_parse_check_modified which takes an 
        additional input of the lead suit in the particular round as well is to be 
        used for varifying inp in follow_logic() of all subsequent rounds.
        """
        # checks and converts the input to unicode and then to Card object        
        #import sys
        # to use sys.exit()
        control_count=0
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
            self.inp_parse_check(self.player_input)
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
                self.inp_parse_check(self.player_input)
            elif (not self.trump_revealed) and (self.inp_uni_obj==self.trump_card):
            #4) if facedown card is played
                if self.round_no == 8:
                # allowed if round*8 is being played, i.e. only card left - added on 20/01/2023
                    control_count += 1
                else:
                    print('\nFace down card cannot be played unless revealed')
                    self.player_input=input('\nEnter the card rank followed by the first letter of the suit, eg.' 
                        +'\n7s or ah or 10d etc.: ').lower().strip()
                    self.inp_parse_check(self.player_input)
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
                    self.inp_parse_check(self.player_input)
            elif (len(self.obj_played_card_lst)) and (len(self.obj_dictn_of_cards_grouped[self.turn_index]\
                [self.round_lead_suit_index[self.round_no]])) and (self.inp_uni_obj.suit()!=self.round_lead_card_suit[self.round_no]):
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
                    self.inp_parse_check(self.player_input)
            else:
                control_count+=1
        # returns the input, converted to Cards object
        return(self.inp_uni_obj)

    ###################################################################
    #inp_parse_check() method end #####################################
    
    ###################################################################
    def round1_lead_logic(self):
        # logic for opening turn of round
        
        self.turn_index=self.round_lead_index[self.round_no]
#         self.turn_index=0
        
        ###############################################################
        if not self.turn_index:
        # i.e. player gets to start 
        
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            # round*1 gui window for taking lead card input(i.e. if self.player leading the round)
            self.player_input=self.gui_handle.gui_card_entry[self.round_no]()
            # the object gui_handle of the Widgets() class is created in Deck() class in 
            # deck.py module
            self.player_input=self.player_input.lower().strip()
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

            #15.######### var15
            self.round_lead_card[self.round_no]=self.inp_parse_check(self.player_input)
        else:
        # starting by other players - lead_logic for other players
#             input("\nStart game: 'Enter'")
            found=False
            
#             print("\nprint for debug in the beginning of round*1_lead_logic()\n")
            
            if self.turn_index==self.highest_bidder_index:
            # case1 - highest bidder himself starting

                if len(self.obj_dictn_of_cards_grouped[self.turn_index][self.trump_suit_index])>2:
                # case1.a - has 4 or more trump cards (including self.trump_card,(which wld be removed,
                # hence len > 2))
                    
#                     print("\nprint for debug in the applicable case in round*1_lead_logic()\n")
                    for keyy in self.obj_dictn_of_cards_grouped[self.turn_index]:
                        if len(self.obj_dictn_of_cards_grouped[self.turn_index][keyy])==1 \
                            and self.obj_dictn_of_cards_grouped[self.turn_index][keyy][0].rank()=='J':
                        # if a non-trump single J present
                            self.round_lead_card[self.round_no]=self.obj_dictn_of_cards_grouped[self.turn_index][keyy][0]
#                             print("\nprint for debug round*1_lead_logic() - lead_card found\n")
                            found=True
                            break
                    if not found:
                    # no single J found
                        for xn in self.obj_dictn_of_cards_grouped[self.turn_index]:
                            if len(self.obj_dictn_of_cards_grouped[self.turn_index][xn])==1 and \
                                self.obj_dictn_of_cards_grouped[self.turn_index][xn][0].rank()!='9':
                            # if there is any single card which is not 9(J already ruled out)
                                self.round_lead_card[self.round_no]=self.obj_dictn_of_cards_grouped[self.turn_index][xn][0]
                                found=True
                                break
                    if not found:
                    # no single J or non-9 single card found
#                         print('\n Checking for a non-trump J')
                        for crd in self.obj_deal_lst_copy[self.turn_index]:
                            if crd.suit()!=self.trump_suit and crd.rank()=='J':
                            # play any non-trump J present
                                self.round_lead_card[self.round_no]=crd
#                                 print('\n found a J')
                                found=True
                                break
                    if not found:
                    # no single J or non-9 single card or no J found
#                         print('\n playing first pointless card')
                        for crd in self.obj_deal_lst_copy[self.turn_index]:
                            if crd.suit()!=self.trump_suit and int(crd.point())==0:
                            # play the first pointless card
                                self.round_lead_card[self.round_no]=crd
#                                 print('\n found a pointless card')
                                found=True
                                break
                    if not found:
                    # no single J or non-9 single card or no J or no pointless card found
                        for crd in self.obj_deal_lst_copy[self.turn_index]:
                            if crd.suit()!=self.trump_suit and crd.rank()!='9':
                            # play any non-trump, non-9 card
                                self.round_lead_card[self.round_no]=crd
                                found=True
                                break
                    if not found:
                    # reaching here means that all non-trump cards present are 9's
                        for crd in self.obj_deal_lst_copy[self.turn_index]:
                            if crd.suit()!=self.trump_suit:
                            # play first non-trump 9
                                self.round_lead_card[self.round_no]=crd
                                found=True
                                break
                else:
                # case1.b - has less than 4 trump cards (including self.trump_card)
                    
                    for keyz in self.obj_dictn_of_cards_grouped[self.turn_index]:
                        if keyz!=self.trump_suit_index and (0<len(self.obj_dictn_of_cards_grouped\
                                [self.turn_index][keyz])<5) and \
                                self.obj_dictn_of_cards_grouped[self.turn_index][keyz][-1].rank()=='J':
                        # if a non-trump J of suit len < 5 present
                            self.round_lead_card[self.round_no]=self.obj_dictn_of_cards_grouped[self.turn_index][keyz][-1]
                            found=True
                            break
                    if not found:
                    # no suitable J found
                        for xn in self.obj_dictn_of_cards_grouped[self.turn_index]:
                            if xn!=self.trump_suit_index and \
                                len(self.obj_dictn_of_cards_grouped[self.turn_index][xn])>2:
                            # if there is any suit with len > 3 play the lowest in that suit
                                self.round_lead_card[self.round_no]=self.obj_dictn_of_cards_grouped[self.turn_index][xn][0]
                                found=True
                                break
                    if not found:
                    # no suitable J or len > 3 suit found
                        for xn in self.obj_dictn_of_cards_grouped[self.turn_index]:
                            if xn!=self.trump_suit_index and \
                                len(self.obj_dictn_of_cards_grouped[self.turn_index][xn])==1 and \
                                self.obj_dictn_of_cards_grouped[self.turn_index][xn][0].rank()!='9':
                            # if there is any single card which is not 9(J already ruled out) 
                                self.round_lead_card[self.round_no]=self.obj_dictn_of_cards_grouped[self.turn_index][xn][0]
                                found=True
                                break
                    if not found:
                    # no suitable J or len > 3 suit or non-9 single card found
                        for xn in self.obj_dictn_of_cards_grouped[self.turn_index]:
                            if xn!=self.trump_suit_index and \
                             (len(self.obj_dictn_of_cards_grouped[self.turn_index][xn])>1) and \
                             int(self.obj_dictn_of_cards_grouped[self.turn_index][xn][0].point())==0 and \
                             self.obj_dictn_of_cards_grouped[self.turn_index][xn][1].rank()!='9':
                            # any pointless card whose 2nd is not a 9
                                self.round_lead_card[self.round_no]=self.obj_dictn_of_cards_grouped[self.turn_index][xn][0]
                                found=True
                                break
                    if not found:
                    # reaches here if there are no pointless cards in hand
                        for crd in self.obj_deal_lst_copy[self.turn_index]:
                            if crd.suit()!=self.trump_suit and crd.rank()!='9':
                            # play the first non-trump,non-9 card
                                self.round_lead_card[self.round_no]=crd
                                break
            else:
            # case2 - not the highest bidder
                for crd in self.obj_deal_lst_copy[self.turn_index]:
                    if crd.rank()=='J' and len(self.obj_dictn_of_cards_grouped[self.turn_index]\
                        [self.suit_dictn[crd.suit()]])<5:
                    # J of the first suit with less than 5 cards
                    # no need to check for trump suit since not highest bidder
                        self.round_lead_card[self.round_no]=crd
                        found=True
                        break
                if not found:
                # i.e. no J's present or has 5 or more cards from the J suit
                    for ixdn in self.obj_dictn_of_cards_grouped[self.turn_index]:
                        if len(self.obj_dictn_of_cards_grouped[self.turn_index][ixdn])==1 and \
                            self.obj_dictn_of_cards_grouped[self.turn_index][ixdn][0].rank()!='9':
                        # if there is any single card which is not 9(J already ruled out)
                            self.round_lead_card[self.round_no]=self.obj_dictn_of_cards_grouped[self.turn_index][ixdn][0]
                            found=True
                            break
                if not found:
                # i.e. no suitable J or no suitable single card
                    for ixdn in self.obj_dictn_of_cards_grouped[self.turn_index]:
                        if len(self.obj_dictn_of_cards_grouped[self.turn_index][ixdn])==2 and \
                            int(self.obj_dictn_of_cards_grouped[self.turn_index][ixdn][-1].point())==0:
                        # if there is a set of 2 point less cards
                            self.round_lead_card[self.round_no]=self.obj_dictn_of_cards_grouped[self.turn_index][ixdn][0]
                            found=True
                            break
                if not found:
                # i.e. no suitable J,single card or pointless two cards
                    for ixdn in self.obj_dictn_of_cards_grouped[self.turn_index]:
                        if len(self.obj_dictn_of_cards_grouped[self.turn_index][ixdn])>2 and \
                            int(self.obj_dictn_of_cards_grouped[self.turn_index][ixdn][0].point())==0:
                        # if there is a pointless card in a set of len>2
                            self.round_lead_card[self.round_no]=self.obj_dictn_of_cards_grouped[self.turn_index][ixdn][0]
                            found=True
                            break
                if not found:
                # if none of the above, play the card with the min point
                    mi=min(crdd.point() for crdd in self.obj_deal_lst_copy[self.turn_index])
                    for crdd in self.obj_deal_lst_copy[self.turn_index]:
                        if crdd.point()==mi:
                            self.round_lead_card[self.round_no]=crdd
                            found=True
                            break
                    
        ###############################################################
                        
        # printing out the card played
        print('\n')
#         time.sleep(0.5)
        sys.stdout.write(self.players_lst[self.turn_index]+': ')
#         time.sleep(0.5)
        sys.stdout.write(self.round_lead_card[self.round_no].show())
        ###############################################################  
        
        
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # gui window for round*1 lead card
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
        
        # adding lead card to round*_cards
        self.round_cards[self.round_no][self.turn_index] = self.round_lead_card[self.round_no]
        
        # removing card played from lst and dictn
        self.obj_deal_lst_copy[self.turn_index].remove(self.round_lead_card[self.round_no])
        self.obj_dictn_of_cards_grouped[self.turn_index]\
                                        [self.round_lead_suit_index[self.round_no]].remove(self.round_lead_card[self.round_no])    
    ###################################################################
    #round*1_lead_logic() method end ###################################


    ###################################################################    
    def round1_follow_logic(self,suit_played):
        # logic followed by turns_index 1,2 and 3
        self.x=suit_played # type int
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
        #round*1_follow_logic()'s point_sofar() function end ########

        ############################################################
        # strategy1 - for J in hand and trump not played in round so far
        def strategy_scenario1():
            # if len() of suit < 5
            if len(self.obj_dictn_of_cards_grouped[self.turn_index][self.x])<5:
                #print('\nreached line 226')
                # storing the card in self.card_played, highest card(J)
                self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][self.x][-1]
                # updating highest point
                self.round_highest_point_sofar[self.round_no]=self.card_played.point()
                # updating dictionary of highest card and its turn
                self.obj_dictn_of_highest_card_and_turn['suit'].clear()
                self.obj_dictn_of_highest_card_and_turn['suit'].extend(\
                                                        [self.turn_index,self.card_played])
                # removing played card from hand
                self.obj_dictn_of_cards_grouped[self.turn_index][self.x].pop(-1)

            # if len() of suit > 4 but last turn
            elif len(self.obj_dictn_of_cards_grouped[self.turn_index][self.x]) in [5,6,7] and \
                len(self.obj_played_card_lst)==3:
                #print('\nreached line 241')
                # storing the card in self.card_played, highest card(J)
                self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][self.x][-1]
                # updating highest point
                self.round_highest_point_sofar[self.round_no]=self.card_played.point()
                # updating dictionary of highest card and its turn
                self.obj_dictn_of_highest_card_and_turn['suit'].clear()
                self.obj_dictn_of_highest_card_and_turn['suit'].extend(\
                                                        [self.turn_index,self.card_played])
                # removing played card from hand
                self.obj_dictn_of_cards_grouped[self.turn_index][self.x].pop(-1)

            # if len() of suit ==5 (but not last turn)and J,9 in hand, then you can play the 9, 
            # it could be mate who doesn't have the suit
            elif (len(self.obj_dictn_of_cards_grouped[self.turn_index][self.x])==5) and \
                (len(self.obj_played_card_lst)<3) and \
                (self.obj_dictn_of_cards_grouped[self.turn_index][self.x][-2].rank()=='9'):
                # <3 coz, can play J itself if 3
                #print('\nreached line 259')
                # storing card in self.card_played, 9
                self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][self.x][-2]
                # updating highest point
                self.round_highest_point_sofar[self.round_no]=self.card_played.point()
                # updating dictionary of highest card and its turn
                self.obj_dictn_of_highest_card_and_turn['suit'].clear()
                self.obj_dictn_of_highest_card_and_turn['suit'].extend(\
                                                        [self.turn_index,self.card_played])
                # removing played card from hand
                self.obj_dictn_of_cards_grouped[self.turn_index][self.x].pop(0)


            # if len() of suit 5 or more and not last turn and len() not 5 with J and 9 in hand
            else:
                #print('\nreached line 274')
                # storing card in self.card_played, lowest card
                self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][self.x][0]
                if self.card_played.point()>self.round_highest_point_sofar[self.round_no]:
                    # updating highest point
                    self.round_highest_point_sofar[self.round_no]=self.card_played.point()
                    # updating dictionary of highest card and its turn
                    self.obj_dictn_of_highest_card_and_turn['suit'].clear()
                    self.obj_dictn_of_highest_card_and_turn['suit'].extend(\
                                                            [self.turn_index,self.card_played])
                # removing played card from hand
                self.obj_dictn_of_cards_grouped[self.turn_index][self.x].pop(0)
        ############################################################   
        #round*1_follow_logic()'s strategy_scenario1() function end #

        ############################################################
        # strategy5 - suit not in hand but round secured by team
        def strategy_scenario5():
            # check for any single cards and play the highest which is not J and if 
            # more than one such case then first encountered case
            for i in range(4):
                if ((not self.trump_revealed) and (self.turn_index!=self.highest_bidder_index)) or \
                    ((self.trump_revealed) and \
                    (i!=self.suit.index(self.trump_suit))) or ((not self.trump_revealed) and \
                    (self.turn_index==self.highest_bidder_index) and (i!=self.suit.index(self.trump_suit))):
                    #making sure a trump card is not being 'let off' if trump revealed or if highest_bidder

                    # checking separately in the order of priority for single cards
                    # if the single card is 9
                    if len(self.obj_dictn_of_cards_grouped[self.turn_index][i])==1 and \
                          self.obj_dictn_of_cards_grouped[self.turn_index][i][0].rank()=='9':
                        #print('\nreached line 303')
                        # storing the card in self.card_played, only card
                        self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][i][0]
                        # highest point need not be updated since already a J is played
                        # and not playing from suit
                        # removing played card from hand
                        self.obj_dictn_of_cards_grouped[self.turn_index][i].pop(0)
                        self.i1=True
                        break

                    # if the single card is either A or 10 - checking separately from 9 
                    # to assign 2nd priority
                    elif len(self.obj_dictn_of_cards_grouped[self.turn_index][i])==1 and \
                    (self.obj_dictn_of_cards_grouped[self.turn_index][i][0].rank() in ['A','10']):
                        #print('\nreached line 317')
                        # storing the card in self.card_played, highest card
                        self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][i][0]
                        # highest point need not be updated
                        # removing played card from hand
                        self.obj_dictn_of_cards_grouped[self.turn_index][i].pop(0)
                        self.i1=True
                        break

                    # if the single card is one of K,Q,8,7 - checking separately to assign 3rd priority
                    elif len(self.obj_dictn_of_cards_grouped[self.turn_index][i])==1 and \
                        (self.obj_dictn_of_cards_grouped[self.turn_index][i][0].rank() in \
                        ['K','Q','8','7']):
                        #print('\nreached line 330')
                        # storing the card in self.card_played, highest card
                        self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][i][0]
                        # highest point need not be updated
                        # removing played card from hand
                        self.obj_dictn_of_cards_grouped[self.turn_index][i].pop(0)
                        self.i1=True
                        break

            # no suitable card has been found so far(J already played by team mate)
            if not self.i1:
                #print('\nreached line 341')
                for i in range(4):
                    if ((not self.trump_revealed) and (self.turn_index!=self.highest_bidder_index)) or \
                        ((self.trump_revealed) and \
                        i!=self.suit.index(self.trump_suit)) or ((not self.trump_revealed) and \
                        (self.turn_index==self.highest_bidder_index) and \
                        (i!=self.suit.index(self.trump_suit))):
                        #making sure a trump card is not being 'let off' if trump revealed or highest_bidder

                        # to remove empty list from comparison, .rank() may give error
                        if len(self.obj_dictn_of_cards_grouped[self.turn_index][i])!=0:
                            for j in range(len(self.obj_dictn_of_cards_grouped[self.turn_index][i])):

                                # selecting the first 9 encountered
                                if self.obj_dictn_of_cards_grouped[self.turn_index][i][j].rank()=='9':
                                    #print('\nreached line 353')
                                    self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][i][j]
                                    # highest point need not be updated
                                    # removing played card from hand
                                    self.obj_dictn_of_cards_grouped[self.turn_index][i].pop(j)
                                    self.i2=True
                                    break
                            # breaking from the outer loop as well if a card was found
                            if self.i2:
                                break
                if not self.i2:
                    for i in range(4):
                        if ((not self.trump_revealed) and (self.turn_index!=self.highest_bidder_index)) or \
                            ((self.trump_revealed) and \
                            i!=self.suit.index(self.trump_suit)) or ((not self.trump_revealed) and \
                            (self.turn_index==self.highest_bidder_index) and \
                            (i!=self.suit.index(self.trump_suit))):
                            #making sure trump card is not 'let off' if trump revealed or highest_bidder

                            # to remove empty list from comparison, .rank() may give error
                            if len(self.obj_dictn_of_cards_grouped[self.turn_index][i])!=0:
                                for j in range(len(self.obj_dictn_of_cards_grouped[self.turn_index][i])):

                                    # selecting the first A or 10 encountered
                                    if self.obj_dictn_of_cards_grouped[self.turn_index][i][j].rank() in \
                                     ['A','10']:
                                        #print('\nreached line 376')
                                        self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][i][j]
                                        # highest point need not be updated
                                        # removing played card from hand
                                        self.obj_dictn_of_cards_grouped[self.turn_index][i].pop(j)
                                        self.i2=True
                                        break
                                # breaking from the outer loop as well if a card was found
                                if self.i2:
                                    break
                if not self.i2:
                    for i in range(4):
                        if ((not self.trump_revealed) and (self.turn_index!=self.highest_bidder_index)) or \
                            ((self.trump_revealed) and \
                            i!=self.suit.index(self.trump_suit)) or ((not self.trump_revealed) and \
                            (self.turn_index==self.highest_bidder_index) and \
                            (i!=self.suit.index(self.trump_suit))):
                            #making sure trump card is not 'let off' if trump revealed or highest_bidder

                            # to remove empty list from comparison, .rank() may give error
                            if len(self.obj_dictn_of_cards_grouped[self.turn_index][i])!=0:
                                for j in range(len(self.obj_dictn_of_cards_grouped[self.turn_index][i])):

                                    # selecting the first K,Q,8,7 encountered
                                    if self.obj_dictn_of_cards_grouped[self.turn_index][i][j].rank() in \
                                     ['K','Q','8','7']:
                                        #print('\nreached line 399')
                                        self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][i][j]
                                        # highest point need not be updated
                                        # removing played card from hand
                                        self.obj_dictn_of_cards_grouped[self.turn_index][i].pop(j)
                                        self.i2=True
                                        break
                                # breaking from the outer loop as well if a card was found
                                if self.i2:
                                    break
        ############################################################
        #round*1_follow_logic()'s strategy_scenario5() function end #

        ############################################################
        # strategy6 - suit not in hand and unfavourable to call/play trump
        def strategy_scenario6():
            for i in range(4):
                if ((not self.trump_revealed) and (self.turn_index!=self.highest_bidder_index)) or \
                    ((self.trump_revealed) and \
                    i!=self.suit.index(self.trump_suit)) or ((not self.trump_revealed) and \
                    (self.turn_index==self.highest_bidder_index) and \
                    (i!=self.suit.index(self.trump_suit))):
                    #making sure trump card is not 'let off' if trump revealed or highest_bidder

                    # selecting a single card which is not J or 9
                    if len(self.obj_dictn_of_cards_grouped[self.turn_index][i])==1 and \
                          self.obj_dictn_of_cards_grouped[self.turn_index][i][0].rank() not in \
                          ['J','9']:
                        #print('\nreached line 424')
                        # storing the card in self.card_played, only card
                        self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][i][0]
                        # highest point need not be updated
                        # removing played card from hand
                        self.obj_dictn_of_cards_grouped[self.turn_index][i].pop(0)
                        self.i3=True
                        break

            # if no suitable single card found
            if not self.i3:
                for i in range(4):
                    if ((not self.trump_revealed) and (self.turn_index!=self.highest_bidder_index)) or \
                        ((self.trump_revealed) and \
                        i!=self.suit.index(self.trump_suit)) or ((not self.trump_revealed) and \
                        (self.turn_index==self.highest_bidder_index) and \
                        (i!=self.suit.index(self.trump_suit))):
                        #making sure trump card is not 'let off' if trump revealed or highest_bidder

                        # checking for a set of 2 that is not J along with another point card and  
                        # one among 9,A,10 along with a non-point card
                        if len(self.obj_dictn_of_cards_grouped[self.turn_index][i])==2 and \
                              self.obj_dictn_of_cards_grouped[self.turn_index][i][-1].rank() not in \
                              ['9','A','10'] and \
                              self.obj_dictn_of_cards_grouped[self.turn_index][i][0].rank() not in \
                              ['9','A','10']:
                            #print('\nreached line 447')
                            # storing the card in self.card_played, lower card
                            self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][i][0]
                            # highest point need not be updated
                            # removing played card from hand
                            self.obj_dictn_of_cards_grouped[self.turn_index][i].pop(0)
                            self.i3=True
                            break

            # if no single or double
            if not self.i3:
                for i in range(4):
                    if ((not self.trump_revealed) and (self.turn_index!=self.highest_bidder_index)) or \
                        ((self.trump_revealed) and \
                        i!=self.suit.index(self.trump_suit)) or ((not self.trump_revealed) and \
                        (self.turn_index==self.highest_bidder_index) and \
                        (i!=self.suit.index(self.trump_suit))):
                        #making sure a trump card is not being 'let off' if trump revealed or highest_bidr

                        # if len() 3 or more and suit of atleast 3 pointless cards
                        if len(self.obj_dictn_of_cards_grouped[self.turn_index][i])>2 and \
                              (self.obj_dictn_of_cards_grouped[self.turn_index][i][-1].rank() in \
                              ['Q','K','10']):
                            #print('\nreached line 467')
                            # storing the card in self.card_played, lower card
                            self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][i][0]
                            # highest point need not be updated
                            # removing played card from hand
                            self.obj_dictn_of_cards_grouped[self.turn_index][i].pop(0)
                            self.i3=True
                            break

            # if no single or double set or pointless suit found so far
            if not self.i3:
                for i in range(4):
                    if (self.trump_revealed==False) or ((self.trump_revealed==True) and \
                        i!=self.suit.index(self.trump_suit)) or ((not self.trump_revealed) and \
                        (self.turn_index==self.highest_bidder_index) and \
                        (i!=self.suit.index(self.trump_suit))):
                        #making sure a trump card is not being 'let off' if trump revealed or highest_bidr

                        # if len() 3 or more and either of list[1] not in [9,A,10] or list[-1]==J
                        if len(self.obj_dictn_of_cards_grouped[self.turn_index][i])>2 and \
                              ((self.obj_dictn_of_cards_grouped[self.turn_index][i][1].rank() not in \
                              ['9','A','10']) or \
                              (self.obj_dictn_of_cards_grouped[self.turn_index][i][-1].rank()=='J')):
                            #print('\nreached line 488')
                            # storing the card in self.card_played, lower card
                            self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][i][0]
                            # highest point need not be updated
                            # removing played card from hand
                            self.obj_dictn_of_cards_grouped[self.turn_index][i].pop(0)
                            self.i3=True
                            break

            # if no suitable cases found so far
            if not self.i3:
                #print('\nreached line 499')
                for i in range(4):
                    if ((not self.trump_revealed) and (self.turn_index!=self.highest_bidder_index)) or \
                        ((self.trump_revealed) and \
                        i!=self.suit.index(self.trump_suit)) or ((not self.trump_revealed) and \
                        (self.turn_index==self.highest_bidder_index) and \
                        (i!=self.suit.index(self.trump_suit))):
                        #making sure a trump card is not being 'let off' if trump revealed or highest_bidr

                        # removing empty list from comparison
                        if len(self.obj_dictn_of_cards_grouped[self.turn_index][i])!=0:
                            for j in range(len(self.obj_dictn_of_cards_grouped[self.turn_index][i])):

                                # selecting the first non point card encountered
                                if self.obj_dictn_of_cards_grouped[self.turn_index][i][j].rank() in \
                                ['7','8','Q','K']:
                                    #print('\nreached line 512')
                                    self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][i][j]
                                    # highest point need not be updated
                                    # removing played card from hand
                                    self.obj_dictn_of_cards_grouped[self.turn_index][i].pop(j)
                                    self.i4=True
                                    break

                                # selecting the first A or 10 if no non point card available
                                elif self.obj_dictn_of_cards_grouped[self.turn_index][i][j].rank() in \
                                 ['A','10']:
                                    #print('\nreached line 523')
                                    self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][i][j]
                                    # highest point need not be updated
                                    # removing played card from hand
                                    self.obj_dictn_of_cards_grouped[self.turn_index][i].pop(j)
                                    self.i4=True
                                    break

                            # breaking from outer loop if card found
                            if self.i4: # checking if true
                                break
        ############################################################
        #round*1_follow_logic()'s strategy_scenario6() function end #

        ############################################################
        # strategy7a - calling trump but then trump suit not in hand
        def strategy_scenario7a():
            for i in range(4):
                # selecting a single card which is not J, 9, A or 10
                if len(self.obj_dictn_of_cards_grouped[self.turn_index][i])==1 and \
                      self.obj_dictn_of_cards_grouped[self.turn_index][i][0].rank() not in \
                      ['J','9','A','10']:
                    #print('\nreached line 545')
                    # storing the card in self.card_played, only card
                    self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][i][0]
                    # highest point need not be updated
                    # removing played card from hand
                    self.obj_dictn_of_cards_grouped[self.turn_index][i].pop(0)
                    self.i3=True
                    break

            # if no suitable single card found
            if not self.i3: # checking if false
                for i in range(4):
                    # checking for a set of 2 that is not J along with another point card and  
                    # one among 9,A,10 along with a non-point card
                    if len(self.obj_dictn_of_cards_grouped[self.turn_index][i])==2 and \
                          self.obj_dictn_of_cards_grouped[self.turn_index][i][-1].rank() not in \
                          ['9','A','10'] and \
                          self.obj_dictn_of_cards_grouped[self.turn_index][i][0].rank() not in \
                          ['9','A','10']:
                        #print('\nreached line 564')
                        # storing the card in self.card_played, lower card
                        self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][i][0]
                        # highest point need not be updated
                        # removing played card from hand
                        self.obj_dictn_of_cards_grouped[self.turn_index][i].pop(0)
                        self.i3=True
                        break

            # if no single or double
            if not self.i3: # checking if false
                for i in range(4):
                    # if len() 3 or more and suit of atleast 3 pointless cards
                    if len(self.obj_dictn_of_cards_grouped[self.turn_index][i])>2 and \
                          (self.obj_dictn_of_cards_grouped[self.turn_index][i][-1].rank() in \
                          ['Q','K','10']):
                        #print('\nreached line 580')
                        # storing the card in self.card_played, lower card
                        self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][i][0]
                        # highest point need not be updated
                        # removing played card from hand
                        self.obj_dictn_of_cards_grouped[self.turn_index][i].pop(0)
                        self.i3=True
                        break

            # if no single or double set or pointless suit found so far
            if not self.i3: # checking if false
                for i in range(4):
                    # if len() 3 or more and either of list[1] not in [9,A,10] or list[-1]==J
                    if len(self.obj_dictn_of_cards_grouped[self.turn_index][i])>2 and \
                          ((self.obj_dictn_of_cards_grouped[self.turn_index][i][1].rank() not in \
                          ['9','A','10']) or \
                          (self.obj_dictn_of_cards_grouped[self.turn_index][i][-1].rank()=='J')):
                        #print('\nreached line 597')
                        # storing the card in self.card_played, lower card
                        self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][i][0]
                        # highest point need not be updated
                        # removing played card from hand
                        self.obj_dictn_of_cards_grouped[self.turn_index][i].pop(0)
                        self.i3=True
                        break

            # if no suitable cases found so far
            if not self.i3: # checking if false
                #print('\nreached line 608')
                for i in range(4):
                    # removing empty list from comparison
                    if len(self.obj_dictn_of_cards_grouped[self.turn_index][i])!=0:
                        for j in range(len(self.obj_dictn_of_cards_grouped[self.turn_index][i])):

                            # selecting the first non point card encountered
                            if self.obj_dictn_of_cards_grouped[self.turn_index][i][j].rank() in \
                            ['7','8','Q','K']:
                                #print('\nreached line 617')
                                self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][i][j]
                                # highest point need not be updated
                                # removing played card from hand
                                self.obj_dictn_of_cards_grouped[self.turn_index][i].pop(j)
                                self.i4=True
                                break

                            # selecting the first A or 10 if no non point card available
                            elif self.obj_dictn_of_cards_grouped[self.turn_index][i][j].rank() in \
                             ['A','10']:
                                #print('\nreached line 628')
                                self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][i][j]
                                # highest point need not be updated
                                # removing played card from hand
                                self.obj_dictn_of_cards_grouped[self.turn_index][i].pop(j)
                                self.i4=True
                                break

                        # breaking from outer loop if card found
                        if self.i4:#checking if true
                            break
        ############################################################
        #round*1_follow_logic()'s strategy_scenario7a() function end#

        ############################################################
        # strategy 7b - calling and playing trump
        def strategy_scenario7b():
            # only one trump available
            if len(self.obj_dictn_of_cards_grouped[self.turn_index][self.trump_suit_index])==1:
                # storing the card in self.card_played
                self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index]\
                [self.trump_suit_index][0]
                # updating dictionary of highest trump and its turn
                self.obj_dictn_of_highest_card_and_turn['trump'].clear()
                self.obj_dictn_of_highest_card_and_turn['trump'].extend(\
                                                        [self.turn_index,self.card_played])
                # removing played card from hand
                self.obj_dictn_of_cards_grouped[self.turn_index][self.trump_suit_index].pop(0)

            # only two trumps available
            if len(self.obj_dictn_of_cards_grouped[self.turn_index][self.trump_suit_index])==2:
                # if trump J available
                if self.obj_dictn_of_cards_grouped[self.turn_index][self.trump_suit_index][-1]\
                    .rank()=='J':
                    # play the card that is not J
                    # storing the card in self.card_played
                    self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index]\
                    [self.trump_suit_index][0]
                    # updating dictionary of highest trump and its turn
                    self.obj_dictn_of_highest_card_and_turn['trump'].clear()
                    self.obj_dictn_of_highest_card_and_turn['trump'].extend(\
                                                            [self.turn_index,self.card_played])
                    # removing played card from hand
                    self.obj_dictn_of_cards_grouped[self.turn_index][self.trump_suit_index].pop(0)
                # if J not available
                else:
                    # play the highest card
                    # storing the card in self.card_played
                    self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index]\
                    [self.trump_suit_index][-1]
                    # updating dictionary of highest trump and its turn
                    self.obj_dictn_of_highest_card_and_turn['trump'].clear()
                    self.obj_dictn_of_highest_card_and_turn['trump'].extend(\
                                                            [self.turn_index,self.card_played])
                    # removing played card from hand
                    self.obj_dictn_of_cards_grouped[self.turn_index][self.trump_suit_index].pop(-1)

            # if 3 or more trumps available
            if len(self.obj_dictn_of_cards_grouped[self.turn_index][self.trump_suit_index])>2:
                # if trump J available
                if self.obj_dictn_of_cards_grouped[self.turn_index][self.trump_suit_index][-1]\
                    .rank()=='J':
                    # play the lowest trump
                    # storing the card in self.card_played
                    self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index]\
                    [self.trump_suit_index][0]
                    # updating dictionary of highest trump and its turn
                    self.obj_dictn_of_highest_card_and_turn['trump'].clear()
                    self.obj_dictn_of_highest_card_and_turn['trump'].extend(\
                                                            [self.turn_index,self.card_played])
                    # removing played card from hand
                    self.obj_dictn_of_cards_grouped[self.turn_index][self.trump_suit_index].pop(0)

                # no J but 9 or A available
                elif self.obj_dictn_of_cards_grouped[self.turn_index][self.trump_suit_index]\
                    [-1].rank() in ['9','A']:
                    # play the 2nd in order
                    # storing the card in self.card_played
                    self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index]\
                    [self.trump_suit_index][-2]
                    # updating dictionary of highest trump and its turn
                    self.obj_dictn_of_highest_card_and_turn['trump'].clear()
                    self.obj_dictn_of_highest_card_and_turn['trump'].extend(\
                                                            [self.turn_index,self.card_played])
                    # removing played card from hand
                    self.obj_dictn_of_cards_grouped[self.turn_index][self.trump_suit_index].pop(-2)

                # no J or 9 or A
                else:
                    # play the highest trump available
                    # storing the card in self.card_played
                    self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index]\
                    [self.trump_suit_index][-1]
                    # updating dictionary of highest trump and its turn
                    self.obj_dictn_of_highest_card_and_turn['trump'].clear()
                    self.obj_dictn_of_highest_card_and_turn['trump'].extend(\
                                                            [self.turn_index,self.card_played])
                    # removing played card from hand
                    self.obj_dictn_of_cards_grouped[self.turn_index][self.trump_suit_index].pop(-1)
        ############################################################
        #round*1_follow_logic()'s strategy_scenario7b() function end#

# round*1_follow_logic() main body###################################

        # turn_index!=0, i.e. engine to play
        if self.turn_index:
        
            # if played suit in hand
            if len(self.obj_dictn_of_cards_grouped[self.turn_index][self.x]) != 0:
                #print('\nreached line 733')

                #Strategy scenario1 
                # J in hand and trump not played in round so far               
                if (self.obj_dictn_of_cards_grouped[self.turn_index][self.x][-1].rank()=='J') and\
                    (not self.trump_played_in_round):
                    #print('\nreached line 738')
                    strategy_scenario1()


                #Strategy scenario2 
                # trump not played and J already played by team mate,
                # (and hence playing 3rd or 4th turn) or highest trump played by team mate and 
                # J in hand or otherwise
                elif ((not self.trump_played_in_round) and (len(self.obj_played_card_lst)>1) and \
                    (self.obj_played_card_lst[(self.turn_in_round_index+2)%4].rank()=='J')) or \
                    ((self.trump_played_in_round) and (len(self.obj_played_card_lst)>1) and \
                    (self.obj_played_card_lst[(self.turn_in_round_index+2)%4] == \
                    self.obj_dictn_of_highest_card_and_turn['trump'][1])):
                    #print('\nreached line 749')
                    # storing the card in self.card_played, highest card
                    self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][self.x][-1]
                    # highest point need not be updated since already a J is played
                    # removing played card from hand
                    self.obj_dictn_of_cards_grouped[self.turn_index][self.x].pop(-1)

                #Strategy scenario3 
                # Last turn and highest card in hand(could happen when J was deliberately not played)
                elif (len(self.obj_played_card_lst)==3) and (not self.trump_played_in_round) and \
                    (self.obj_dictn_of_cards_grouped[self.turn_index][self.x][-1].point()>\
                    self.round_highest_point_sofar[self.round_no]):
                    #print('\nreached line 760')
                    # storing the card in self.card_played, highest card
                    self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][self.x][-1]
                    # updating highest point
                    self.round_highest_point_sofar[self.round_no]=self.card_played.point()
                    # updating dictionary of highest card and its turn
                    self.obj_dictn_of_highest_card_and_turn['suit'].clear()
                    self.obj_dictn_of_highest_card_and_turn['suit'].extend(\
                                                            [self.turn_index,self.card_played])
                    # removing played card from hand
                    self.obj_dictn_of_cards_grouped[self.turn_index][self.x].pop(-1)

                #Strategy scenario4 
                # no J and playing 1st(?) or 2nd turn
                else:
                    #print('\nreached line 774')                    
                    # storing card in self.card_played, lowest card
                    self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][self.x][0]
                    if self.card_played.point()>self.round_highest_point_sofar[self.round_no]:
                        # updating highest point
                        self.round_highest_point_sofar[self.round_no]=self.card_played.point()
                        # updating dictionary of highest card and its turn
                        self.obj_dictn_of_highest_card_and_turn['suit'].clear()
                        self.obj_dictn_of_highest_card_and_turn['suit'].extend(\
                                                                [self.turn_index,self.card_played])
                    # removing played card from hand
                    self.obj_dictn_of_cards_grouped[self.turn_index][self.x].pop(0)

            # if played suit not in hand - strategy scenarios 5,6 and 7
            else:
                
                #----------new situation added on 23/01/2023------------------------
                # if the highest bidder has only one trump card which is face down and
                # a trump round is going on, the engine_hand is currently calling trump and 
                # revealing and playing the face down trump card, which should not be done
                # so the below condition check is added
                if (self.turn_index == self.highest_bidder_index) and \
                (not self.trump_revealed) and (self.round_lead_card_suit[self.round_no] == self.trump_suit):
                    # playing the card with the min point remaining in hand (last card if many)
                    # without any other considerations of the suit or other factors 
                    # unlike other scenarios that have been more meticulously coded in round*1
                    
                    print(f'\nreached bug point')
                    mi=min(crdd.point() for crdd in self.obj_deal_lst_copy[self.turn_index])
                    for crdd in self.obj_deal_lst_copy[self.turn_index]:
                        if crdd.point()==mi:
                            self.card_played=crdd

                    print(f'\nself.card_played = {crdd.form()}')
                    suit_name = self.card_played.suit()
                    suit_no = self.suit_dictn[suit_name]

                    # removing played card from hand
                    self.obj_dictn_of_cards_grouped[self.turn_index][suit_no].remove(self.card_played)
                
                #-------------------------------------------------------------------

                #Strategy scenario5 - NOT CALLING/PLAYING TRUMP
                # J has already been played by team mate and no trump played so far
                # or last turn and highest card sofar(not necessarily J) played by team mate and no trump
                # in round or highest trump so far played by team mate (suit not in hand)
                # 1) these are favourable situations - no need to call or play trump
                
                elif ((len(self.obj_played_card_lst)>1) and \
                (self.obj_played_card_lst[(self.turn_in_round_index+2)%4].rank()=='J') and \
                (not self.trump_played_in_round)) or \
                ((not self.trump_played_in_round) and (len(self.obj_played_card_lst)==3) and \
                (self.obj_dictn_of_highest_card_and_turn['suit'][1] == \
                self.obj_played_card_lst[(self.turn_in_round_index+2)%4])) or \
                ((self.trump_played_in_round) and \
                 (self.obj_played_card_lst[(self.turn_in_round_index+2)%4] == \
                 self.obj_dictn_of_highest_card_and_turn['trump'][1])):
                    #print('\nreached line 805')
                    strategy_scenario5()

                #Strategy scenario6 - NOT CALLING/PLAYING TRUMP
                # points so far played is less than <1 
                # or points so far played >0 (suit not in hand) bt have no trump or no higher trump
                # ???????????????????????????????
                #  - but a player might still want to take control of the round for other reasons like 
                # wanting to start next round or to play out a suit etc. 
                # ???????????????????????????????
                #  - there might also be a higher trump available with player and point maybe >0
                # and can still happen to not want to play the higher trump
                # 2) unfavourable situation or/and helpless

                elif ((point_sofar()<1) or ((self.trump_played_in_round) and (point_sofar()>0) and \
                    (len(self.obj_dictn_of_cards_grouped[self.turn_index][self.suit.index(self.trump_suit)])==0))\
                    or ((self.trump_played_in_round) and (point_sofar()>0) and \
                    (self.obj_dictn_of_cards_grouped[self.turn_index][self.suit.index(self.trump_suit)]\
                     [-1].point()<self.obj_dictn_of_highest_card_and_turn['trump'][1].point()))):
                    #print('\nreached line 819')
                    strategy_scenario6()

                #Strategy scenario7 
                #i.e. ready to call and/or play trump
                
                else:
                    
                    # if either trump is not called yet, (so going to call) 
                    # or trump revealed but not played in round so far
                    
                    if (not self.trump_revealed) or \
                        ((self.trump_revealed) and (not self.trump_played_in_round)):
                        #print('\nreached line 821')
                        
                        # CALLING TRUMP
                        if not self.trump_revealed:
                            print('\n{} calls trump'.format(self.players_lst[self.turn_index]))
                            # now trump_suit and obj_trump_checked can be used freely
                            self.trump_revealed=True
                            print('\nRevealing trump, card set by {} was: {}'.format(\
                                        self.players_lst[self.highest_bidder_index],self.trump_card.show()))

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

                            # if highest bidder himself is revealing trump
                            # but this cannot happen in round*1 - why not? highest bidder is not the one 
                            # who starts the round
                            
                            if self.highest_bidder_index==self.turn_index:
                                self.trump_played_in_round=True
                                #print('\nreached line 822')
                                # playing the card that was set as trump
                                self.card_played=self.trump_card
                                # updating dictionary of highest trump and its turn
                                self.obj_dictn_of_highest_card_and_turn['trump'].clear()
                                self.obj_dictn_of_highest_card_and_turn['trump'].extend(\
                                                                        [self.turn_index,self.card_played])
                                # removing played card from hand
                                self.obj_dictn_of_cards_grouped[self.turn_index][self.trump_suit_index]\
                                .remove(self.card_played)
                                found=True
                        
                        if not found:

                            #Strategy scenario7a 
                            # no trump in hand - this is scenario6 repeat except not checking for trump suit                            
                            if len(self.obj_dictn_of_cards_grouped[self.turn_index][self.trump_suit_index])==0:
                                strategy_scenario7a()
                                
                            #Strategy scenario7b 
                            # trump in hand and has to play trump                            
                            else:
                                #print('\nreached line 824')
                                self.trump_played_in_round=True
                                strategy_scenario7b()
                    
                    #Strategy scenario7c 
                    # trump has already been played in round and has to play a trump that is higher                    
                    else:
                        #print('\nreached line 825')
                        for item in self.obj_dictn_of_cards_grouped[self.turn_index][self.trump_suit_index]:
                            if item.point()>self.obj_dictn_of_highest_card_and_turn['trump'][1].point():
                                #print('\nreached line 826')
                                # play the 1st higher trump available
                                # storing the card in self.card_played
                                self.card_played=item
                                # updating dictionary of highest trump and its turn
                                self.obj_dictn_of_highest_card_and_turn['trump'].clear()
                                self.obj_dictn_of_highest_card_and_turn['trump'].extend(\
                                                                        [self.turn_index,self.card_played])
                                # removing played card from hand
                                self.obj_dictn_of_cards_grouped[self.turn_index][self.trump_suit_index]\
                                .remove(item)
                                break
        
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
                                
                                # the below lines have been commented out, since gui_round*1_card_played 
                                # needs to be called only once and only at the end of this 
                                # follow_logic() method
                                #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                # gui window for round*1 (follow card)
                                # self.gui_handle.gui_round*1_card_played(self.turn_index,self.card_played)
                                # the object gui_handle of the Widgets() class is created in Deck() 
                                # class in deck.py module
                                #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                
                            else:
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                # gui window for taking card input
                                self.player_input=self.gui_handle.gui_card_entry[self.round_no]()
                                self.player_input=self.player_input.lower().strip()
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                self.card_played=self.inp_parse_check(self.player_input)
                                # making sure a trump is played
                                while (self.card_played.suit()!=self.trump_suit):
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                    # gui window for taking card input
                                    self.player_input=self.gui_handle.gui_card_entry[self.round_no]()
                                    self.player_input=self.player_input.lower().strip()
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                    self.card_played=self.inp_parse_check(self.player_input)

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
                    
                    self.card_played=self.inp_parse_check(self.player_input)
        
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
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

                self.card_played=self.inp_parse_check(self.player_input)

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
        #########################################################
        
        #------------------------edit-09102022-------------------------
        # adding played card to round*_cards
        # though the card is added to the dictionary here, it is not written to 
        # file as in other rounds, since round*1 is completely deterministic and no random 
        # play is involved. so when in debugging mode, the same set of cards would anyways be
        # played by engine if the player sticks to the same card as well
        self.round_cards[self.round_no][self.turn_index] = self.card_played
        
        #------------------------edit-09102022-------------------------
        
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
        
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # gui window for round*1 (follow card)
        self.gui_handle.gui_card_played[self.round_no](self.turn_index,self.card_played)
        # the object gui_handle of the Widgets() class is created in Deck() class in 
        # deck.py module
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        
    ###################################################################
    #round*1_follow_logic() method end #################################


    def round1_play(self):
        """
        Round*1 play method.
        
        Arguments:
                Nil
        
        Methods:
                Only inherited methods
                
        Attributes:
                self.round_till_which_written - type(int)
                ...
                
        __docu_end"""
                
        while(len(self.obj_played_card_lst)<4):
            
#             print("\nprint for debug in round*1_play() just before calling lead_logic()\n")
            # calling the round*1 lead_logic for the first turn
            if len(self.obj_played_card_lst)==0:                
                self.round1_lead_logic()

            # updating turn_index - this is actually the player index
            self.turn_index=(self.turn_index+1)%4 # to cycle through 0,1,2,3
            
            # updating turn_in_round_index
            self.turn_in_round_index=len(self.obj_played_card_lst)# not +1 since list index start from 0

            # calls the follow_logic by passing suit value of the lead suit
            self.round1_follow_logic(self.round_lead_suit_index[self.round_no])


        # determining round*2_lead_index
        if len(self.obj_dictn_of_highest_card_and_turn['trump'])==0:
            key = self.obj_dictn_of_highest_card_and_turn['suit'][0]
        else:
            key = self.obj_dictn_of_highest_card_and_turn['trump'][0]
        
        
        #----------------edit-06102022-------------------------------
        
        self.round_lead_player[self.round_no] = self.players_lst[self.round_lead_index[self.round_no]]
             
        next_round = self.round_no + 1

        self.round_lead_index[next_round] = key
        self.round_lead_player[next_round] = self.players_lst[key]
        #self.round*2_lead_index=key
        #self.round*2_lead_player=self.players_lst[key]
        
        #----------------edit-06102022-------------------------------
        
        # calculating points scored by each team
        if key in [0,2]:
            self.point_player_team=sum(int(i.point()) for i in self.obj_played_card_lst)
        else:
            self.point_oppo_team=sum(int(i.point()) for i in self.obj_played_card_lst)
            
        # storing points for the whole game
        self.point_player_team_sofar = self.point_player_team
        self.point_oppo_team_sofar = self.point_oppo_team

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # gui window display
        # the gui disp method of Widget() class in widget_manager module is called by its object
        # gui_handle which was created earlier in __init__() of Deck()
        self.gui_handle.gui_summary[self.round_no](self.point_oppo_team,self.point_player_team,\
                                          self.round_lead_player[next_round])
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        time.sleep(0.5)
        print('\n')
        print(20*' '+'Mate:'+'{}'.format(self.obj_dictn_of_played_card_and_player['Mate'][0].show()))
        print('Oppo_left:'+'{}'.format(self.obj_dictn_of_played_card_and_player\
                                       ['Oppo_left'][0].show()),end=' ')
        print(21*' '+'Oppo_right:'+'{}'.format(self.obj_dictn_of_played_card_and_player\
                                               ['Oppo_right'][0].show()))
        print(20*' '+'{}:'.format(self.players_lst[0]),end=' ')
        print(self.obj_dictn_of_played_card_and_player[self.players_lst[0]][0].show())
        print("\nRound-1 - starting from {}, counter_clockwise: ".format\
              (self.players_lst[self.round_lead_index[self.round_no]]),end=' ')        
        for i in self.obj_played_card_lst:
            print(i.show(),end=' ')
        print('')
        print('\nround-2_lead_index: ',self.round_lead_index[next_round])
        print('\nPoints scored - Your_team:{} , Oppo_team:{}'.format(\
                                    self.point_player_team,self.point_oppo_team))
        
        #-----------------------------edit-07102022------------------------------
        c_list = [i.form_alpha_num() for i in self.obj_played_card_lst]
        lead = str(self.round_lead_index[self.round_no])
        wr_str = lead + ":" + " ".join(c_list) + "\n"
        
        gdf = open(self.game_data_file_name,'a')
        gdf.write(wr_str)

        gdf.writelines(["#round-2\n","#-------------------------\n"])
        gdf.close()
        
        #-----------------------------edit-07102022------------------------------
        
        #-----------------------------edit-09102022------------------------------
        # though round*_cards are not written to file in round*1, the variable below is being 
        # initialized here as it is being used from round*2
        self.round_till_which_written = self.round_no
        #-----------------------------edit-09102022------------------------------
        
        # updating and clearing variables
        self.obj_played_card_lst_of_32.extend(self.obj_played_card_lst)
        self.obj_played_card_lst.clear()
        self.obj_dictn_of_highest_card_and_turn['suit'].clear()
        self.obj_dictn_of_highest_card_and_turn['trump'].clear()
        ###############################################################
        #round*1_play() method end #####################################

#######################################################################
#round_*1() class end ##################################################
      
