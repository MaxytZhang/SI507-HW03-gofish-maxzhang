import random

# SI 507 Fall 2018
# Homework 3 Extra- Fish Coding

class Card(object):
    suit_names =  ["Diamonds","Clubs","Hearts","Spades"]
    rank_levels = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    faces = {1:"Ace",11:"Jack",12:"Queen",13:"King"}

    def __init__(self, suit=0,rank=2):
        self.suit = self.suit_names[suit]
        if rank in self.faces: # self.rank handles printed representation
            self.rank = self.faces[rank]
        else:
            self.rank = rank
        self.rank_num = rank # To handle winning comparison

    def __str__(self):
        return "{} of {}".format(self.rank,self.suit)

class Deck(object):
    def __init__(self): # Don't need any input to create a deck of cards
        # This working depends on Card class existing above
        self.cards = []
        for suit in range(4):
            for rank in range(1,14):
                card = Card(suit,rank)
                self.cards.append(card) # appends in a sorted order

    def __str__(self):
        total = []
        for card in self.cards:
            total.append(card.__str__())
        # shows up in whatever order the cards are in
        return "\n".join(total) # returns a multi-line string listing each card

    def pop_card(self, i=-1):
        # removes and returns a card from the Deck
        # default is the last card in the Deck
        return self.cards.pop(i) # this card is no longer in the deck -- taken off

    def shuffle(self):
        random.shuffle(self.cards)

    def replace_card(self, card):
        card_strs = [] # forming an empty list
        for c in self.cards: # each card in self.cards (the initial list)
            card_strs.append(c.__str__()) # appends the string that represents that card to the empty list
        if card.__str__() not in card_strs: # if the string representing this card is not in the list already
            self.cards.append(card) # append it to the list

    def sort_cards(self):
        # Basically, remake the deck in a sorted way
        # This is assuming you cannot have more than the normal 52 cars in a deck
        self.cards = []
        for suit in range(4):
            for rank in range(1,14):
                card = Card(suit,rank)
                self.cards.append(card)
    
    def deal(self, number_hands, card_nums):
        result = []
        if card_nums == -1 or card_nums == 0:
            for i in range(0, number_hands):
                tmp = []
                result.append(tmp)
            return result
        else:
            for i in range(0, number_hands):
                tmp = []
                for j in range(0, card_nums):
                    num = random.randint(0, len(self.cards)-1)
                    card = self.pop_card(num)
                    tmp.append(card)
                result.append(tmp)
            return result

class Hand(object):
    def __init__(self, init_cards, name):
        self.cards = init_cards[:]
        self.name = name
        self.face = []
        self.face_number = 0

    def add_card(self, card):
        card_strs = []
        for c in self.cards:
            card_strs.append(c.__str__())
        if card.__str__() not in card_strs:
            self.cards.append(card)


    def remove_card(self, card):
        card_strs = []
        for c in self.cards:
            card_strs.append(c.__str__())
        if card.__str__() in card_strs:
            return self.cards.pop(card_strs.index(card.__str__()))
        else:
            return None

    def draw(self, deck):
        card = deck.pop_card()
        self.add_card(card)


    def remove_pairs(self):
        # pair are two with equal rank
        card_rank = []
        for card in self.cards:
            card_rank.append(card.rank)

        use_rank = []
        for rank in card_rank:
            c = card_rank.count(rank)
            if c % 2 == 1:
                if rank not in use_rank:
                    use_rank.append(rank)
    
        tmp = []
        for rank in use_rank:
            for card in self.cards:
                if card.rank == rank:
                    tmp.append(card)
                    break
        self.cards = tmp

    def book(self):
        card_status = []
        cards_copy = self.cards[:]
        card_number = len(self.cards)
        for i in range(card_number):
            card_status.append(True)
        for i in range(card_number):
            count = 1
            count_list = [i]
            for j in range(i + 1, card_number):
                if cards_copy[i].rank == cards_copy[j].rank:
                    count = count + 1
                    count_list.append(j)
            if count == 4:
                for c in count_list:
                    card_status[c] = False
                print("%s is in the book" % cards_copy[i].rank)
                self.face_number = self.face_number + 1
        for i in range(card_number):
            if not card_status[i]:
                self.face.append(self.remove_card(cards_copy[i]))

    def check(self, card):
        card_ranks = []
        for c in self.cards:
            if c.rank not in card_ranks:
                card_ranks.append(c.rank)
        if card.rank in card_ranks:
            return True
        else:
            return False

    def transfer_card(self, card):
        card_list = []
        for i in range(len(self.cards)-1, -1, -1):
            if self.cards[i].rank == card.rank:
                card_list.append(self.cards[i])
                self.remove_card(self.cards[i])
        return card_list


def player_turn(a, b, deck):
    if len(a.cards) == 0:
        return
    print("%s's number: %d" % (a.name, len(a.cards)))
    print("This is %s's turn" % a.name)
    print("%s please choose a random rank in your hand" % a.name)
    if len(a.cards) > 1:
        num1 = random.randint(0, len(a.cards)-1)
    else:
        num1 = 0
    card1 = a.cards[num1]
    print("%s chooses: %s" % (a.name, str(card1.rank)))
    if b.check(card1):
        print("%s have the card(s) with the same rank" % b.name)
        list_card = b.transfer_card(card1)
        for c in list_card:
            a.add_card(c)
        print("%s add %d card(s) from %s" % (a.name, len(list_card), b.name))
        a.book()
        if len(a.cards) or len(b.cards) == 0:
            return
    else:
        print("%s doesn't have the card(s) with the same rank \n%s go fish" % (b.name, a.name))
        new_card = deck.pop_card()
        a.add_card(new_card)
        print("%s add %s in hand" % (a.name, new_card.rank))
        a.book()
        if len(a.cards) == 0:
            return
        if new_card.rank == card1.rank:
            print("The new card has the same rank, Player could get a new turn")
            player_turn(a, b, deck)
        else:
            print("%s's turn ends" % a.name)



def play_fish_game():
    # the defalut value of players is two and we simply use two player with default 7 cards.
    deck = Deck()
    deck.shuffle()
    deal = deck.deal(2, 7)
    player1 = Hand(deal[0], "player1")
    player2 = Hand(deal[1], "player2")
    i = 0    
    while len(player1.cards) != 0 or len(player2.cards) != 0:
        if i % 2 == 0:
            player_turn(player1, player2, deck)
            i = i + 1
            continue
        else:
            player_turn(player2, player1, deck)
            i = i + 1
            continue
    
    print("player1: %d, player2: %d" % (player1.face_number, player2.face_number))
    if player1.face_number > player2.face_number:
        print("player1 wins")
    elif player1.face_number == player2.face_number:
        print("Tie")
    else:
        print("player2 wins")

if __name__ == "__main__":
    play_fish_game()