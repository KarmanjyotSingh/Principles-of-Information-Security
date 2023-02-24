import sys
sys.path.append('../PRF')
from PRF import PRF as prf
class CPA:
    # This class implements the encryption scheme that is secured against chosen plain text attack
    # CPA is deterministic encryption scheme
    def __init__(self, security_parameter: int, 
                 prime_field: int,
                 generator: int, key: int, 
                 mode="CTR"):
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

        mode = self.mode
        n = self.security_parameter
        
        l = len(message) # length of the message to be encoded 
        # number of message blocks
        # assume messages to be a multiple of the security parameter 
        num_blocks = l //n
        cipher_text = bin(random_seed)[2:].zfill(n) 
        if mode == "CTR":    
            for block in range(0,num_blocks):
                m_i = message[block*n:(block+1)*n]
                m_i = int(m_i,2)
                r_i = random_seed+block+1
                Fk_r = self.prf.evaluate(r_i)
                y_i = m_i ^ Fk_r
                cipher_text +=bin(y_i)[2:].zfill(n)
        elif mode == "OFB":
                for block in range(0,num_blocks):
                    m_i = message[block*n:(block+1)*n]
                    m_i = int(m_i,2)
                    r_i = random_seed 
                    Fk_r = self.prf.evaluate(r_i)
                    y_i = m_i ^ Fk_r
                    random_seed = Fk_r
                    cipher_text +=bin(y_i)[2:].zfill(n)
        elif mode == "CBC":
                for block in range(0,num_blocks):
                    m_i = message[block*n:(block+1)*n]
                    m_i = int(m_i,2)
                    r_i = random_seed 
                    x_i = m_i ^ r_i
                    Fk_r = self.prf.evaluate(x_i)
                    y_i = Fk_r
                    cipher_text +=bin(y_i)[2:].zfill(n)      
                    random_seed = y_i 
        return cipher_text
        
    def dec(self, cipher: str) -> str:
        """
        Decrypt ciphertext to obtain plaintext message
        :param cipher: ciphertext c
        :type cipher: str
        """
        n = self.security_parameter
        r_str = cipher[:n]
        r = int(r_str,2)  # random seed 
        cipher = cipher[n:]
        l = len(cipher)
        num_blocks = l // n
        message = ""
        mode = self.mode
        if mode == "CTR":     
            for block in range(0,num_blocks):
                c_i = cipher[block*n:(block+1)*n]
                r_i = r+block +1
                Fk_r = self.prf.evaluate(r_i)
                m_i = Fk_r ^ int(c_i,2)
                message+=bin(m_i)[2:].zfill(n)
        elif mode == "OFB":
            for block in range(0,num_blocks):
                c_i = cipher[block*n:(block+1)*n]
                c_i = int(c_i,2)
                Fk_r = self.prf.evaluate(r)
                m_i = Fk_r ^ c_i
                r = Fk_r
                message+=bin(m_i)[2:].zfill(n)
        elif mode == "CBC":
            for block in range(0,num_blocks):
                c_i = cipher[block*n:(block+1)*n]
                c_i = int(c_i,2)
        return message
