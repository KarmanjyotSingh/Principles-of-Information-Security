from typing import Optional
import sys
import importlib
sys.path.append('../CBC-MAC')
sys.path.append('../CPA')
from CPA import CPA
CBC_MAC = importlib.import_module("CBC-MAC").CBC_MAC

class CCA:
    def __init__(self, security_parameter: int, prime_field: int,
                 generator: int, key_cpa: int, key_mac: list,
                 cpa_mode="CTR"):
        """
        Initialize the values here
        :param security_parameter: 1ⁿ
        :type security_parameter: int
        :param prime_field: q
        :type prime_field: int
        :param generator: g
        :type generator: int
        :param key_cpa: k1
        :type key_cpa: int
        :param key_mac: k2
        :type key_mac: list[int]
        :param cpa_mode: Block-Cipher mode of operation for CPA
            - CTR
            - OFB
            - CBC
        :type cpa_mode: str
        """

        self.security_parameter = security_parameter
        self.prime_field = prime_field
        self.generator = generator
        self.key_cpa = key_cpa
        self.key_mac = key_mac
        self.cpa_mode = cpa_mode

        self.mac = CBC_MAC(security_parameter=security_parameter,
                          prime_field=prime_field,
                            generator=generator,
                            keys = key_mac)

        self.cpa = CPA(security_parameter=security_parameter,
                          prime_field=prime_field,
                            generator=generator,
                            key = key_cpa,
                            mode = cpa_mode)


    def enc(self, message: str, cpa_random_seed: int) -> str:
        """
        Encrypt message against Chosen Ciphertext Attack
        :param message: m
        :type message: str
        :param cpa_random_seed: random seed for CPA encryption
        :type cpa_random_seed: int
        """
        n = self.security_parameter
        c = self.cpa.enc(message,cpa_random_seed)
        t = self.mac.mac(c)
        t = bin(t)[2:].zfill(n)
        # print(t)
        # print(c)
        c+=t
        return c
    
    def dec(self, cipher: str) -> Optional[str]:
        """
        Decrypt ciphertext to obtain message
        :param cipher: <c, t>
        :type cipher: str
        """
        n = self.security_parameter
        t = cipher[-n:]
        # print(t)
        c = cipher[:-n]
        t = int(t,2)
       
        valid = self.mac.vrfy(c,t)
        if valid:
            d = self.cpa.dec(c)
            return d
        else:
            return None


# a = [8,127,55,34,56,17,"111101000100001110100010011101001111010101001111",100]
# cca = CCA(security_parameter=a[0],
#           prime_field=a[1],
#           generator=a[2],
#           key_cpa=a[3],
#           key_mac=[a[4],a[5]]
#           )

# # c = cca.enc(a[6],a[7])
# # # print(c)
# d = cca.dec(c)
# print(d)
