from functools import partial
import hashlib
import multiprocessing as mp
from tqdm import tqdm

from hash_function_collision.hfc_const import *


class MatchCardNumber:
    @staticmethod
    def card_number(card_hash, last_4_digits, card_bin):
        cores = mp.cpu_count()
        start_range, end_range = MatchCardNumber.card_range(card_bin, last_4_digits)
        with mp.Pool(processes=cores) as p:
            func = partial(MatchCardNumber.compare_with_hash, card_hash)
            for result in p.map(func, tqdm(range(start_range, end_range + 1, SHIFT))):
                if result:
                    return result
        return None

    @staticmethod
    def card_range(card_bin, last_4_digits):
        start_range = int((card_bin[0] + str(START_VALUE)[BIN_LENGTH:])[:-LAST_FOUR_LENGTH]+ last_4_digits)
        end_range = int(card_bin[1] + (str(END_VALUE)[:-LAST_FOUR_LENGTH] + last_4_digits)[BIN_LENGTH:])
        return start_range, end_range

    @staticmethod
    def compare_with_hash(card_hash, number):
        hash_value = hashlib.sha224(str(number).encode()).hexdigest()
        return number if hash_value == card_hash else False
