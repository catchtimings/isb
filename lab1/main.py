from file_work import read_json, read_txt, save_json, save_txt
from lab1.task1.text_encryption import make_dict_upper
from task1.text_encryption import text_encryption
from task2.frequency_analysis import frequency_count, sort_dict


def main():
    try:
        TASK1_FILES = read_json("settings.json").get("task1")
        TASK2_FILES = read_json("settings.json").get("task2")

        # task1
        text = read_txt(TASK1_FILES["plain_text"])
        key = read_json(TASK1_FILES["key"])
        encrypted_text = text_encryption(text, key)
        save_txt(TASK1_FILES["encrypted_text"], encrypted_text)

        # task2
        cod25 = read_txt(TASK2_FILES["plain_text"])
        save_json(TASK2_FILES["frequency"], sort_dict(frequency_count(cod25), True))
        key_cod25 = read_json(TASK2_FILES["key"])
        decrypted_text = text_encryption(cod25, key_cod25)
        save_txt(TASK2_FILES["decrypted_text"], decrypted_text)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
