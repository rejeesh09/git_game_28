#!/usr/bin/env python
# coding: utf-8

# ## a. Cards()

# In[2]:



######################################################################
class Cards():
    def __init__(self,x):
        self.x=x
        
        # spade-\u2660, hearts-\u2665, clubs-\u2663, diamonds-\u2666
        self.suit_uni=['\u2660','\u2665','\u2663','\u2666']
        self.rank_er=['7','8','Q','K','10','A','9','J']
        
        # making the game deck of 32 cards
        # ['7♠', '8♠','Q♠',...,'9♦','J♦']
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
        return(self.x)
    
    def show(self):
        red_begin='\033[31m'
        red_end='\033[0m'
        if self.x.count('\u2665')!=0 or self.x.count('\u2666')!=0:
            return(red_begin+self.x+red_end)
        else:
            return(self.x)

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
        if self.x.count('7')!=0:
            return('7')
        if self.x.count('8')!=0:
            return('8')
        if self.x.count('Q')!=0:
            return('Q')
        if self.x.count('K')!=0:
            return('K')
        if self.x.count('10')!=0:
            return('10')
        if self.x.count('A')!=0:
            return('A')
        if self.x.count('9')!=0:
            return('9')
        if self.x.count('J')!=0:
            return('J')
    
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

