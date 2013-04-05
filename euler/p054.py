
import pdb

VALUES = ("2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")
SUITS = ("C", "D", "H", "S")

RANKS = ("royalflush", "straightflush", "fourofakind", "fullhouse", "flush", "straight", "threeofakind", "twopairs", "onepair")

class Card(object):
    def __init__(self, value, suit):
        assert value in VALUES
        assert suit in SUITS
        self.value = value
        self.suit = suit
        
    def __hash__(self):
        return hash((self.suit, self.value))
        
    def __cmp__(self, other):
        return cmp(VALUES.index(self.value), VALUES.index(other.value))
    
    def __repr__(self):
        return "%s%s" % (self.value, self.suit)    

"""
    High Card: Highest value card.
    One Pair: Two cards of the same value.
    Two Pairs: Two different pairs.
    Three of a Kind: Three cards of the same value.
    Straight: All cards are consecutive values.
    Flush: All cards of the same suit.
    Full House: Three of a kind and a pair.
    Four of a Kind: Four cards of the same value.
    Straight Flush: All cards are consecutive values of same suit.
    Royal Flush: Ten, Jack, Queen, King, Ace, in same suit.
"""                                                
class HandError(Exception):
    pass


class Hand(list):
    R_OR, R_AND = range(2)

    def query(self, suit=None, value=None, reltype=None, rtype=None):
        if reltype is None:
            reltype = Hand.R_OR
            
        retval = []
        if value is None:
            values = []
        elif isinstance(value, (list, tuple, set)):
            values = value
        elif isinstance(value, basestring):
            values = [value]

        if suit is None:
            suits = []
        elif isinstance(suit, (list, tuple, set)):
            suits = suit
        elif isinstance(suit, basestring):
            suits = [suit]
            
            
        for card in self:
            if (reltype == Hand.R_OR and (card.suit in suits or card.value in values)) or \
               (reltype == Hand.R_AND and (card.suit in suits and card.value in values)):
                retval.append(card)
        if rtype == None:
            return Hand(retval)
        else:
            return rtype(retval)


    def has_royalflush(self):
        for suit in SUITS:
            hand = self.query(value=("T", "J", "Q", "K", "A"), suit=suit, reltype=Hand.R_AND)
            if len(hand) == 5:
                return hand

    def has_straightflush(self):
        if self.has_flush() and self.has_straight():
            return self
                    

    def has_fourofakind(self):
        for value in VALUES:
            hand = self.query(value=value)
            if len(hand) == 4:
                return hand
                
    def has_fullhouse(self):
        return self.has_threeofakind() and self.has_onepair()

        
    def has_flush(self):
        first = self[0]
        return len(self.query(suit=first.suit)) == 5
    
    def has_straight(self):
        values = sorted([VALUES.index(a.value) for a in self])
        exp = range(values[0], values[0]+5)
        return values == exp
    
    def has_threeofakind(self):
        for value in VALUES:
            hand = self.query(value=value)
            if len(hand) == 3:
                return hand

    def has_twopairs(self):
        for value in reversed(VALUES):
            hand = self.query(value=value)
            if len(hand) == 2:
                for value2 in reversed(VALUES):
                    if value2 != value:
                        hand2 = self.query(value=value2)
                        if len(hand2) == 2:
                            return hand2+hand
        
        
    def has_onepair(self):
        for value in reversed(VALUES):
            hand = self.query(value=value)
            if len(hand) == 2:
                return hand
    
    def has_highest(self):
        for value in reversed(VALUES):
            hand = self.query(value=value)
            if len(hand) > 0:
                return hand[0]
        


class Match(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def winner(self):
#        left, right = sorted(self.left), sorted(self.right)

        left, right = self.left,self.right
        
        for rank in RANKS:
            left_meth = getattr(left, "has_%s" % rank)
            right_meth = getattr(right, "has_%s" % rank)
            
            left_result = left_meth()
            right_result = right_meth()
    
            if not left_result and not right_result:
                continue
    
            if left_result and not right_result:
                print "L", left, right, rank, left_result
                return left
                
            if right_result and not left_result:
                print "R", left, right, rank, right_result
                return right
                
            if left_result and right_result:
                print "T", left, right, rank, left_result, right_result

                if rank == "onepair" or rank == "straightflush":
                    left_value = left_result[0].value
                    right_value = right_result[0].value
                    
                    if VALUES.index(left_value) > VALUES.index(right_value):
                        return left
                    elif VALUES.index(left_value) < VALUES.index(right_value):
                        return right
                    else:
                        print "FFFF", rank, left, right, left_value, right_value
#                        pdb.set_trace()
                        break
                    
    
        if VALUES.index(left.has_highest().value) > VALUES.index(right.has_highest().value):
            print "L", left, right, "N"
            return left
        elif VALUES.index(left.has_highest().value) < VALUES.index(right.has_highest().value):
            print "R", left, right, "N"
            return right
        else:
            print "QQQ"
            
        
            

counter = 0

for line in open("poker.txt"):
    game = line.strip().split(" ")
    
    left, right = game[:5], game[5:]

    lh = Hand([Card(x[0], x[1]) for x in left])
    rh = Hand([Card(x[0], x[1]) for x in right])
    
    m = Match(lh, rh)
    if m.winner() == lh:
        counter += 1
    
print "counter", counter
    