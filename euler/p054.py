
VALUES = ("2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")
SUITS = ("C", "D", "H", "S")
class Card(object):
    def __init__(self, value, suit):
        assert value in VALUES
        assert suit in SUITS
        self.value = value
        self.suit = suit
        
    def __hash__(self):
        return hash((self.suit, self.value))
        
    def __cmp__(self, other):
        return cmp(self.value, other.value)
        

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
    
    def query(self, suit=None, value=None, reltype=Hand.R_OR, rtype=Hand):
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
            
            
        for card in self.cards:
            if (reltype == Hand.R_OR and card.suit in suits or card.value in values) or \
               (reltype == Hand.R_AND and card.suit in suits and card.value in values):
                retval.append(card)
	return rtype(retval)

    def has_royalflush(self):
        for suit in SUITS:
            hand = self.query(value=("T", "J", "Q", "K", "A"), suit=suit, reltype=Hand.R_AND)
            if len(hand) == 5:
                return hand

    def has_straightflush(self):
        for suit in SUITS:
            for vidx in xrange(len(VALUES)-5):
                values = VALUES[vidx:vidx+5]
                hand = self.query(value=values, suit=suit, reltype=Hand.R_AND)
                if len(hand) == 5:
                    return hand
                    

    def has_fourofakind(self):
        for value in VALUES:
            hand = self.query(value=value)
            if len(hand) == 4:
                return hand
                
    def has_fullhouse(self):
        for value in VALUES:
            hand = self.query(value=value)
            if len(hand) == 3:
                rem = self[:]
                rem.remove(hand)    
                
        
            

for line in open("poker.txt"):
    game = line.strip().split(" ")
    
    left, right = game[:5], game[5:]
    print left, right
    