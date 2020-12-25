from round_1 import Round_1
# obj1=Round_1(True)
    
class Round_2(Round_1):
    def __init__(self,hold):
        self.hold=hold
        super().__init__(self.hold)
        # kind of creating an object instance of Round_1() class with the above __init__()
        super().round1_play()
        # similarly round2_play(to be defined){as well as __init__()} 
        # can be called in __init__() of Round_3() and so on.
    
    # methods to be defined in this class
    # round2_lead_logic()
    # round2_follow_logic()
    # round2_play()
