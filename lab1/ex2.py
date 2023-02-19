from utils import b64decode, strxor, bin_2_str, hex_2_str

C1 = "000100010001000000001100000000110001011100000111000010100000100100011101000001010001100100000101"
C2 = "02030F07100A061C060B1909"

print(strxor(bin_2_str(C1), "abcdefghijkl"))
print(strxor(hex_2_str(C2), "abcdefghijkl"))