def huffman_decoding(encoded_string, codes):
    decoded_string = ''
    keys = list(codes.keys())
    values = list(codes.values())
    interchanged_dict = dict()
    for i in range(len(keys)):
        interchanged_dict.update({values[i]: keys[i]})
    temp = ''
    for char in encoded_string:
        if temp not in values:
            temp += char
        else:
            decoded_string += interchanged_dict[temp]
            temp = ''
            temp += char
    decoded_string += interchanged_dict[temp]
    return decoded_string

o = huffman_decoding(10010111100111110011010100111111011111011010000001110100101000010110101010001011101011010010110110000001001011001111001011111), {'T': '110', 'E': '1111', 'A': '1110', 'S': '001', 'R': '000', 'U': '011', 'I': '1001', 'L': '1000', 'O': '1011', 'V': '1010', 'D': '0101', 'C': '0100'})
print(o)
