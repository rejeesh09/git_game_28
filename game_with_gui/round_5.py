#########################################################################
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
        # kind of creating an object instance of Round_3() class with the above __init__()
        super().round4_play()
        # similarly round5_play(to be defined){as well as super().__init__()} 
        # can be called in __init__() of class Round_6(Round_5) and so on.
    
    # methods in this class are:
    # round5_lead_logic()
    # round5_follow_logic()
    # round5_play()
    

# #######################################################################
# #round_5() class end ##################################################
