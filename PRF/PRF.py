# pseudorandom function (PRF) class
import sys
sys.path.append('../PRG')
from PRG import PRG as prg

class PRF:
    def __init__(self, security_parameter: int, 
                 generator: int,
                 prime_field: int, 
                 key: int):
        """
        description : implements a pseudo-random function
        ---
        parameters:
        ---
        security_parameter(int) : n (from 1ⁿ)
        generator(int) : g
        prime_field(int) : p
        key(int) : uniformly sampled seed
        """
        self.security_parameter = security_parameter
        self.generator = generator
        self.prime_field = prime_field
        self.key = key

        # declare a PRG object
        # G : a pseudo-random generator that doubles the given seed 
        self.prg = prg(security_parameter = security_parameter,
                       generator=generator,
                       prime_field=prime_field,
                       expansion_factor=2*security_parameter)

    def slice_left(self,binary_string:str)->str:
        """
        description : slices the left half of the binary string
        ---
        parameters:
        ---
        binary_string : binary string to be sliced
        """
        return binary_string[:len(binary_string)//2]
        
    def slice_right(self,binary_string:str)->str:
        """
        description : slices the right half of the binary string
        ---
        parameters:
        ---
        binary_string : binary string to be sliced
        """
        return binary_string[len(binary_string)//2:]

    def evaluate(self, x: int) -> int:
        """
        description :Evaluate the pseudo-random function at `x`
        ---
        parameters:
        ---
        x(int): input for Fₖ
        """
        # generate the binary string for x, as random oracle
        r = bin(x)[2:].zfill(self.security_parameter)
        # generate the binary string for k, as random oracle
        initial_seed = self.key
        
        for bit in r:
            string = self.prg.generate(initial_seed)
            if bit == '0':
                string = self.slice_left(string)
            else :
                string = self.slice_right(string)
            # string = self.prg.generate(x)
            # print(bit," ",string)
            initial_seed = int(string,2)
           
        # return the final seed
        ret = initial_seed
        return ret

# test 
# expansion_factor=7,security_parameter = 32,generator = 41,prime_field = 2**64-59
# prf = PRF(security_parameter=32,generator=41,prime_field=2**64-59,key=100)

# while True:
#     x = int(input("Enter a number: "))
#     print(prf.evaluate(x))
# # 1001010010011000111010011101100101000011101010000010011110101111
# # 10010100100110001110100111011001
# n = [8,8,10,11,12]
# g = [36,45,71,44,14]
# p = [191,137,179,107,79]
# k = [150,129,568,1056,1389]
# s = [190,201,890,1300,1780]

# for i in range(len(n)):
#     prf = PRF(security_parameter=n[i],generator=g[i],prime_field=p[i],key=k[i])
#     print(prf.evaluate(s[i]))
#     break