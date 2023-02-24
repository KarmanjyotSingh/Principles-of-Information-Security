import sys
sys.path.append('../PRF')
from PRF import PRF 
class CBC_MAC:
    def __init__(self, security_parameter: int, 
                 generator: int,
                 prime_field: int, keys: list):
        """
        Initialize the values here
        :param security_parameter: 1ⁿ
        :type security_parameter: int
        :param generator: g
        :type generator: int
        :param prime_field: q
        :type prime_field: int
        :param keys: k₁, k₂
        :type keys: list[int]
        """
        self.security_parameter = security_parameter
        self.generator = generator
        self.prime_field = prime_field
        self.keys = keys
        

    def mac(self, message: str) -> int:
        """
        Message Authentication code for message
        :param message: message encoded as bit-string m
        :type message: str
        """
        # length of the message
        l = len(message) 
        n = self.security_parameter
        g = self.generator
        p = self.prime_field
        k1 = self.keys[0]
        k2 = self.keys[1]
        prf = PRF(security_parameter = n,generator=  g,prime_field =  p,key= k1)
        t = 0
        d = l // n
        for i in range(d):
            m_i = message[i*n:(i+1)*n]
            m_i = int(m_i,2)
            t = t^m_i
            t = prf.evaluate(t)
        prf = PRF(security_parameter = n,generator=  g,prime_field =  p,key= k2)
        return prf.evaluate(t)
    def vrfy(self, message: str, tag: int) -> bool:
        """
        Verify if the tag commits to the message
        :param message: m
        :type message: str
        :param tag: t
        :type tag: int
        """
        t = self.mac(message)
        return True if t == tag else False

# a = [4, 113, 227,2,7,"111010100101"]

# cbc = CBC_MAC(security_parameter=a[0], generator=a[1], prime_field=a[2], keys=[a[3],a[4]])
# print(cbc.mac(a[5]))