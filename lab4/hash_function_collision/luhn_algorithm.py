class LuhnAlgorithm:
    @staticmethod
    def luhn_algorithm(sequence: str) -> int:
        """
        Luhn algorithm
        :param sequence: sequence to check
        :return: checksum
        """
        processed_sequence = ""
        for position, digit in enumerate(sequence[::-1], start=1):
            if position % 2 == 0:
                processed_sequence += LuhnAlgorithm.number_processing(digit)
            else:
                processed_sequence += digit

        s = sum(int(digit) for digit in processed_sequence)
        c = 10 - (s % 10) % 10
        return c

    @staticmethod
    def number_processing(num: str) -> str:
        """
        The function doubles the number and
        results in the sum of the digits when the condition is met.
        :param num: number to process
        :return: processed number as string
        """
        doubled_num = int(num) * 2
        if doubled_num >= 10:
            doubled_num = sum(int(digit) for digit in str(doubled_num))
        return str(doubled_num)
