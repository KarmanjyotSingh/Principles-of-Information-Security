class PRF:
    def __init__(self, security_parameter: int, generator: int,
                 prime_field: int, key: int):
        """
        Initialize values here
        :param security_parameter: 1ⁿ
        :type security_parameter: int
        :param generator: g
        :type generator: int
        :param prime_field: p
        :type prime_field: int
        :param key: k, uniformly sampled key
        :type key: int
        """
        self.security_parameter = security_parameter
        self.generator = generator
        self.prime_field = prime_field
        self.key = key
        

    def evaluate(self, x: int) -> int:
        """
        Evaluate the pseudo-random function at `x`
        :param x: input for Fₖ
        :type x: int
        """
        pass