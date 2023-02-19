import random
import math
 
def get_random_string(n):
    """ Generate random bit string """
    return bin(random.getrandbits(n)).lstrip('0b').zfill(n)

def return_prg(n):
    random_str = get_random_string(n)
    prg_generated_str = ''
    for ch in random_str:
        if ch == '1':
            prg_generated_str += '1'
        else:
            rand = random.randint(0, 1)
            if rand == 0:
                prg_generated_str += '0'
            else:
                prg_generated_str += '1'
    
    return (prg_generated_str, random_str)

def frequency_monobit_test(str):
    sum = 0
    for bit in str:
        sum += 2 * (ord(bit) - ord('0')) - 1
    
    statistic = math.fabs(sum) / math.sqrt(len(str))
    p_value = math.erfc(statistic / math.sqrt(2))

    return (p_value >= 0.01)

def main():
    (prg_generated_str, random_str) = return_prg(100)
    if frequency_monobit_test(random_str):
        print("Random string passes the test")
    else:
        print("Random string doesn't pass the test")
    
    if frequency_monobit_test(prg_generated_str):
        print("PRG string generated passes the test")
    else:
        print("PRG generated string doesn't pass the test")

if __name__ == "__main__":
    main()