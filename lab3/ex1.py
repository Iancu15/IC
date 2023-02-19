from operator import is_
from utils import *
    
    
class WeakRNG:
    """ Simple class for weak RNG """
    
    def __init__(self):
        self.rstate = 0
        self.maxn = 255
        self.a = 0  # Set this to correct value
        self.b = 0  # Set this to correct value
        self.p = 257
    
    def init_state(self, rstate):
        """ Initialise rstate """
        self.rstate = rstate  # Set this to some value
        self.update_state()
    
    def update_state(self):
        """ Update state """
        self.rstate = (self.a * self.rstate + self.b) % self.p
    
    def get_prg_byte(self):
        """ Return a new PRG byte and update PRG state """
        s = self.rstate & 0xFF
        self.update_state()
        return s
    
def main():
    # Initialise weak rng
    wr = WeakRNG()
    wr.init_state(0)
    
    # Print ciphertext
    CH = 'a432109f58ff6a0f2e6cb280526708baece6680acc1f5fcdb9523129434ae9f6ae9edc2f224b73a8'
    print("Full ciphertext in hexa:", CH)
    
    # Print known plaintext
    pknown = 'Let all creation'
    nb = len(pknown)
    print("Known plaintext:", pknown)
    pkh = str_2_hex(pknown)
    print("Plaintext in hexa:", pkh)
    
    # Obtain first nb bytes of RNG
    gh = hexxor(pkh, CH[0:nb*2])
    print(gh)
    gbytes = []
    for i in range(nb):
        gbytes.append(ord(hex_2_str(gh[2*i:2*i+2])))
    print("Bytes of RNG: ")
    print(gbytes)
    
    # Break the LCG here:
    # TODO 1: Find a and b, and set them in the RNG
    def get_correct_values():
        for a in range(0, 257):
            for b in range(0, 257):
                wr.a = a
                wr.b = b
                is_ok = 1
                wr.init_state(gbytes[0])
                for i in range(1, len(gbytes)):
                    if gbytes[i] != wr.get_prg_byte():
                        is_ok = 0
                        break
                
                if is_ok == 1:
                    return (a, b)
        
        return (0, 0)
    
    (correct_a, correct_b) = get_correct_values()
    print(correct_a, correct_b)

    # TODO 2: Predict/generate rest of RNG bytes
    wr.init_state(gbytes[0])
    wr.a = correct_a
    wr.b = correct_b
    rng_bytes = [gbytes[0]]
    for i in range(0, int(len(CH)/2)):
        rng_bytes.append(wr.get_prg_byte())
    
    print("all rng bytes:", rng_bytes)

    # TODO 3: Decrypt plaintext
    key = ''
    for i in range(0, len(rng_bytes)):
        key += str_2_hex(chr(rng_bytes[i]))
    
    p = hexxor(key, CH)
    p = hex_2_str(p)
    
    # TODO 4: Print the full plaintext
    print("Full plaintext is:", p)
    
    
if __name__ == "__main__":
    main()

