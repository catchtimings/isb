from functools import partial
import hashlib
import multiprocessing as mp
from tqdm import tqdm

from hash_function_collision.hfc_const import *


class MatchCardNumber:
    @staticmethod
    def card_number(
        card_hash: tuple, last_4_digits: str, card_bin: str, cores=mp.cpu_count()
    ):
        start_range, end_range = MatchCardNumber.card_range(card_bin, last_4_digits)
        with mp.Pool(processes=cores) as p:
            for result in p.imap_unordered(
                partial(MatchCardNumber.compare_with_hash, card_hash),
                tqdm(range(start_range, end_range + 1, SHIFT)),
                chunksize=100,
            ):
                if result:
                    p.terminate()
                    break
        return result

    @staticmethod
    def card_range(card_bin: tuple, last_4_digits: str):
        start_range = int(
            (card_bin[0] + str(START_VALUE)[BIN_LENGTH:])[:-LAST_FOUR_LENGTH] + last_4_digits
        )
        end_range = int(
            card_bin[-1] + (str(END_VALUE)[:-LAST_FOUR_LENGTH] + last_4_digits)[BIN_LENGTH:]
        )
        return start_range, end_range

    @staticmethod
    def compare_with_hash(card_hash: str, number: int):
        hash_value = hashlib.sha224(str(number).encode()).hexdigest()
        return number if hash_value == card_hash else None
