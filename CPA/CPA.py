import sys 
sys.path.append('../PRG')
sys.path.append('../PRF')
from PRG import PRG as prg
from PRF import PRF as prf
class CPA:
    # This class implements the encryption scheme that is secured against chosen plain text attack
    # CPA is deterministic encryption scheme
    def __init__(self, security_parameter: int, 
                 prime_field: int,
                 generator: int, 
                 key: int):
        """
        description : implements a CPA encryption scheme
        ---
        parameters:
        ---
        security_parameter(int) : n (from 1ⁿ)
        prime_field(int) : p
        generator(int) : g
        key(int) : uniformly sampled seed
        """

        self.security_parameter = security_parameter
        self.prime_field = prime_field
        self.generator = generator
        self.key = key
        self.prf = prf(security_parameter = security_parameter,
                       prime_field = prime_field,
                       generator = generator,
                       key = key)


    def enc(self, message: int, random_seed: int) -> str:
        """
        description : Encrypt message
        ---
        parameters:
        ---
        message(int) : m
        random_seed(int) : r
        """
        
        n = self.security_parameter
        # initialise the cipher text
        cipher_text = self.prf.prg.convert_to_binary(random_seed,n) # n bits
        Fₖ_r = self.prf.evaluate(random_seed) # Fₖ(r)
        y = message ^ Fₖ_r
        cipher_text += self.prf.prg.convert_to_binary(y,n)
        return cipher_text
        

    def dec(self, cipher: str) -> int:
        """
        description : Decrypt ciphertext to obtain plaintext message
        ---
        parameters:
        ---
        cipher(str) : c
        """
        r = self.prf.slice_left(cipher)
        c = self.prf.slice_right(cipher)
        s = int(c,2)
        Fₖ_r = self.prf.evaluate(r)
        m = s ^ Fₖ_r
        return m

