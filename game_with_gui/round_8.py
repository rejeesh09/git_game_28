#########################################################################
#unfolder - finding and replacing unfolder with itself helps to unfold all the code.
from round_7 import Round_7
# Round_7() class is where the seventh round of the game takes place(i.e. round7_play() method in Round_7())
# so the round7_play() method has to be called from Round_8 and round8_play() from main code.
########################################################################
import time
import sys
# sys used in inp_parse_check to exit 
# sys and time used in follow_logic to print played cards with delay before taking player inp
#########################################################################
class Round_8(Round_7):
    def __init__(self,hold,custom_deal,tkntr_rt):
        self.hold=hold
        self.custom_deal=custom_deal
        self.tkntr_rt=tkntr_rt
        # don't think these arguments to be passed below have to be made self as done above.
        super().__init__(self.hold,self.custom_deal,self.tkntr_rt)
        # kind of creating an object instance of Round_7() class with the above __init__()
        super().round7_play()
        # round8_play() to be called from main code
    
    # methods in this class are:
    # round8_play()
    

# #######################################################################
# #round_8() class end ##################################################
