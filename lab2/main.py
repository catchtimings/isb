import argparse


from file_work import read_data
from task2.tests import frequency_bit_test


def get_arguments() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file", type=str, help="directory to json file")
    return parser.parse_args().json_file


def tests_cpp_sequence(directory: str) -> None:
    cpp_sequence = read_data(directory)
    freq_bit_test = frequency_bit_test(cpp_sequence)
    print(freq_bit_test)


def main():
    try:
        config = read_data(get_arguments())
        tests_cpp_sequence(config["cpp_seq"])
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
