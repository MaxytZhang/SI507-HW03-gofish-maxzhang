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
        cards_copy = []
        card_number = len(self.cards)
        for card in self.cards:
            cards_copy.append(card)
        for i in range(card_number):
            count = 1
            count_list = [i]
            for j in range(i+1,card_number):
                if cards_copy[i].rank == cards_copy[j].rank:
                    count = count+1
                    count_list.append(j)
            if count == 4:
                for c in count_list:
                    self.face.append(self.remove_card(self.cards[c]))
                print(i + "is in the book")
                self.face_number = self.face_number+1

    def check(self, card):
        card_ranks = []
        for c in self.cards:
            card_ranks.append(c.rank)
        if card.rank in card_ranks:
            return True

    def transfer_card(self, card):
        card_list = []
        for c in self.cards:
            if c.rank == card.rank:
                card_list.append(c)
                self.remove_card(c)
        return card_list



def player_turn(player1, player2, deck):
    print("This is player1's turn")
    print("Player1 please choose a random rank in your hand")
    num1 = random.randint(0, len(player1.cards)-1)
    card1 = player1.cards[num1]
    print("Player1 chooses: " + str(card1.rank))
    if player2.check(card1):
        print("Player2 have the card(s) with the same rank")
        for c in player2.transfer_card(card1):
            player1.add_card(c)
        player1.book()
    else:
        print("Player2 doesn't have the card(s) with the same rank \n Player2 go fish")
        new_card2 = deck.pop_card()
        while new_card2.rank == card1.rank:
            print("The new card has the same rank, Player could get a new turn")
            new_card2 = deck.pop_card
        player2.add_card(new_card2)
    print("Player1' turn ends")

    print("This is player2's turn")
    print("Player2 please choose a random rank in your hand")
    num2 = random.randint(0, len(player2.cards)-1)
    card2 = player2.cards[num2]
    print("Player2 chooses: " + card2.rank)
    if player2.check(card2):
        print("Player1 have the card(s) with the same rank")
        for c in player1.transfer_card(card2):
            player2.add_card(c)
        player2.book()
    else:
        print("Player1 doesn't have the card(s) with the same rank \n Player1 go fish")
        new_card1 = deck.pop_card()
        while new_card1.rank == card1.rank:
            print("The new card has the same rank, Player could get a new turn")
            new_card1 = deck.pop_card
        player2.add_card(new_card1)
    print("Player2's turn ends")



def play_fish_game():
    # the defalut value of players is two and we simply use two player with default 7 cards.
    deck = Deck()
    deck.shuffle()
    deal = deck.deal(2, 7)
    player1 = Hand(deal[0], "player1")
    player2 = Hand(deal[1], "player2")
    player_turn(player1, player2, deck)
    i = 0
    '''while deck:
        if i % 2 == 0:
            player_turn(player1, player2, deck)
        else:
            player_turn(player2, player2, deck)
        i = i + 1
    '''

    # one question: how to deal "book"? I will remain that for you. better to have sth to store the score(number of book and pop the book in the hand)
    pass


    

def play_war_game(testing=False):
    # Call this with testing = True and it won't print out all the game stuff -- makes it hard to see test results
    player1 = Deck()
    player2 = Deck()

    p1_score = 0
    p2_score = 0

    player1.shuffle()
    player2.shuffle()
    if not testing:
        print("\n*** BEGIN THE GAME ***\n")
    for i in range(52):
        p1_card = player1.pop_card()
        p2_card = player2.pop_card()
        print('p1 rank_num=', p1_card.rank_num, 'p1 rank_num=', p2_card.rank_num)
        if not testing:
            print("Player 1 plays", p1_card,"& Player 2 plays", p2_card)

        if p1_card.rank_num > p2_card.rank_num:

            if not testing:
                print("Player 1 wins a point!")
            p1_score += 1
        elif p1_card.rank_num < p2_card.rank_num:
            if not testing:
                print("Player 2 wins a point!")
            p2_score += 1
        else:
            if not testing:
                print("Tie. Next turn.")

    if p1_score > p2_score:
        return "Player1", p1_score, p2_score
    elif p2_score > p1_score:
        return "Player2", p1_score, p2_score
    else:
        return "Tie", p1_score, p2_score

if __name__ == "__main__":
    play_fish_game()