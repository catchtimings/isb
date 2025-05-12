from functools import partial
import hashlib
import multiprocessing as mp
from tqdm import tqdm

from hash_function_collision.hfc_const import *


class MatchCardNumber:
    @staticmethod
    def card_number(
        card_hash: tuple, last_4_digits: str, card_bin: str, cores=mp.cpu_count()
    ) -> int | None:
        """
        The function matches card number
        :param card_hash: known hash of the card
        :param last_4_digits: last 4 digits of the card
        :param card_bin: known card bin
        :param cores: number of processes that the function will run on
        :return: matched card number or None
        """
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
    def card_range(card_bin: tuple, last_4_digits: str) -> tuple(int, int):
        """
        The function calculate the range for brute force
        :param card_bin: known card bin
        :param last_4_digits: last 4 digits of the card
        :return: start value of range, end value of range
        """
        start_range = int(
            (card_bin[0] + str(START_VALUE)[BIN_LENGTH:])[:-LAST_FOUR_LENGTH] + last_4_digits
        )
        end_range = int(
            card_bin[-1] + (str(END_VALUE)[:-LAST_FOUR_LENGTH] + last_4_digits)[BIN_LENGTH:]
        )
        return start_range, end_range

    @staticmethod
    def compare_with_hash(card_hash: str, number: int) -> int | None:
        """
        The function hashes possible card number and compare with hash
        :param card_hash: known hash of the card
        :param number: possible card number
        :return: matched card number or None
        """
        hash_value = hashlib.sha224(str(number).encode()).hexdigest()
        return number if hash_value == card_hash else None
