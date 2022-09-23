#########################################################################
from round_6 import Round_6
# Round_6() class is where the sixth round of the game takes place(i.e. round6_play() method in Round_6())
# so the round6_play() method has to be called from Round_7 and round7_play() from Round_8.
########################################################################
import time
import sys
# sys used in inp_parse_check to exit 
# sys and time used in follow_logic to print played cards with delay before taking player inp
#########################################################################
class Round_7(Round_6):
    def __init__(self,hold,custom_deal,tkntr_rt):
        self.hold=hold
        self.custom_deal=custom_deal
        self.tkntr_rt=tkntr_rt
        # don't think these arguments to be passed below have to be made self as done above.
        super().__init__(self.hold,self.custom_deal,self.tkntr_rt)
        # kind of creating an object instance of Round_5() class with the above __init__()
        super().round6_play()
        # similarly round7_play(to be defined){as well as super().__init__()}
        # can be called in __init__() of class Round_8(Round_7).
    
    # methods in this class are:
    # round7_lead_logic()
    # round7_follow_logic()
    # round7_play()
    

# #######################################################################
# #round_7() class end ##################################################
