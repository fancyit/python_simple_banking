from card import Card
from utils import Utils
import os, sqlite3


class MainMenu:
    db_exists = os.path.exists('card.s3db')  # if the db file exists on startup
    logged_in = False  # user logged_in ?
    utils = Utils()
    user_card = {}
    main_menu = {1: 'Create an account', 2: 'Log into account', 0: 'Exit'}
    loggedIn_menu = {
        1: 'Balance',
        2: 'Add income',
        3: 'Do transfer',
        4: 'Close account',
        5: 'Log out',
        0: 'Exit'
    }
    # db operations on start
    conn = sqlite3.connect('card.s3db', check_same_thread=False)
    cur = conn.cursor()
    if not db_exists:
        query = '''create table card(
                 id INTEGER PRIMARY KEY,
                 number TEXT,
                 pin TEXT,
                 balance INTEGER DEFAULT 0
                 )'''
        cur.execute(query)

    # handle login
    def handle_login(self):
        print("Enter your card number:\n>")
        user_card = input()
        print("Enter your PIN:")
        user_pin = input()
        self.cur.execute(self.utils.Sql_Select('*', 'card', f'number={user_card}'))
        self.user_card = self.cur.fetchone()
        if self.user_card and self.user_card[1] == user_card and self.user_card[2] == user_pin:
            self.logged_in = True
        if self.logged_in:
            print("You have successfully logged in!")
        else:
            print("Wrong card number or PIN!")

    # handle menu option
    def menu_options(self, option):
        if not self.logged_in:
            if option == 1:
                temp_card = Card()
                temp_card.Issue()
                self.cur.execute(f"""
                    insert into card (number, pin) values(
                    {temp_card.card_num},
                    {temp_card.card_pin}
                    )
                """)
                self.conn.commit()
                print("Your card number:")
                print(int(temp_card.card_num))
                print("Your card PIN:")
                print(temp_card.card_pin)
                self.print_menu()
            elif option == 2:
                self.handle_login()
                self.print_menu()
            else:
                print("You have successfully logged out!")
                #  commit changes to DB
                self.conn.close()
        else:
            if option == 1:
                self.cur.execute(self.utils.Sql_Select('*', 'card', f'number={self.user_card[1]}'))
                self.user_card = self.cur.fetchone()
                print(f"Balance: {self.user_card[3]} $")
                self.print_menu()
            elif option == 2:
                print('Enter income: ')
                income = int(input())
                self.cur.execute(f"""
                    update card
                    set balance = {income + int(self.user_card[3])}
                    where number = {self.user_card[1]}
                """)
                self.conn.commit()
                self.cur.execute(self.utils.Sql_Select('*', 'card', f'number={self.user_card[1]}'))
                self.user_card = self.cur.fetchone()
                print('Income was added!')
                self.print_menu()
            elif option == 3:
                print('Transfer')
                print('Enter card number: ')
                card_num = input()
                self.cur.execute(f"""
                    select * from card where number = {card_num}
                """)
                tmp_card = self.cur.fetchone()
                check = False
                if tmp_card:
                    check = self.utils.luhn_check(tmp_card[1])
                else:
                    print('Such a card does not exist.')
                    self.print_menu()
                if check:
                    print('Enter how much money you want to transfer:')
                    amount = int(input())
                    if (self.user_card[3] - amount < 0):
                        print('Not enough money!')
                        self.print_menu()
                    else:
                        amount_to_upd = amount + int(tmp_card[3])
                        self.cur.execute(f"""
                            update card
                            set balance={amount_to_upd} 
                            where number={tmp_card[1]}
                        """)
                        self.conn.commit()
                        self.cur.execute(f"""
                            update card
                            set balance = {self.user_card[3] - amount}
                            where number = {self.user_card[1]}
                        """)
                        self.conn.commit()
                        print('Success!')
                    self.print_menu()
                else:
                    print('Probably you made a mistake in the card number. Please try again!')
                    self.print_menu()
            elif option == 4:
                self.cur.execute(f"""
                    DELETE FROM card
                    WHERE number = {self.user_card[1]};    
                """)
                self.conn.commit()
                print('The account has been closed!')
                self.logged_in = False
                self.print_menu()
            elif option == 5:
                self.logged_in = False
                print("You have successfully logged out!")
                self.print_menu()
            else:
                print("You have successfully logged out!")
                #  commit changes to DB
                self.conn.close()

    # print the menu
    def print_menu(self):
        if not self.logged_in:
            menu = self.main_menu
        else:
            menu = self.loggedIn_menu
        for key, value in menu.items():
            print(f"{key}. {value}")
        print('> ')



