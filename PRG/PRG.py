class PRG:
    """
    Pseudo Random Number Generator [PRG]
    ---
    This class implements a PRG, which generates a pseudo random bit-string 
    from a uniformly sampled seed.
    ---
    Function Parameters :
    security_parameter : n (from 1ⁿ) [int]
    generator : g [int]
    prime_field : p [int]
    expansion_factor : l(n) [int]
    seed : uniformly sampled seed [int]
    """

    def __init__(self, security_parameter: int, generator: int,
                 prime_field: int, expansion_factor: int):
        
        self.security_parameter = security_parameter
        self.generator = generator
        self.prime_field = prime_field
        self.expansion_factor = expansion_factor
        

    def generate(self, seed: int) -> str:
        pass