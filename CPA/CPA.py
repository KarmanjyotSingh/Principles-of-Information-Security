import sys
sys.path.append('../PRF')
from PRF import PRF as prf
class CPA:
    # This class implements the encryption scheme that is secured against chosen plain text attack
    # CPA is deterministic encryption scheme
    def __init__(self, security_parameter: int, prime_field: int,
                 generator: int, key: int, mode="CTR"):
        """
        description : implements a CPA encryption scheme
        ---
        parameters:
        ---
        security_parameter(int) : n (from 1ⁿ)
        prime_field(int) : p
        generator(int) : g
        key(int) : uniformly sampled seed
        mode(str): Block-Cipher mode of operation
            - CTR
            - OFB
            - CBC
        """
        self.security_parameter = security_parameter
        self.prime_field = prime_field
        self.generator = generator
        self.key = key
        self.prf = prf(security_parameter = security_parameter,
                       prime_field = prime_field,
                       generator = generator,
                       key = key)

        self.mode = mode

    def enc(self, message: str, random_seed: int) -> str:
        """
        Encrypt message against Chosen Plaintext Attack using randomized ctr mode
        :param message: m
        :type message: int
        :param random_seed: ctr
        :type random_seed: int
        """
        n = self.security_parameter

        len_msg = len(message) # length of the message to be encoded 
        arr = []
        # number of message blocks
        # assume messages to be a multiple of the security parameter 
        num_blocks = len_msg //n
        cipher_text = bin(random_seed)[2:].zfill(n) 
        for block in range(0,num_blocks):
            m_i = message[block*n:(block+1)*n]
            arr.append(m_i)
            m_i = int(m_i,2)
            r_i = random_seed+block+1
            Fk_r = self.prf.evaluate(r_i)
            print(m_i," ",Fk_r)
            y_i = m_i ^ Fk_r
            cipher_text +=bin(y_i)[2:].zfill(n)
      
        return cipher_text

    def dec(self, cipher: str) -> str:
        """
        Decrypt ciphertext to obtain plaintext message
        :param cipher: ciphertext c
        :type cipher: str
        """
        l = len(cipher)
        print(l)
        l = l//2
        n = self.security_parameter
        num_blocks = l //n
        # random seed 
        r = int(self.prf.slice_left(cipher),2)
        cipher = self.prf.slice_right(cipher)
        message = ""
        for block in range(0,num_blocks):
            c_i = cipher[block*n:(block+1)*n]
            r_i = r+block
            Fk_r = self.prf.evaluate(r_i)
            m_i = Fk_r ^ int(c_i,2)
            message+=bin(m_i)[2:].zfill(n)
        
        return int(message,2)
    
# 11100011011110000000
# 11100011011110000000
m = ["1010100011100111","11100011011110000000","101011011101","111000101010","1010100110110110"]
r = [4,7,5,37,8]
k = [58,145,113,10,15]
g = [112,189,217,14,3]
p = [307,599,881,59,11]
n = [4,5,6,6,8]

# for i in range(len(m)):
i = 0
cpa = CPA(security_parameter = n[i], prime_field = p[i], generator = g[i], key = k[i])
c = cpa.enc(m[i],r[i])
print("cipher text",c)
d = cpa.dec(c)
print(d)
# break