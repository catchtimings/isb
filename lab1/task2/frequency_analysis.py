def frequency_count(data: str) -> dict[str, float]:
    """
    The function finds the frequency of occurrence of a character in the text
    :param data: text in which character frequencies are counted
    :return: frequency as a dictionary
    """
    symbols = set(data)
    result = dict()

    for symbol in symbols:
        if symbol == "\n":
            continue
        cnt = data.count(symbol) / len(data)
        result[symbol] = cnt

    return result


def sort_dict(data: dict[str, str], reverse_flag: bool) -> dict[str, str]:
    """
    The function sorts the dictionary by values in descending order
    :param data: dictionary to sort
    :param reverse_flag: sorting order
    :return: sorted dictionary
    """
    return dict(sorted(data.items(), key=lambda item: item[1], reverse=reverse_flag))


def find_key(data: str, frequency: dict[str, float]) -> dict[str, str]:
    """
    The function finds the decryption key using frequency matching
    :param data: The text in which need to find the key
    :param frequency: Alphabet frequencies
    :return: the key is in the form of a dictionary
    """
    result = dict()
    frequency_data = sort_dict(frequency_count(data), True)
    frequency = sort_dict(frequency, True)

    for cod25_key, absolute_key in zip(frequency_data.keys(), frequency.keys()):
        result[cod25_key] = absolute_key

    return result
