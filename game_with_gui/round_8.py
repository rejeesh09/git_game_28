#########################################################################
#unfolder - finding and replacing unfolder with itself helps to unfold all the code.
from round_7 import Round_7
# Round_*7() class is where the seventh round of the game takes place(i.e. round*7_play() method in Round_*7())
# so the round*7_play() method has to be called from Round_*8 and round*8_play() from main code.
########################################################################
import time
import sys
# sys used in inp_parse_check to exit 
# sys and time used in follow_logic to print played cards with delay before taking player inp

# added on 06/10/2022 since there is randomness in each round play and hence the card played
# in each round should be reloadable for debugging purposes
import random
import pickle
#########################################################################
class Round_8(Round_7):
    def __init__(self,hold,custom_deal,tkntr_rt):
        self.hold=hold
        self.custom_deal=custom_deal
        self.tkntr_rt=tkntr_rt
        # don't think these arguments to be passed below have to be made self as done above.
        super().__init__(self.hold,self.custom_deal,self.tkntr_rt)
        # kind of creating an object instance of Round_*7() class with the above __init__()
        super().round7_play()
        # round*8_play() to be called from main code
        
        self.round_no = 8  
        self.round_cards[self.round_no] = {}
        
#         #------------------------edit-07102022------------------------
#         # put the below lines of code wherever appropriate so that the game is successfully 
#         # finished by then
        
#         gc = open("game_counter.txt",'w')
#         gc.write(str(self.game_count))
#         gc.close()    
#         #------------------------edit-07102022------------------------
    
    
    def round8_lead(self):
        # opening turn of round*8
        # trump could still be uncalled and hence keeping the lead and follow methods separate even in 
        # round*8

        self.turn_index=self.round_lead_index[self.round_no]
        
        if self.turn_index == self.highest_bidder_index and not self.trump_revealed:
            self.trump_revealed=True
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            # gui window display
            # the gui disp method of Widget() class in widget_manager module is called by its object
            # gui_handle which was created earlier in __init__() of Deck()
            self.gui_handle.gui_trump_reveal[self.round_no](self.turn_index,\
                                                    self.trump_card,self.highest_bidder_index)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            if self.highest_bidder_index:
            # as the trump card is removed from the hands(obj_dictn_of_cards_grouped and
            # obj_deal_lst_copy) of only the engine
                self.insert_trump_card_back()
        
        
        self.round_lead_card[self.round_no] = self.obj_deal_lst_copy[self.turn_index][-1]
        
        # adding lead card to round*_cards
        self.round_cards[self.round_no][self.turn_index] = self.round_lead_card[self.round_no]


        # printing out the card played
        print('\n')
#         time.sleep(0.5)
        sys.stdout.write(self.players_lst[self.turn_index]+': ')
#         time.sleep(0.5)
        sys.stdout.write(self.round_lead_card[self.round_no].show())
        ###############################################################  

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # gui window for round*8 lead card
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

        self.round_lead_card_suit[self.round_no]=self.round_lead_card[self.round_no].suit()
        self.round_lead_suit_index[self.round_no]=self.suit_dictn[self.round_lead_card_suit[self.round_no]]
        
        self.round_highest_point_sofar[self.round_no]=self.round_lead_card[self.round_no].point()

        #-----------------------edit---------------------------
        # incrementing the count of the suit of which the card is played
        self.cards_in_suit_so_far[self.round_lead_card_suit[self.round_no]] += 1
        #-----------------------edit---------------------------

        # removing card played from lst and dictn
        self.obj_deal_lst_copy[self.turn_index].remove(self.round_lead_card[self.round_no])
        self.obj_dictn_of_cards_grouped[self.turn_index]\
                                        [self.round_lead_suit_index[self.round_no]].remove(self.round_lead_card[self.round_no])    
    ####################################################################
    #round*8_lead() method end #########################################
    
    
    ###################################################################    
    def round8_follow(self,suit_played):
        # round*8 follow play
        # trump call situation not included yet
        
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
        #round*8_follow()'s point_sofar() function end #############


        # round*8_follow() main body###################################


        # for all turns (engine as well as player) 
        if (self.turn_index == self.highest_bidder_index and not self.trump_revealed) or \
        (len(self.obj_dictn_of_cards_grouped[self.turn_index][self.x]) == 0 and not self.trump_revealed):
        # i.e. if engine_hand was the highest bidder or if played suit not in engine_hand
            self.trump_revealed=True
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            # gui window display
            # the gui disp method of Widget() class in widget_manager module is called by its object
            # gui_handle which was created earlier in __init__() of Deck()
            self.gui_handle.gui_trump_reveal[self.round_no](self.turn_index,\
                                                    self.trump_card,self.highest_bidder_index)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            if self.highest_bidder_index:
            # as the trump card is removed from the hands(obj_dictn_of_cards_grouped and
            # obj_deal_lst_copy) of only the engine
                self.insert_trump_card_back()


        self.card_played = self.obj_deal_lst_copy[self.turn_index][-1]
#         print(f'\nself.card_played = {self.card_played.form()}')

        # updating highest point in round, if applicable
        played_suit_ind = self.suit_dictn[self.card_played.suit()]
        if played_suit_ind == self.round_lead_card_suit[self.round_no]:
            if self.card_played.point() > self.round_highest_point_sofar[self.round_no]:
                # updating highest point
                self.round_highest_point_sofar[self.round_no]=self.card_played.point()
                # updating dictionary of highest card and its turn
                self.obj_dictn_of_highest_card_and_turn['suit'].clear()
                self.obj_dictn_of_highest_card_and_turn['suit'].extend(\
                                                        [self.turn_index,self.card_played])                  

        # removing played card from hand
#         print(f'\nself.obj_dictn_of_cards_grouped[{self.turn_index}][{played_suit_ind}] = \
#         {self.obj_dictn_of_cards_grouped[self.turn_index][played_suit_ind]}')
        self.obj_dictn_of_cards_grouped[self.turn_index][played_suit_ind].remove(self.card_played)
        #------------------------edits-------------------

        
        # adding card to round*8_cards for saving in file
        self.round_cards[self.round_no][self.turn_index] = self.card_played
        
        # adding card to played card lst
        self.obj_played_card_lst.append(self.card_played)

        # updating the two dictionaries(player and suit) for played card
        self.obj_dictn_of_played_card_and_player[self.players_lst[self.turn_index]]\
        .append(self.card_played)
        self.obj_dictn_of_played_card_and_suit[self.card_played.suit()]\
        .append(self.card_played)
        
        #-----------------------edit---------------------------
        # incrementing the count of the suit from which the card is played
        self.cards_in_suit_so_far[self.card_played.suit()] += 1
        #-----------------------edit---------------------------
        
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
        # gui window for round*7 (follow card)
        self.gui_handle.gui_card_played[self.round_no](self.turn_index,self.card_played)
        # the object gui_handle of the Widgets() class is created in Deck() class in 
        # deck.py module
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
    ####################################################################
    #round*8_follow() method end #######################################

    
    
    def round8_play(self):
    # round*8_play() method  #######################################
                
        while(len(self.obj_played_card_lst)<4):

            # calling the round*8 lead_logic for the first turn
            if len(self.obj_played_card_lst)==0:                
                self.round8_lead()

            # updating turn_index - this is actually the player index
            self.turn_index=(self.turn_index+1)%4 # to cycle through 0,1,2,3
            
            # updating turn_in_round_index
            self.turn_in_round_index=len(self.obj_played_card_lst)# not +1 since list index start from 0

            # calls the follow_logic by passing suit value of the lead suit
            self.round8_follow(self.round_lead_suit_index[self.round_no])

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
        
        # determining round*8_lead_index
        if len(self.obj_dictn_of_highest_card_and_turn['trump'])==0:
            key = self.obj_dictn_of_highest_card_and_turn['suit'][0]
        else:
            key = self.obj_dictn_of_highest_card_and_turn['trump'][0]

        
        #--------------------------edit------------------------
#         next_round = self.round_no + 1

#         self.round_lead_index[next_round] = key
#         self.round_lead_player[next_round] = self.players_lst[key]
        #--------------------------edit------------------------
        
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

        
        time.sleep(0.5)
        print('\n')
        print(20*' '+'Mate:'+'{}'.format(self.obj_dictn_of_played_card_and_player['Mate'][7].show()))
        print('Oppo_left:'+'{}'.format(self.obj_dictn_of_played_card_and_player\
                                       ['Oppo_left'][7].show()),end=' ')
        print(21*' '+'Oppo_right:'+'{}'.format(self.obj_dictn_of_played_card_and_player\
                                               ['Oppo_right'][7].show()))
        print(20*' '+'{}:'.format(self.players_lst[0]),end=' ')
        print(self.obj_dictn_of_played_card_and_player[self.players_lst[0]][7].show())
        print("\nRound-8 - starting from {}, counter_clockwise: ".format\
              (self.players_lst[self.round_lead_index[self.round_no]]),end=' ')        
        for i in self.obj_played_card_lst:
            print(i.show(),end=' ')
        print('')
        print('\nPoints scored - Your_team:{} , Oppo_team:{}'.format(\
                                    self.point_player_team,self.point_oppo_team))
        
        print('\nTotal points scored - Your_team:{} , Oppo_team:{}'.format(\
                                    self.point_player_team_sofar,self.point_oppo_team_sofar))
        
        # declaring result of game
        #---------------------------------------------------------------------------
        if self.bid2_any_call:
            point_needed = self.bid2_value_final
        else:
            point_needed = self.bid_value_final
            
        if (self.highest_bidder_index in [0,2] and self.point_player_team_sofar >= point_needed) or \
        (self.highest_bidder_index in [1,3] and self.point_oppo_team_sofar < point_needed):
            winner_indx = 0
            print('\nYour team won the game')
        else:
            winner_indx = 1
            print('\nOppo team won the game')
        #---------------------------------------------------------------------------
        
        
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # gui window display
        # the gui disp method of Widget() class in widget_manager module is called by its object
        # gui_handle which was created earlier in __init__() of Deck()
        self.gui_handle.gui_summary[self.round_no](self.point_oppo_team,self.point_player_team,\
                                          winner_indx,self.point_player_team_sofar)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        
    
        c_list = [i.form_alpha_num() for i in self.obj_played_card_lst]
        lead = str(self.round_lead_index[self.round_no])
        wr_str = lead + ":" + " ".join(c_list) + "\n"
        
        gdf = open(self.game_data_file_name,'a')
        gdf.write(wr_str)

        gdf.writelines(["#end\n","#-------------------------\n"])
        gdf.close()
        
        
        # updating and clearing variables
        self.obj_played_card_lst_of_32.extend(self.obj_played_card_lst)
        self.obj_played_card_lst.clear()
        self.obj_dictn_of_highest_card_and_turn['suit'].clear()
        self.obj_dictn_of_highest_card_and_turn['trump'].clear()
        ###############################################################
        #round*8_play() method end #####################################

    

# #######################################################################
# #round_*8() class end ##################################################
