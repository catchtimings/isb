import argparse
from file_work import read_data


def get_arguments() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file", type=str, help="directory to json file")
    return parser.parse_args().json_file


def main():
    try:
        config = read_data(get_arguments())

        print(read_data(config["cpp_seq"]))
        print(read_data(config["java_seq"]))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()