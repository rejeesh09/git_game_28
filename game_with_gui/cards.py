######################################################################
class Cards():
    def __init__(self,x):
        # the argument x should be the alphanumeric-unicode combo of one of the 32 cards
        self.x=x
        
        # making a list, cards_no_colr=['7♠', '8♠','Q♠',...,'9♦','J♦']
        # this is done to have a .value() method which returns the index of 
        # the card in this list, which is used in sorting hands
        # - unicode for symbols, spade-\u2660, hearts-\u2665, clubs-\u2663, diamonds-\u2666
        self.suit_uni=['\u2660','\u2665','\u2663','\u2666']
        self.rank_er=['7','8','Q','K','10','A','9','J']                
        self.cards_no_colr=[]
        for y in self.suit_uni:
            self.cards_no_colr.extend([x+y for x in self.rank_er])
        
    ##################################################################
    # to make the objects hashable - to be used as dictionary key etc.
    def __hash__(self):
        return hash(str(self.x))
    ##################################################################
    # objects in Cards can now be compared or used with membership operators
    def __eq__(self,other):
        return self.x == other.x
    ##################################################################
    
    def form(self):
        """
        If the Cards object is made in standalone code, form() method returns whatever argument 
        is given to make the card object.
        But in the game Card objects are made by giving unicode arguments - so form() method in 
        game returns corresponding figure character for each suit
        """
        return(self.x)
    
    def form_alpha_num(self):
        """
        To return the alpha-numeric form of the card object
        """
        if self.x[0] == "1":
            val = "10"
        else:
            val = self.x[0]
        
        if self.x.count('\u2660')!=0:
            return(val+'s')
        if self.x.count('\u2665')!=0:
            return(val+'h')
        if self.x.count('\u2663')!=0:
            return(val+'c')
        if self.x.count('\u2666')!=0:
            return(val+'d')
    
    def show(self):
        red_begin='\033[31m'
        red_end='\033[0m'
        if self.x.count('\u2665')!=0 or self.x.count('\u2666')!=0:
            return(red_begin+self.x+red_end)
        else:
            return(self.x)
    
    def colour(self):
        if self.x.count('\u2665')!=0 or self.x.count('\u2666')!=0:
            return('red')
        else:
            return('black')

    def suit(self):
        if self.x.count('\u2660')!=0:
            return('spade')
        if self.x.count('\u2665')!=0:
            return('hearts')
        if self.x.count('\u2663')!=0:
            return('clubs')
        if self.x.count('\u2666')!=0:
            return('diamonds')
    
    def rank(self):
        """
        The method just returns the 1st character of the string argument used to create the object
        (except for 10). Earlier implementation was unnecessary and commented out, but revert if 
        any problem occurs.
        """
#         if self.x.count('7')!=0:
#             return('7')
#         if self.x.count('8')!=0:
#             return('8')
#         if self.x.count('Q')!=0:
#             return('Q')
#         if self.x.count('K')!=0:
#             return('K')
#         if self.x.count('10')!=0:
#             return('10')
#         if self.x.count('A')!=0:
#             return('A')
#         if self.x.count('9')!=0:
#             return('9')
#         if self.x.count('J')!=0:
#             return('J')
        if self.x[0] == '1':
            return(self.x[0]+'0')
        else:
            return(self.x[0])
    
    def point(self):
        if self.x.count('7')!=0:
            return(0.01)
        if self.x.count('8')!=0:
            return(0.02)
        if self.x.count('Q')!=0:
            return(0.03)
        if self.x.count('K')!=0:
            return(0.04)
        if self.x.count('10')!=0:
            return(1.00)
        if self.x.count('A')!=0:
            return(1.01)
        if self.x.count('9')!=0:
            return(2.00)
        if self.x.count('J')!=0:
            return(3.00)
        
    def value(self):
        return self.cards_no_colr.index(self.x)
