#  Pseudo Random Number Generator (PRG)
class PRG:
    """
    description : This class implements a PRG, which generates a pseudo random bit-string 
    from a uniformly sampled seed.
    ---
    parameters:
    ---
    security_parameter(int) : n (from 1ⁿ) 
    generator(int) : g
    prime_field(int) : p
    expansion_factor(int) : l
    seed(int) : uniformly sampled seed 
    """

    def __init__(self, security_parameter: int, generator: int,
                 prime_field: int, expansion_factor: int):
        
        self.security_parameter = security_parameter # n
        self.generator = generator # g
        self.prime_field = prime_field # p
        self.expansion_factor = expansion_factor # l
        
    def convert_to_binary(self,x:int,l:int)->str:
        """
        description : converts an integer to it's binary representation 
        --- 
        parameters: 
        ---
        x: integer to be converted to binary
        l: length of the binary string ( the length of the desired binary string )
        """
        binary_string  = ""
        while x > 0:
            # get the binary representation of the string
            binary_string = str(x%2) + binary_string
            x = x//2
        ig = len(binary_string)
        
        while ig <= l:
            # print(ig,l)
            # while the length is less than the desired length, pad with 0's
            binary_string = "0" + binary_string
            ig = ig + 1
        
        # print(binary_string, " ", len(binary_string))
        return binary_string
    
    def one_way_function(self,seed:int)->int:
        """
        description : implements dlp as the one way function for our PRG
                      y = g^x mod p
        ---
        parameters:
        ---
        seed : uniformly sampled seed
        """
        g = self.generator
        p = self.prime_field
        return pow(g,seed,p)

    def hardcore_predicate(self,seed:int)->bool:
        """
        description : implements the hardcore predicate for our PRG
        ---
        parameters:
        ---
        seed : uniformly sampled seed
        """
        p = self.prime_field
        return 0 if (seed < p//2) else 1
    
    def to_int(self,x:str)->int:
        """
        description : converts a binary string to an integer
        ---
        parameters:
        ---
        x : binary string
        """
        return int(x,2)
    
    def generate(self, seed: int) -> str:
        """
        description : generates a pseudo random bit-string from a uniformly sampled seed
        ---
        parameters:
        ---
        seed : uniformly sampled seed
        """
        pseudo_random_bit_string = ""
        # constraining the length of the seed to be 32 bits
        SEED_LENGTH = self.security_parameter
        for l in range(1,self.expansion_factor+1):
            y = self.one_way_function(seed) # get the output from the one way function
            pseudo_random_bit_string = self.convert_to_binary(y,SEED_LENGTH)
            hcp = self.hardcore_predicate(seed) # get the hardcore predicate
            pseudo_random_bit_string = pseudo_random_bit_string + str(hcp) # append the hardcore predicate to the pseudo random bit string
            seed = y
            SEED_LENGTH = SEED_LENGTH + 1
        return pseudo_random_bit_string



### testing the PRG
# def to_int(x):    
#     return int(x,2)

prg = PRG(expansion_factor=7,security_parameter = 32,generator = 41,prime_field = 2**32-59)

while True:
    y = int(input("Enter seed: "))
    x = prg.generate(y)
    print(x)
