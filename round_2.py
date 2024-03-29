#########################################################################
from round_1 import Round_1
# Round_1() class is where the first round of the game takes place(i.e. round1_play() method in Round_1())
# so the round1_play() method has to be called from Round_2 and round2_play() from Round_3 and so on
#########################################################################
class Round_2(Round_1):
    def __init__(self,hold,custom_deal):
        self.hold=hold
        self.custom_deal=custom_deal
        # don't think the arguments passed have to be made self.
        super().__init__(self.hold,self.custom_deal)
        # kind of creating an object instance of Round_1() class with the above __init__()
        super().round1_play()
        # similarly round2_play(to be defined){as well as __init__()} 
        # can be called in __init__() of Round_3() and so on.
    
    # methods to be defined in this class
    # round2_lead_logic()
    # round2_follow_logic()
    # round2_play()
