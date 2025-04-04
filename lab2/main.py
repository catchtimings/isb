import argparse


from file_work import read_data, save_data
from task2.tests import (
    frequency_bit_test,
    equally_consecutive_bits,
    longest_sequence_test,
)


def get_arguments() -> str:
    """
    The function parses directory to json file with settings
    :return: path to json file
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file", type=str, help="directory to json file")
    return parser.parse_args().json_file


def tests_sequence(directory: str) -> dict[str, float]:
    """
    The function performs all tests on the sequence
    :param directory: sequence
    :return: result as dictionary
    """
    sequence = read_data(directory)
    return {
        "frequency_bit_test": frequency_bit_test(sequence),
        "equally_consecutive_bits": equally_consecutive_bits(sequence),
        "longest_sequence_test": longest_sequence_test(sequence),
    }


def main():
    try:
        config = read_data(get_arguments())
        cpp_sequence_stats = {
            "cpp_sequence_stats": tests_sequence(config["cpp_seq"])
        }
        java_sequence_stats = {
            "java_sequence_stats": tests_sequence(config["java_seq"])
        }
        stats = {**cpp_sequence_stats, **java_sequence_stats}
        save_data(config["stats"], stats)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
