from math import erfc, sqrt


def frequency_bit_test(data: str) -> float:
    s_n = (1 / sqrt(len(data))) * (data.count("1") - data.count("0"))
    p_value = erfc((s_n) / sqrt(2))
    return p_value
