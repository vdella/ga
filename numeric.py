def to_bits_from(floating_point):
    integer_part, fractional_part = int(floating_point), floating_point - int(floating_point)
    binary_integer_part = bin(integer_part).lstrip('0b')  # Removes 0b from the prefix
    binary_fractional_part = ''

    # Trim the size at 32 bits maximum. As we are adding a point (.) to the string,
    # we must take into account minus 1 for the size.
    size = 32 - len(binary_integer_part) - 1

    while fractional_part and len(binary_fractional_part) < size:
        fractional_part *= 2
        bit = int(fractional_part)
        if bit == 1:
            fractional_part -= bit
            binary_fractional_part += '1'
        else:
            binary_fractional_part += '0'

    if not binary_integer_part:
        binary_integer_part = '0'

    if not binary_fractional_part:
        binary_fractional_part = '0'

    return binary_integer_part + '.' + binary_fractional_part


def to_float_from(bits):
    integer_part, fractional_part = bits.split('.')

    integer_part = int(integer_part, base=2)
    fractional_part = int(fractional_part, base=2) / 2 ** len(fractional_part)

    return integer_part + fractional_part


if __name__ == '__main__':
    # result = to_bits_from(3.14)
    # print(to_float_from(result))

    result = to_bits_from(0.5)
    print(to_float_from(result))

    # (print(bitwise('101.110', '111.101', '&')))
    # (print(bitwise('101.110', '111.101', '|')))