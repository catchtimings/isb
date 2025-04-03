import math

def frequency_bit_test(data: str) -> float:
    s_n = (data.count("1") - data.count("0")) / math.sqrt(len(data))
    p_value = math.erfc(abs(s_n) / math.sqrt(2))
    return p_value


def equally_consecutive_bits(data: str) -> float:
    seq_len = len(data)
    zeta = data.count("1") / seq_len

    if not (abs(zeta - 0.5) < (2 / math.sqrt(seq_len))):
        return 0

    v_n = 0
    for i in range(seq_len - 1):
        if data[i] == data[i + 1]:
            v_n += 0
        else:
            v_n += 1

    numerator = v_n - 2 * seq_len * (1 - zeta)
    denominator = 2 * math.sqrt(2 * seq_len) * zeta * (1 - zeta)
    p_value = math.erfc(abs(numerator) / denominator)
    return p_value
