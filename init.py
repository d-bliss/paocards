# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///xfinal.db")

def create_standard_cards():
    suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
    ranks = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']

    for suit in suits:
        for rank in ranks:
            db.execute("INSERT INTO cards (suit, rank) VALUES (?, ?)", suit, rank)

# check if the cards table is empty
if not db.execute("SELECT COUNT(*) FROM cards")[0]['COUNT(*)']:
    create_standard_cards()

from app import db