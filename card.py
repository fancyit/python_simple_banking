from utils import Utils


class Card:
    balance = 0
    #
    # def __init__(self, num = None, pin = None, balance = 0):
    #     self.card_num = num
    #     self.card_pin = pin
    #     self.balance = balance

    def Issue(self):
        utils = Utils()
        self.card_num = utils.GenerateAccountNumber()
        self.card_pin = utils.GeneratePIN()
