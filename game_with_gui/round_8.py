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
    
    # methods in this class are:
    # round*8_play()
    

# #######################################################################
# #round_*8() class end ##################################################
