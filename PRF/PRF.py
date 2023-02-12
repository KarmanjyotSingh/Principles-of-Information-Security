# pseudorandom function (PRF) class
import sys
sys.path.append('../PRG')
from PRG import PRG as prg

class PRF:
    def __init__(self, security_parameter: int, generator: int,
                 prime_field: int, key: int):
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
                       expansion_factor=security_parameter)

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
        binary_string = self.prg.convert_to_binary(x,self.security_parameter)
        string = self.prg.generate(seed = self.key)
        for bit in binary_string:
            print("string: ",string)
            if bit == '0':
                string = self.slice_left(string)
                print("left: ",string)    
            else :
                string = self.slice_right(string)
                print("right: ",string)
            string = self.prg.generate(self.prg.to_int(string))
                
        return self.prg.to_int(string)

# test 
# expansion_factor=7,security_parameter = 32,generator = 41,prime_field = 2**64-59
# prf = PRF(security_parameter=32,generator=41,prime_field=2**64-59,key=100)

# while True:
#     x = int(input("Enter a number: "))
#     print(prf.evaluate(x))
# # 1001010010011000111010011101100101000011101010000010011110101111
# # 10010100100110001110100111011001