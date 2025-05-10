from filehandler import FileHandler
from hash_function_collision.matching_card_number import MatchCardNumber


class HashFunctionCollision:
    @staticmethod
    def match_card_number(card_hash, last_4_digits, card_bin, directory_to_ser):
        if not card_hash:
            raise ValueError("Card hash information must not be empty")
        if not last_4_digits:
            raise ValueError("Last four digits information must not be empty")
        if not card_bin:
            raise ValueError("Card bin information must not be empty")
        if not (card_number := MatchCardNumber.card_number(card_hash, last_4_digits, card_bin)):
            raise Warning("Match card number operation failed")
        FileHandler.save_data(directory_to_ser, {"card_number" : card_number }, "w")
