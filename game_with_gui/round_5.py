#########################################################################
#unfolder - finding and replacing unfolder with itself helps to unfold all the code.
from round_4 import Round_4
# Round_4() class is where the fourth round of the game takes place(i.e. round4_play() method in Round_4())
# so the round4_play() method has to be called from Round_5 and round5_play() from Round_6 and so on
########################################################################
import time
import sys
# sys used in inp_parse_check to exit 
# sys and time used in follow_logic to print played cards with delay before taking player inp
#########################################################################
class Round_5(Round_4):
    def __init__(self,hold,custom_deal,tkntr_rt):
        self.hold=hold
        self.custom_deal=custom_deal
        self.tkntr_rt=tkntr_rt
        # don't think these arguments to be passed below have to be made self as done above.
        super().__init__(self.hold,self.custom_deal,self.tkntr_rt)
        # kind of creating an object instance of Round_4() class with the above __init__()
        super().round4_play()
        # similarly round5_play(to be defined){as well as super().__init__()} 
        # can be called in __init__() of class Round_6(Round_5) and so on.
    
    # methods in this class are:
    # round5_lead_logic()
    # round5_follow_logic()
    # round5_play()
    
    def round5_lead_logic(self):
        # logic for opening turn of round
        
        self.turn_index=self.round5_lead_index
        
        ###############################################################
        if not self.turn_index:
        # i.e. player gets to start 
        
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            # round5 gui window for taking lead card input(i.e. if self.player leading the round)
            self.player_input=self.gui_handle.gui_round5_card_entry()
            # the object gui_handle of the Widgets() class is created in Deck() class in 
            # deck.py module
            self.player_input=self.player_input.lower()
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

            #15.######### var15
            self.round5_lead_card=self.inp_parse_check(self.player_input)
        else:
        # starting by other players - lead_logic for other players
        # just playing the maximum point card for now
#             input("\nStart game: 'Enter'")
#             found=False
            
#             if not found:
            # play the card with the max point
            mx=max(crdd.point() for crdd in self.obj_deal_lst_copy[self.turn_index])
            for crdd in self.obj_deal_lst_copy[self.turn_index]:
                if crdd.point()==mx:
                    self.round5_lead_card=crdd
#                     found=True
                    
        ###############################################################
                        
        # printing out the card played
        print('\n')
#         time.sleep(0.5)
        sys.stdout.write(self.players_lst[self.turn_index]+': ')
#         time.sleep(0.5)
        sys.stdout.write(self.round5_lead_card.show())
        ###############################################################  
        
        
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # gui window for round5 lead card
        self.gui_handle.gui_card_played5(self.turn_index,self.round5_lead_card)
        # the object gui_handle of the Widgets() class is created in Deck() class in 
        # deck.py module
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        # adding inp to lst and dictionaries
        self.obj_played_card_lst.append(self.round5_lead_card)
        self.obj_dictn_of_highest_card_and_turn['suit']=[self.turn_index,self.round5_lead_card]

        self.obj_dictn_of_played_card_and_player[self.players_lst[self.turn_index]]\
        .append(self.round5_lead_card)

        self.obj_dictn_of_played_card_and_suit[self.round5_lead_card.suit()].append(self.round5_lead_card)
        
        # updating an additional dictionary from 18/09/2022 - not used
        self.obj_dictn_of_player_index_and_hand[self.turn_index].remove(self.round5_lead_card)
        
        #16.######### var16
        self.round5_lead_card_suit=self.round5_lead_card.suit()
        self.round5_lead_suit_index=self.suit_dictn[self.round5_lead_card_suit]
        #17.######### var17
        self.round5_highest_point_sofar=self.round5_lead_card.point()
        
        # removing card played from lst and dictn
        self.obj_deal_lst_copy[self.turn_index].remove(self.round5_lead_card)
        self.obj_dictn_of_cards_grouped[self.turn_index]\
                                        [self.round5_lead_suit_index].remove(self.round5_lead_card)    
    ###################################################################
    #round5_lead_logic() method end ###################################
    
    
    ###################################################################    
    def round5_follow_logic(self,suit_played):
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
        #round5_follow_logic()'s point_sofar() function end ########


# round5_follow_logic() main body###################################

        # turn_index!=0, i.e. engine to play
        if self.turn_index:
        
            # if played suit in hand
            if len(self.obj_dictn_of_cards_grouped[self.turn_index][self.x]) != 0:
                #print('\nreached line 733')
                
                # if same team started the round
                if abs(self.round5_lead_index - self.turn_index) == 2:
                    
                    # playing highest card of the lead suit of the round
                    self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][self.x][-1]

                    # updating highest point in round, if applicable
                    if self.obj_dictn_of_cards_grouped[self.turn_index][self.x][-1].point()>\
                        self.round5_highest_point_sofar:
                        # updating highest point
                        self.round5_highest_point_sofar=self.card_played.point()
                        # updating dictionary of highest card and its turn
                        self.obj_dictn_of_highest_card_and_turn['suit'].clear()
                        self.obj_dictn_of_highest_card_and_turn['suit'].extend(\
                                                                [self.turn_index,self.card_played])
                
                # team player has not started the round
                else:
                    
                    # playing lowest card of the lead suit of the round
                    self.card_played=self.obj_dictn_of_cards_grouped[self.turn_index][self.x][0]
                    
                    # updating highest point in round, if applicable(this can happen if the lowest 
                    # card in hand is still higher the highest card so far)
                    if self.obj_dictn_of_cards_grouped[self.turn_index][self.x][0].point()>\
                        self.round5_highest_point_sofar:
                        # updating highest point
                        self.round5_highest_point_sofar=self.card_played.point()
                        # updating dictionary of highest card and its turn
                        self.obj_dictn_of_highest_card_and_turn['suit'].clear()
                        self.obj_dictn_of_highest_card_and_turn['suit'].extend(\
                                                                [self.turn_index,self.card_played])
                    
                
                # removing played card from hand
                self.obj_dictn_of_cards_grouped[self.turn_index][self.x].remove(self.card_played)
                

            # if played suit not in hand play min point card in hand
            else:
                
                # play the card with the min point remaining in hand (first card if many)
                mi=min(crdd.point() for crdd in self.obj_deal_lst_copy[self.turn_index])
                for crdd in self.obj_deal_lst_copy[self.turn_index]:
                    if crdd.point()==mi:
                        self.card_played=crdd
                
#                 self.card_played=self.obj_dictn_of_players_and_hand[self.players_lst[self.turn_index]][-1]
                suit_name = self.card_played.suit()
                suit_no = self.suit_dictn[suit_name]
                
                # removing played card from hand
                self.obj_dictn_of_cards_grouped[self.turn_index][suit_no].remove(self.card_played)

        #---------------------------------------------------------------------------------------
        
        # turn_index==0, taking input
        else:
        # i.e self.turn_index==0
            # taking player input
            played=False
#             time.sleep(0.5)
            if not len(self.obj_dictn_of_cards_grouped[0][self.round5_lead_suit_index]):
            # played suit not in hand
                if not self.trump_revealed:

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                    # gui window display
                    # the gui disp method of Widget() class in widget_manager module is called by its object
                    # gui_handle which was created earlier in __init__() of Deck()
                    self.check_val=self.gui_handle.gui_round5_trump_call_instance(self.turn_index)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

                    if self.check_val:
                        self.trump_revealed=True
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        # gui window display
                        # the gui disp method of Widget() class in widget_manager module is called by its object
                        # gui_handle which was created earlier in __init__() of Deck()
                        self.gui_handle.gui_round5_trump_reveal(self.turn_index,\
                                                                self.trump_card,self.highest_bidder_index)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        
                        if len(self.obj_dictn_of_cards_grouped[0][self.trump_suit_index]):
                        # trump called and trump present
                            if self.turn_index==self.highest_bidder_index:
                            # player was highest bidder
#                                 input("\nHave to play trump card itself: 'Enter'")
                                self.card_played=self.trump_card
                                
                                # the below lines have been commented out, since gui_card_played 
                                # needs to be called only once and only at the end of this 
                                # follow_logic() method
                                #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                # gui window for round1 (follow card)
                                # self.gui_handle.gui_card_played(self.turn_index,self.card_played)
                                # the object gui_handle of the Widgets() class is created in Deck() 
                                # class in deck.py module
                                #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                
                            else:
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                # gui window for taking card input
                                self.player_input=self.gui_handle.gui_round5_card_entry()
                                self.player_input=self.player_input.lower()
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                self.card_played=self.inp_parse_check_modified(self.player_input,self.x)
                                # making sure a trump is played
                                while (self.card_played.suit()!=self.trump_suit):
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                    # gui window for taking card input
                                    self.player_input=self.gui_handle.gui_round5_card_entry()
                                    self.player_input=self.player_input.lower()
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
                    self.player_input=self.gui_handle.gui_round5_card_entry()
                    self.player_input=self.player_input.lower()
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
                self.player_input=self.gui_handle.gui_round5_card_entry()
                self.player_input=self.player_input.lower()
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

                self.card_played=self.inp_parse_check_modified(self.player_input,self.x)

                # updating highest point sofar - need to check if this has to be used from round2
                # this is being updated only coz of doubt whether this has already been used to 
                # check conditions
                self.round5_highest_point_sofar=max(self.card_played.point(),self.round5_highest_point_sofar)
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
            
        # adding card to played card lst
        self.obj_played_card_lst.append(self.card_played)

        # updating the two dictionaries(player and suit) for played card
        self.obj_dictn_of_played_card_and_player[self.players_lst[self.turn_index]]\
        .append(self.card_played)
        self.obj_dictn_of_played_card_and_suit[self.card_played.suit()]\
        .append(self.card_played)
        
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
        # gui window for round5 (follow card)
        self.gui_handle.gui_card_played5(self.turn_index,self.card_played)
        # the object gui_handle of the Widgets() class is created in Deck() class in 
        # deck.py module
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
    ###################################################################
    #round5_follow_logic() method end #################################
    
    
    def round5_play(self):
        # round5_play() method  #######################################
                
        while(len(self.obj_played_card_lst)<4):

            # calling the round5 lead_logic for the first turn
            if len(self.obj_played_card_lst)==0:                
                self.round5_lead_logic()

            # updating turn_index - this is actually the player index
            self.turn_index=(self.turn_index+1)%4 # to cycle through 0,1,2,3
            
            # updating turn_in_round_index
            self.turn_in_round_index=len(self.obj_played_card_lst)# not +1 since list index start from 0

            # calls the follow_logic by passing suit value of the lead suit
            self.round5_follow_logic(self.round5_lead_suit_index)


        # determining round6_lead_index
        if len(self.obj_dictn_of_highest_card_and_turn['trump'])==0:
            key = self.obj_dictn_of_highest_card_and_turn['suit'][0]
        else:
            key = self.obj_dictn_of_highest_card_and_turn['trump'][0]

        self.round6_lead_index=key
        self.round6_lead_player=self.players_lst[key]
        
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
        self.gui_handle.gui_round5_summary(self.point_oppo_team,self.point_player_team,\
                                          self.round6_lead_player)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        time.sleep(0.5)
        print('\n')
        print(20*' '+'Mate:'+'{}'.format(self.obj_dictn_of_played_card_and_player['Mate'][4].show()))
        print('Oppo_left:'+'{}'.format(self.obj_dictn_of_played_card_and_player\
                                       ['Oppo_left'][4].show()),end=' ')
        print(21*' '+'Oppo_right:'+'{}'.format(self.obj_dictn_of_played_card_and_player\
                                               ['Oppo_right'][4].show()))
        print(20*' '+'{}:'.format(self.players_lst[0]),end=' ')
        print(self.obj_dictn_of_played_card_and_player[self.players_lst[0]][4].show())
        print("\nRound5 - starting from {}, counter_clockwise: ".format\
              (self.players_lst[self.round5_lead_index]),end=' ')        
        for i in self.obj_played_card_lst:
            print(i.show(),end=' ')
        print('')
        print('\nround6_lead_index: ',self.round6_lead_index)
        print('\nPoints scored - Your_team:{} , Oppo_team:{}'.format(\
                                    self.point_player_team,self.point_oppo_team))

        # updating and clearing variables
        self.obj_played_card_lst_of_32.extend(self.obj_played_card_lst)
        self.obj_played_card_lst.clear()
        self.obj_dictn_of_highest_card_and_turn['suit'].clear()
        self.obj_dictn_of_highest_card_and_turn['trump'].clear()
        ###############################################################
        #round5_play() method end #####################################
    

# #######################################################################
# #round_5() class end ##################################################
