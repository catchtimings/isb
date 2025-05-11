import multiprocessing as mp
import time

from filehandler import FileHandler
from hash_function_collision.diagram import construct_diagram
from hash_function_collision.matching_card_number import MatchCardNumber
from hash_function_collision.luhn_algorithm import LuhnAlgorithm


class HashFunctionCollision:
    @staticmethod
    def match_card_number(
        card_hash: str, last_4_digits: str, card_bin: tuple, directory_to_save: str
    ):
        if not card_hash:
            raise ValueError("Card hash information must not be empty")
        if not last_4_digits:
            raise ValueError("Last four digits information must not be empty")
        if not card_bin:
            raise ValueError("Card bin information must not be empty")
        if not (card_number := MatchCardNumber.card_number(card_hash, last_4_digits, card_bin)):
            raise Warning("Match card number operation failed")
        FileHandler.save_data(directory_to_save, {"card_number": card_number})

    @staticmethod
    def check_validate(card_number: str):
        if not card_number:
            raise ValueError("Card number info must not be empty")
        key = LuhnAlgorithm.luhn_algorithm(card_number)
        if key == card_number[-1]:
            return True
        return False

    @staticmethod
    def measuring_time(card_hash: tuple, last_4_digits: str, card_bin: str):
        if not card_hash:
            raise ValueError("Card hash information must not be empty")
        if not last_4_digits:
            raise ValueError("Last four digits information must not be empty")
        if not card_bin:
            raise ValueError("Card bin information must not be empty")
        cores = mp.cpu_count()
        measured_time = dict()
        for cores_ in range(1, int(1.5 * cores) + 1):
            start_time = time.time()
            print(f"Matching for {cores_} cores started")
            MatchCardNumber.card_number(card_hash, last_4_digits, card_bin, cores_)
            end_time = time.time()
            measured_time[str(cores_)] = end_time - start_time
        construct_diagram(measured_time)
