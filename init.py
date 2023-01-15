from app import db

def create_standard_cards():
    suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
    ranks = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']

    for suit in suits:
        for rank in ranks:
            db.execute("INSERT INTO cards (suit, rank) VALUES (?, ?)", suit, rank)

create_standard_cards()
