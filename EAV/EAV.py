import sys
sys.path.append('../PRG')
from PRG import PRG as prg

# This class implements the eavesdropper adversary
class Eavesdrop:
    def __init__(self, security_parameter: int, key: int, expansion_factor: int,
                 generator: int, prime_field: int):
        """
        Initialize values here
        :param security_parameter: 1ⁿ
        :type security_parameter: int
        :param key: k, uniformly sampled key
        :type key: int
        :param expansion_factor: l(n)
        :type expansion_factor: int
        :param generator: g
        :type generator: int
        :param prime_field: p
        :type prime_field: int
        """
        self.security_parameter = security_parameter
        self.key = key
        self.expansion_factor = expansion_factor
        self.generator = generator
        self.prime_field = prime_field
        self.prg = prg( security_parameter = security_parameter,
                        expansion_factor = expansion_factor, 
                        prime_field = prime_field, 
                        generator = generator)

    def enc(self, message: str) -> str:
        """
        Encrypt Message against Eavesdropper Adversary
        :param message: message encoded as bit-string
        :type message: str
        """
        # generate a uniformly sampled seed
        key = self.key
        w = self.prg.generate(key)
        # print(w)
        # print(len(w))
        ret_str = ""
        for i in range(len(message)):
            if message[i]==w[i]:
                ret_str = ret_str + "0"
            else:
                ret_str = ret_str + "1"
        return ret_str

    def dec(self, cipher: str) -> str:
        """
        Decipher ciphertext
        :param cipher: ciphertext encoded as bit-string
        :type cipher: str
        """

        # generate a uniformly sampled seed
        key = self.key
        w = self.prg.generate(key)
        # print(w)
        # print(len(w))
        ret_str = ""
        for i in range(len(cipher)):
            if cipher[i]==w[i]:
                ret_str = ret_str + "0"
            else:
                ret_str = ret_str + "1"
        return ret_str